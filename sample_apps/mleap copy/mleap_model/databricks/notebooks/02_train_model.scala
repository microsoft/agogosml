// Databricks notebook source
// MAGIC %md
// MAGIC Train, evaluate, and persist model using uploaded mleap_model package

// COMMAND ----------

import com.Microsoft.agogosml.mleap_model_trainer._

// Read in data
val spamDf = spark.read.format("csv")
  .option("delimiter", "\t")
  .load("/mnt/blob_storage/data/SMSSpamCollection.tsv")

// Prepare data (Column rename, StringIndexer, etc)
val prepData = ModelTrainer.prepareData(spamDf)

// Split data
val Array(trainingData, testData) = prepData.randomSplit(Array(0.7, 0.3))

// Train model
val trainedModel = ModelTrainer.train(trainingData)

// Evaluate model
ModelTrainer.evaluate(trainedModel, testData)

// Save model
ModelTrainer.save(trainedModel, "/dbfs/mnt/blob_storage/outmodel.zip", trainingData)
