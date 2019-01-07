// Databricks notebook source
// MAGIC %md
// MAGIC Setup an Mleap Frame and set model file path

// COMMAND ----------

import ml.combust.mleap.runtime.frame.{DefaultLeapFrame, Row}
import ml.combust.mleap.core.types._

// Create leapFrame
val schema: StructType = StructType(
  StructField("text", ScalarType.String)).get
val dataset = Seq(
  Row("Don't stop me now"),
  Row("cause I'm having a good time"))
val leapFrame = DefaultLeapFrame(schema, dataset)

// Model path
val modelPath = "/dbfs/mnt/blob_storage/outmodel.zip"

// COMMAND ----------

// MAGIC %md
// MAGIC Reload Model bundle with ModelTrainer utility "load" function

// COMMAND ----------

import com.Microsoft.agogosml.mleap_model_trainer._

val mleapPipeline1 = ModelTrainer.load(modelPath)
val frameTransformed1 = mleapPipeline1.transform(leapFrame).get
val predictionFrame1 = frameTransformed1.select("prediction").get

println(predictionFrame1.dataset)

// COMMAND ----------

// MAGIC %md
// MAGIC Reload Model bundle with Mleap standard libraries

// COMMAND ----------

import ml.combust.bundle.BundleFile
import ml.combust.mleap.runtime.MleapSupport._
import resource._

// Loads the model from the given path
val bundle = (for(bundleFile <- managed(BundleFile(s"jar:file:${modelPath}"))) yield {
  bundleFile.loadMleapBundle().get
}).opt.get

// 
val mleapPipeline2 = bundle.root
val frameTransformed2 = mleapPipeline2.transform(leapFrame).get
val predictionFrame2 = frameTransformed2.select("prediction").get

println(predictionFrame2.dataset)
