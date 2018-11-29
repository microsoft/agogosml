package com.Microsoft.agogosml.mleap_serving

import ml.combust.bundle.BundleFile
import ml.combust.mleap.runtime.MleapSupport._
import resource._
import ml.combust.mleap.runtime.frame.{DefaultLeapFrame, Row}
import ml.combust.mleap.core.types._

// Schema of the expected input and output, respectively, of the model
case class InputMessage(text: String)
case class OutputMessage(input: InputMessage, prediction: Double)

class Model {

  // Loads the model from the given path
  val modelPath = sys.env("MODEL_PATH")

  val pipelinePath = "jar:file:" + modelPath
  val bundle = (for(bundleFile <- managed(BundleFile(pipelinePath))) yield {
    bundleFile.loadMleapBundle().get
  }).opt.get

  // TO DO: Dynamically create the schema rather than hardcode
  def createSchema(): StructType = {
    // load in our schema
    StructType(StructField("text", ScalarType.String)).get
  }

  // make schema available when Model is initiated
  val schema = createSchema()

  /** Creates a dataframe from the new data received, according to the defined
    * schema
    *
    *  @param message input data
    *  @return a DefaultLeapFrame of a single line
    */
  def createDataFrame(message: InputMessage) : DefaultLeapFrame = {
    val data = Seq(Row(message.text))
    DefaultLeapFrame(schema, data)
  }

  /** Processes a single message through the model
    *
    *  @param message input data to transform
    *  @return a new OutputMessage instance with the model's prediction and
    *          the original message
    */
  def processData(message: InputMessage): OutputMessage = {
    val frame = createDataFrame(message)

    val mleapPipeline = bundle.root
    val frameTransformed = mleapPipeline.transform(frame).get

    // get the prediction out of the transformed dataframe
    val predictionFrame = frameTransformed.select("prediction").get

    // create our output message
    // What one wants to send along to the output will vary by use case
    val processedData = OutputMessage(message, predictionFrame.dataset(0).getDouble(0))
    processedData
  }
}

