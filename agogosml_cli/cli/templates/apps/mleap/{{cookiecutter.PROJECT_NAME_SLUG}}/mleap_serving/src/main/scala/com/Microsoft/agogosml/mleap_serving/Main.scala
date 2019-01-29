package com.Microsoft.agogosml.mleap_serving

import com.google.gson.Gson
import scalaj.http.HttpResponse

object Main extends App {

  /** Sends HTTP request with processed data to the output
    *
    *  @param body transformed OutputMessage returned from the model
    *  @return response from the output http server
    */
  def sendPostRequest(body: OutputMessage): HttpResponse[String] = {
    // where to send the final processed message
    val outputUrl = sys.env("OUTPUT_URL")

    val stringBody = new Gson().toJson(body)
    scalaj.http.Http(outputUrl).postData(stringBody)
      .header("Content-Type", "application/json")
      .header("Charset", "UTF-8").asString
  }

  val s = new ModelServer
  s.main()
}
