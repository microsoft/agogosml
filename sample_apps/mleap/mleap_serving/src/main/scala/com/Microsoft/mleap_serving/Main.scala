import com.twitter.finagle.Http
import com.twitter.util.Await
import io.finch._
import io.finch.circe._
import io.finch.syntax._
import io.circe.generic.auto._
import com.google.gson.Gson
import scalaj.http.Http
import ml.combust.bundle.BundleFile
import ml.combust.mleap.runtime.MleapSupport._
import resource._

// create a simple LeapFrame to transform
import ml.combust.mleap.runtime.frame.{DefaultLeapFrame, Row}
import ml.combust.mleap.core.types._


object Main extends App {

  val port = sys.env("PORT")
  val output_url = sys.env("OUTPUT_URL")
  val model_path = sys.env("MODEL_PATH")
  val pipeline_path = "jar:file:" + model_path
  //Users/margaretmeehan/Desktop/worktings/ASB/agogosml/sample_apps/mleap/frank_model_export_json.zip"

  //MLEAP CODE TO MOVE TO SEPARATE CLASS

  val bundle = (for(bundleFile <- managed(BundleFile(pipeline_path))) yield {
    bundleFile.loadMleapBundle().get
  }).opt.get

  case class InputMessage(text: String)
  case class OutputMessage(text: String, prediction: Double)
  case class Response(message: String)

  def sendPostRequest(body: OutputMessage): String = {
    val stringBody = new Gson().toJson(body)
    val response = scalaj.http.Http(output_url).postData(stringBody)
      .header("Content-Type", "application/json")
      .header("Charset", "UTF-8").asString
    return response.body
  }

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

  val receiveMessage: Endpoint[Response] =
    post("message" :: jsonBody[InputMessage]) { message: InputMessage =>
      // feed msg into mleap model
      val transformedMessage = transformMessage((message))

      // send the transformed data to the output writer
      val r = sendPostRequest(transformedMessage)

      // send OK response to the input container if OK. Otherwise, handle exception
      Ok(Response(r))
    }.handle {
      case e: Exception =>
        BadRequest(e)
    }

  Await.ready(com.twitter.finagle.Http.server.serve(":" + port, receiveMessage.toService))
}

