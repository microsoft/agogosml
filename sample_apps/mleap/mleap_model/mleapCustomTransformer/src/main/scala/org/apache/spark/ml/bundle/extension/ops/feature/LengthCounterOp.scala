package org.apache.spark.ml.bundle.extension.ops.feature

import ml.combust.bundle.BundleContext
import ml.combust.bundle.dsl._
import ml.combust.bundle.op.{OpModel, OpNode}
import ml.combust.mleap.core.feature.LengthCounterModel
// import ml.combust.mleap.runtime.MleapContext
import org.apache.spark.ml.bundle.SparkBundleContext
import org.apache.spark.ml.mleap.feature.LengthCounter


class LengthCounterOp extends OpNode[SparkBundleContext, LengthCounter, LengthCounterModel] {
  override val Model: OpModel[SparkBundleContext, LengthCounterModel] = new OpModel[SparkBundleContext, LengthCounterModel] {
    // the class of the model is needed for when we go to serialize JVM objects
    override val klazz: Class[LengthCounterModel] = classOf[LengthCounterModel]

    // a unique name for our op: "string_map"
    // this should be the same as for the MLeap transformer serialization
    override def opName: String = "length_counter" //Bundle.BuiltinOps.feature.length_counter

    override def store(model: Model, obj: LengthCounterModel)
                      (implicit context: BundleContext[SparkBundleContext]): Model = {
      model
    }

    override def load(model: Model)
                     (implicit context: BundleContext[SparkBundleContext]): LengthCounterModel = {
      LengthCounterModel()
    }
  }
  override val klazz: Class[LengthCounter] = classOf[LengthCounter]

  override def name(node: LengthCounter): String = node.uid

  override def model(node: LengthCounter): LengthCounterModel = node.model

  override def load(node: Node, model: LengthCounterModel)
                   (implicit context: BundleContext[SparkBundleContext]): LengthCounter = {
    new LengthCounter(uid = node.name, model = model).
      setInputCol(node.shape.standardInput.name).
      setOutputCol(node.shape.standardOutput.name)
  }

  override def shape(node: LengthCounter)(implicit context: BundleContext[SparkBundleContext]): NodeShape =
    NodeShape().withStandardIO(node.getInputCol, node.getOutputCol)
}