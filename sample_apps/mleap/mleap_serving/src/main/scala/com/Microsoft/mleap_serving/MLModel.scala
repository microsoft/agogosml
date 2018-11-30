package mleap_model

import ml.combust.bundle.BundleFile
import ml.combust.mleap.runtime.MleapSupport._
import resource._
import ml.combust.mleap.runtime.frame.{DefaultLeapFrame, Row}
import ml.combust.mleap.core.types._

class MLModel {

  val pipeline_path = "jar:file:" + sys.env("MODEL_PATH")

  case class InputMessage(text: String)
  case class OutputMessage(text: String, prediction: Double)

  val bundle = (for(bundleFile <- managed(BundleFile(pipeline_path))) yield {
    bundleFile.loadMleapBundle().get
  }).opt.get

  def transformMessage(message: InputMessage): OutputMessage = {
    val schema = StructType(StructField("text", ScalarType.String)).get
    val data = Seq(Row(message.text))
    val frame = DefaultLeapFrame(schema, data)

    // transform the dataframe using our pipeline
    val mleapPipeline = bundle.root
    val frame_transformed = mleapPipeline.transform(frame).get

    val prediction_frame = frame_transformed.select("prediction").get
    val transformedMessage = OutputMessage(message.text, prediction_frame.dataset(0).getDouble(0))
    return transformedMessage
  }

}

