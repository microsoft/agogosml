package com.Microsoft.agogosml.mleap_serving

import org.scalatest._
import io.finch._
import com.twitter.io.Buf
import com.twitter.finagle.http.Status

class MainTest extends FlatSpec with Matchers {
  val model = new Model
  val server = new ModelServer
  val testInputMessage = InputMessage("{'text': 'test message'}")
  val testOutputMessage = OutputMessage(testInputMessage, 1.0)

  // this test should be modified once we decide on a format to send to the output
  it should "transform a message in the correct form" in {
    val transformedMessage = model.processData(testInputMessage)
    assert(transformedMessage.input == testInputMessage)
  }

  it should "send correctly formatted message to output and receive OK response" in {
    val resp = Main.sendPostRequest(testOutputMessage)
    assert(resp.code == 200)
  }

  it should "get status OK on correct schema" in {
    var input = Input.post("/").withBody[Application.Json](Buf.Utf8("{\"text\":\"correct schema\"}"))
    val res = server.receiveMessage(input)
    res.awaitOutputUnsafe().map(_.status) shouldBe Some(Status.Ok)
  }

  it should "get status Bad Request on incorrect schema" in {
    var input = Input.post("/").withBody[Application.Json](Buf.Utf8("{\"tst\":\"incorrect schema\"}"))
    val res = server.receiveMessage(input)
    res.awaitOutputUnsafe().map(_.status) shouldBe Some(Status.BadRequest)
  }
}