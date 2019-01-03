package com.Microsoft.agogosml.mleap_model_trainer

import org.apache.spark.sql.SparkSession
import org.apache.spark.{SparkConf, SparkContext}

/**
  * Use this to test the app locally, from sbt:
  * sbt "run inputFile.txt /tmp/modelout"
  *  (+ select ModelLocalApp when prompted)
  */
object ModelLocalApp extends App{
  val (inputFile, outputModel) = (args(0), args(1))
  val conf = new SparkConf()
    .setMaster("local")
    .setAppName("Model Training app")

  Runner.run(conf, inputFile, outputModel)
}

/**
  * Use this when submitting the app to a cluster with spark-submit
  * */
object ModelApp extends App{
  val (inputFile, outputModel) = (args(0), args(1))

  // spark-submit command should supply all necessary config elements
  Runner.run(new SparkConf(), inputFile, outputModel)
}

object Runner {
  def run(conf: SparkConf, inputFile: String, outputModelPath: String): Unit = {

    val spark = SparkSession
      .builder()
      .config(conf)
      .getOrCreate()

    val spamDf = spark.read.format("csv")
      .option("delimiter", "\t")
      .load(inputFile)

    val spamDfRenamed = spamDf
      .withColumnRenamed("_c0", "hamOrSpam")
      .withColumnRenamed("_c1", "text")

    val trainedModel = ModelTrainer.train(spamDfRenamed)

    ModelTrainer.save(trainedModel, outputModelPath, spamDfRenamed)

    println("Done!")
  }
}
