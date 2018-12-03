package ml.combust.mleap.bundle.ops.feature

import ml.combust.bundle.BundleContext
import ml.combust.bundle.dsl._
import ml.combust.bundle.op.OpModel
import ml.combust.mleap.bundle.ops.MleapOp
import ml.combust.mleap.core.feature.LengthCounterModel
import ml.combust.mleap.runtime.MleapContext
import ml.combust.mleap.runtime.transformer.feature.LengthCounter


class LengthCounterOp extends MleapOp[LengthCounter, LengthCounterModel] {
  override val Model: OpModel[MleapContext, LengthCounterModel] = new OpModel[MleapContext, LengthCounterModel] {
    // the class of the model is needed for when we go to serialize JVM objects
    override val klazz: Class[LengthCounterModel] = classOf[LengthCounterModel]

    // a unique name for our op: "string_map"
    override def opName: String = "length_counter" //Bundle.BuiltinOps.feature.length_counter

    override def store(model: Model, obj: LengthCounterModel)
                      (implicit context: BundleContext[MleapContext]): Model = {
      model
    }

    override def load(model: Model)
                     (implicit context: BundleContext[MleapContext]): LengthCounterModel = {
      LengthCounterModel()
    }
  }

  // the core model that is used by the transformer
  override def model(node: LengthCounter): LengthCounterModel = node.model
}