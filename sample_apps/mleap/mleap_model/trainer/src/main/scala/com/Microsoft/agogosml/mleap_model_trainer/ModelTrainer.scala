package com.Microsoft.agogosml.mleap_model_trainer

import org.apache.spark.sql._
import org.apache.spark.ml.feature.{CountVectorizer, IDF, StringIndexer, Tokenizer}
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.tuning.{CrossValidator, ParamGridBuilder}
import org.apache.spark.ml.{Pipeline, PipelineModel}
import org.apache.spark.ml.evaluation.BinaryClassificationEvaluator
import ml.combust.bundle.BundleFile
import ml.combust.bundle.serializer.SerializationFormat
import ml.combust.mleap.spark.SparkSupport._
import ml.combust.mleap.runtime.MleapSupport._
import ml.combust.mleap.runtime.frame.Transformer
import org.apache.spark.ml.bundle.SparkBundleContext
import resource._

// Custom transformer
import org.apache.spark.ml.mleap.feature.LengthCounter

/**
 * Train, evaluate, model
 */

object ModelTrainer {

  def prepareData(df: Dataset[Row]) : Dataset[Row] = {
    val sparkDFrame = df
      .withColumnRenamed("_c0", "hamOrSpam")
      .withColumnRenamed("_c1", "text")
    // Index data outside of pipeline
    val indexer = new StringIndexer()
      .setInputCol("hamOrSpam")
      .setOutputCol("label")
    val indexedDf = indexer
      .fit(sparkDFrame)
      .transform(sparkDFrame)
    indexedDf
  }

  def train(df: Dataset[Row]) : PipelineModel = {
    val tokenizer = new Tokenizer()
      .setInputCol("text")
      .setOutputCol("words")

    val cvModel = new CountVectorizer()
      .setInputCol(tokenizer.getOutputCol)
      .setOutputCol("rawFeatures")

    val idf = new IDF()
      .setInputCol("rawFeatures")
      .setOutputCol("features")

    val lr = new LogisticRegression()
      .setMaxIter(10)
      .setFeaturesCol("features")
      .setLabelCol("label")

    // Custom transformer
    val lc = new LengthCounter()
      .setInputCol("text")
      .setOutputCol("length_counter_out")

    val pipeline = new Pipeline()
      .setStages(Array(tokenizer, cvModel, idf, lr, lc))

    // Cross Validation
    val paramGrid = new ParamGridBuilder()
      .addGrid(lr.regParam, Array(0.1, 0.01))
      .build()

    val cv = new CrossValidator()
      .setEstimator(pipeline)
      .setEstimatorParamMaps(paramGrid)
      .setNumFolds(5)
      .setEvaluator(new BinaryClassificationEvaluator)

    val pipelineModel = cv.fit(df)
    val model = pipelineModel.bestModel.asInstanceOf[PipelineModel]

    model
  }

  def evaluate(model: PipelineModel, testDf: Dataset[Row]) : Double = {
    val evaluator = new BinaryClassificationEvaluator()
    val predictions = model.transform(testDf)
    val accuracy = evaluator.evaluate(predictions)
    accuracy
  }

  def save(model: PipelineModel, outPath: String, inputDf: Dataset[Row]) : Unit = {
    // Create transformedDf
    val transformedDf = model.transform(inputDf)
    implicit val context = SparkBundleContext().withDataset(transformedDf)
    // save the pipeline
    (for(modelFile <- managed(BundleFile(s"jar:file:${outPath}"))) yield {
      model.writeBundle.format(SerializationFormat.Json).save(modelFile)(context)
    }).tried.get
  }

  def load(inPath: String) : Transformer = {
    val bundle = (for(bundleFile <- managed(BundleFile(s"jar:file:${inPath}"))) yield {
      bundleFile.loadMleapBundle().get
    }).opt.get
    bundle.root
  }
}
