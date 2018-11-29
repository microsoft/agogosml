import com.twitter.finagle.Http
import com.twitter.util.Await
import io.finch._
import io.finch.circe._
import io.finch.syntax._
import io.circe.generic.auto._
import com.google.gson.Gson
import scalaj.http.Http

object Main extends App {

  val port = sys.env("PORT")
  val output_url = sys.env("OUTPUT_URL")

  case class Message(key: String, value: String)
  case class Response(message: String)

  def sendPostRequest(body: Message): String ={
    val stringBody = new Gson().toJson(body)
    val response = scalaj.http.Http(output_url).postData(stringBody)
      .header("Content-Type", "application/json")
      .header("Charset", "UTF-8").asString
    return response.body
  }

  val receiveMessage: Endpoint[Response] =
    post("message" :: jsonBody[Message]) { message: Message =>
      // feed msg into mleap model

      // send the result from the model to the output

      // if all succeeds, send the response from the output container
      val r = sendPostRequest(message)
      Ok(Response(r))
    }.handle {
      case e: Exception =>
        println(e)
        BadRequest(e)
    }

  Await.ready(com.twitter.finagle.Http.server.serve(":" + port, receiveMessage.toService))
}

