import com.twitter.finagle.Http
import com.twitter.util.Await
import io.finch._
import io.finch.circe._
import io.finch.syntax._
import io.circe.generic.auto._
import com.google.gson.Gson
import scalaj.http.Http
import mleap_model._

object Main extends App {

  val port = sys.env("PORT")
  val output_url = sys.env("OUTPUT_URL")

  val model = new MLModel
  case class Response(message: String)

  def sendPostRequest(body: model.OutputMessage): String = {
    val stringBody = new Gson().toJson(body)
    val response = scalaj.http.Http(output_url).postData(stringBody)
      .header("Content-Type", "application/json")
      .header("Charset", "UTF-8").asString
    return response.body
  }

  val receiveMessage: Endpoint[Response] =
    post(jsonBody[model.InputMessage]) { message: model.InputMessage =>
      // feed msg into mleap model after validation
      val transformedMessage = model.transformMessage(message)

      // send the transformed data to the output writer
      val r = sendPostRequest(transformedMessage)
      println(r)

      // send OK response to the input container if OK. Otherwise, handle exception
      Ok(Response(r))
    }.handle {
      case e: Exception =>
        BadRequest(e)
    }

  Await.ready(com.twitter.finagle.Http.server.serve(":" + port, receiveMessage.toService))
}

