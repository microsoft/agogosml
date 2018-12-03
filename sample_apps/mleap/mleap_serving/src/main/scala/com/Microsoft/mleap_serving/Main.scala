package com.Microsoft.mleap_serving

import com.twitter.util.Await
import io.finch._
import io.finch.circe._
import io.finch.syntax._
import io.circe.generic.auto._
import com.google.gson.Gson
import mleap_model._

object Main extends App {

  // port to serve the app
  val port = sys.env("PORT")

  // where to send the final processed message
  val output_url = sys.env("OUTPUT_URL")

  // instantiate the machine learning model
  val model = new MLModel

  // Format of response to REST request
  case class Response(message: String)

  /** Sends HTTP request with processed data to the output
    *
    *  @param body transformed OutputMessage returned from the model
    *  @return response from the output http server
    */
  def sendPostRequest(body: model.OutputMessage): String = {
    val stringBody = new Gson().toJson(body)
    val response = scalaj.http.Http(output_url).postData(stringBody)
      .header("Content-Type", "application/json")
      .header("Charset", "UTF-8").asString
    return response.body
  }

  /** HTTP server that receives incoming data, feeds it to the model model,
    * and pushes it through the pipeline to the output */
  def receiveMessage: Endpoint[Response] =
    post(jsonBody[model.InputMessage]) { message: model.InputMessage =>
      // feed msg into mleap model
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

