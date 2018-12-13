// Databricks notebook source
// MAGIC %md
// MAGIC Train, evaluate, and persist model using uploaded mleap_model package

// COMMAND ----------

import com.Microsoft.agogosml.mleap_model_trainer._

// Read in data
val spamDf = spark.read.format("csv")
  .option("delimiter", "\t")
  .load("/mnt/blob_storage/data/SMSSpamCollection.tsv")
val spamDfRenamed = spamDf
  .withColumnRenamed("_c0", "hamOrSpam")
  .withColumnRenamed("_c1", "text")
val Array(trainingData, testData) = spamDfRenamed.randomSplit(Array(0.7, 0.3))

// Train model
val trainedModel = ModelTrainer.train(trainingData)

// Evaluate model
ModelTrainer.evaluate(trainedModel, testData)

// Save model
ModelTrainer.save(trainedModel, "/dbfs/mnt/blob_storage/outmodel", trainingData)
