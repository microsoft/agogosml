package com.Microsoft.agogosml.mleap_model_trainer

/**
 * Tests for Model Trainer
 */

import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext, SparkSessionProvider}
import org.apache.spark.sql.SparkSession
import org.scalatest.FunSuite
import java.io.File

import ml.combust.mleap.core.types.{ScalarType, StructType}
import ml.combust.mleap.runtime.frame.{DefaultLeapFrame, Row}
import ml.combust.mleap.core.types._

class ModelTrainerTest extends FunSuite with DataFrameSuiteBase with SharedSparkContext {

  override implicit def reuseContextIfPossible: Boolean = true

  // Need to retrieve access to SparkSesssion from SparkContext
  // but DataFrameSuiteBase has unneeded dependency on Spark-hive
  // See github issue: https://github.com/holdenk/spark-testing-base/issues/148#issuecomment-437859541
  override def beforeAll(): Unit = {
    super[SharedSparkContext].beforeAll()
    SparkSessionProvider._sparkSession = SparkSession
      .builder()
      .appName("test-app")
      .master("local[2]")
      .getOrCreate()
  }

  def fixture = {
    // Create SparkDf
    val inputFile = getClass.getResource("/SMSSpamCollection.tsv").toString
    val spamDf = spark.read.format("csv")
      .option("delimiter", "\t")
      .load(inputFile)

    // Create leapFrame
    val schema: StructType = StructType(StructField("text", ScalarType.String)).get
    val dataset = Seq(
      Row("Don't stop me now"),
      Row("cause I'm having a good time"))
    val mleapFrame = DefaultLeapFrame(schema, dataset)

    new {
      val sparkDf = spamDf
      val mleapDf = mleapFrame
    }
  }

  test("trained model with baseline accuracy given sample data is created"){
    val f = fixture
    val prepDf = ModelTrainer.prepareData(f.sparkDf)
    val Array(trainingData, testData) = prepDf.randomSplit(Array(0.7, 0.3))
    val trainedModel = ModelTrainer.train(trainingData)
    val accuracy = ModelTrainer.evaluate(trainedModel, testData)
    assert(accuracy > 0.5)
  }

  test("Can save and reload model") {
    val f = fixture
    val prepDf = ModelTrainer.prepareData(f.sparkDf)
    val trainedModel = ModelTrainer.train(prepDf)
    val modelPath = "/tmp/outmodel.zip"
    try {
      // Try to save and reload model
      ModelTrainer.save(trainedModel, modelPath, prepDf)
      val mleapModel = ModelTrainer.load(modelPath)
      mleapModel.transform(f.mleapDf).get
    }
    finally new File(modelPath).delete()

  }
}
