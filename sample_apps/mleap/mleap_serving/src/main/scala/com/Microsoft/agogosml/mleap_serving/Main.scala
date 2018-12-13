package com.Microsoft.agogosml.mleap_serving

import com.twitter.util.Await
import io.finch._
import io.finch.circe._
import io.finch.syntax._
import io.circe.generic.auto._
import com.google.gson.Gson
import com.twitter.finagle.ListeningServer
import scalaj.http.HttpResponse

object Main extends App {

  // port to serve the app
  val port = sys.env("PORT")

  // where to send the final processed message
  val outputUrl = sys.env("OUTPUT_URL")

  // instantiate the machine learning model
  val model = new Model

  /** Sends HTTP request with processed data to the output
    *
    *  @param body transformed OutputMessage returned from the model
    *  @return response from the output http server
    */
  def sendPostRequest(body: OutputMessage): HttpResponse[String] = {
    val stringBody = new Gson().toJson(body)
    val response = scalaj.http.Http(outputUrl).postData(stringBody)
      .header("Content-Type", "application/json")
      .header("Charset", "UTF-8").asString
    return response
  }

  /** HTTP server that receives incoming data, feeds it to the model model,
    * and pushes it through the pipeline to the output */
  def receiveMessage: Endpoint[String] =
    post(jsonBody[InputMessage]) { message: InputMessage =>
      // feed msg into mleap model
      val transformedMessage = model.transformMessage(message)

      // send the transformed data to the output writer
      val r = sendPostRequest(transformedMessage).body
      println(r)

      // send OK response to the input container if OK. Otherwise, handle exception
      Ok(r)
    }.handle {
      case e: Exception =>
        BadRequest(e)
    }

  def initiateServer(): ListeningServer = {
    Await.ready(com.twitter.finagle.Http.server.serve(":" + port, receiveMessage.toService))
  }
  
  initiateServer()
}
