package com.Microsoft.agogosml.mleap_serving

import com.twitter.finagle.{Http, ListeningServer}
import com.twitter.util.Await
import io.finch._
import io.finch.circe._
import io.finch.syntax._
import io.circe.generic.auto._
import org.slf4j.LoggerFactory

class ModelServer {

  val logger = LoggerFactory.getLogger(classOf[ModelServer])

  // instantiate the machine learning model
  val model = new Model

  // port to serve the app
  val port = sys.env("PORT")

  /** Processes incoming through the model, send it along the pipeline
    * @param message received from the server
    */
  def handleIncomingMessage(message: InputMessage) : String = {
    // feed message into mleap model
    val processedData = model.processData(message)
    // send the transformed data to the output
    Main.sendPostRequest(processedData).body
  }

  /** HTTP server that receives incoming data, processes it,
    * and pushes it through the pipeline to the output */
  def receiveMessage : Endpoint[String] =
    post(jsonBody[InputMessage]) { message: InputMessage =>

      handleIncomingMessage(message)

      logger.info("Incoming piece of data has been processed")
      // send OK response to the input container. If error, handle exception
      Ok("Message Received and Processed Successfully")
    }.handle {
      case e: Exception =>
        logger.error("There was an exception when processing the incoming data")
        BadRequest(e)
    }

  /** Initiates an HTTP server */
  def main() : ListeningServer = {
    logger.info(s"Serving the application on port ${port}", port)

    val server = Http.server.serve(":" + port, receiveMessage.toService)
    Await.ready(server)
  }
}
