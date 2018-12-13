package com.Microsoft.agogosml.mleap_model_trainer

/**
 * Tests for Model Trainer
 */

import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext, SparkSessionProvider}
import org.apache.spark.sql.SparkSession
import org.scalatest.FunSuite

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

  test("trained model with baseline accuracy given sample data is created"){

    val inputFile = getClass.getResource("/SMSSpamCollection.tsv").toString

    val spamDf = spark.read.format("csv")
      .option("delimiter", "\t")
      .load(inputFile)

    val spamDfRenamed = spamDf
      .withColumnRenamed("_c0", "hamOrSpam")
      .withColumnRenamed("_c1", "text")

    val Array(trainingData, testData) = spamDfRenamed.randomSplit(Array(0.7, 0.3))

    val trainedModel = ModelTrainer.train(trainingData)
    val accuracy = ModelTrainer.evaluate(trainedModel, testData)

    assert(accuracy > 0.7)

  }
}
