package com.Microsoft.agogosml.mleap_serving

import org.scalatest._
import io.finch._
import com.twitter.io.Buf

class MainTest extends FlatSpec with Matchers {
  val model = new Model
  val testInputMessage = InputMessage("{'text': 'test message'}")
  val testOutputMessage = OutputMessage(testInputMessage, 1.0)

  it should "transform a message in the correct form" in {
    val transformedMessage = model.transformMessage(testInputMessage)
    assert(transformedMessage.input == testInputMessage)
  }

  it should "send a post request to output" in {
    val resp = Main.sendPostRequest(testOutputMessage)
    assert(resp.code == 200)
  }

  it should "receive our message and send an OK" in {
    val foo = Input.post("/").withBody[Application.Json](Buf.Utf8("{\"text\":\"the cat jumped\"}"))
    val res = Main.receiveMessage(input = foo)
    res.awaitValueUnsafe() shouldBe Some("heres some post")
  }

  it should "throw an error because of an incorrect message" in {
    val foo = Input.post("/").withBody[Application.Json](Buf.Utf8("{\"incorrect\":\"bad msg\"}"))
    val res = Main.receiveMessage(input = foo)
    res.awaitValueUnsafe() shouldBe an [Exception]
  }
}