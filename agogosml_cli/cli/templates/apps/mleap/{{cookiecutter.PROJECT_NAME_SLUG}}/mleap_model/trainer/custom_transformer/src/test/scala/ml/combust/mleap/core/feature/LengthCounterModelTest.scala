package ml.combust.mleap.core.feature

import org.scalatest.FunSuite

class LengthCounterModelTest extends FunSuite {

  test("Core model logic is correct") {
    val model = new LengthCounterModel()
    val result = model("Is this the real life? Is this just fantasy?")
    assert(result == 44)
  }

}
