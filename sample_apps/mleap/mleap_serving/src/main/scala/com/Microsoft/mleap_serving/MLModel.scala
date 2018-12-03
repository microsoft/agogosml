package mleap_model

import ml.combust.bundle.BundleFile
import ml.combust.mleap.runtime.MleapSupport._
import resource._
import ml.combust.mleap.runtime.frame.{DefaultLeapFrame, Row}
import ml.combust.mleap.core.types._

class MLModel {

  // Schema of the expected input and output, respectively of the model
  case class InputMessage(text: String)
  case class OutputMessage(input: InputMessage, prediction: Double)

  // Loads the model from the given path
  val pipeline_path = "jar:file:" + sys.env("MODEL_PATH")
  val bundle = (for(bundleFile <- managed(BundleFile(pipeline_path))) yield {
    bundleFile.loadMleapBundle().get
  }).opt.get

  /** Processes a single message through the model
    *
    *  @param message input data to transform
    *  @return a new OutputMessage instance with the model's prediction and
    *          the original message
    */
  def transformMessage(message: InputMessage): OutputMessage = {
    val schema = StructType(StructField("text", ScalarType.String)).get
    val data = Seq(Row(message.text))
    val frame = DefaultLeapFrame(schema, data)

    val mleapPipeline = bundle.root
    val frame_transformed = mleapPipeline.transform(frame).get

    val prediction_frame = frame_transformed.select("prediction").get
    val transformedMessage = OutputMessage(message, prediction_frame.dataset(0).getDouble(0))
    return transformedMessage
  }

}

