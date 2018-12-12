MLeap Model Example
============================

This documentation walks the user through an MLeap model app example.
This examples includes:

- Databricks setup
- Creation of Spark Model
- Creation of custom transformer in Scala
- Serving of the Model

Requirements to Run Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  azure-cli
-  java 8
-  scala 2.11
-  sbt 1.2.1
-  spark > 2.3
-  mleap

Databricks Setup
------------------

<Lace to add more here>



MLeap Model
----------------

MLeap provides functionality to serialize trained pipelines and algorithm to a
``BundleFile`` which can then easily be deployed.
Our example implements a pipeline with a trained model and a custom
transformer.

`Model <mleap_model/model/src/main/scala/com/Microsoft/agogosml/mleap_model/Model.scala>`__
contains our Spark model which imports the custom transformer ``LengthCounter``. The Spark
model is a simple classification model on the `Spam or Ham` dataset. The MLeap ``BundleFile``
is saved/outputted as a ``jar`` which can then be saved as an artifact.

`ModelApp <mleap_model/model/src/main/scala/com/Microsoft/agogosml/mleap_model/ModelApp.scala>`__
executes the training of the Spark model in a Spark session (locally or on a cluster).


MLeap Custom Transformer
-----------------------------

MLeap supports a range of `transformers
<http://mleap-docs.combust.ml/core-concepts/transformers/support.html>`__,
however as these are limited, so it may be necessary for you to write your
own custom implementation.
We have written a simple example of a custom transformer called ``LengthCounter``
which returns the count of words as an ``Int`` given a ``String`` input.

There are a number of `standard steps
<https://github.com/combust/mleap-docs/blob/master/mleap-runtime/
custom-transformer.md>`__  for creating a custom transformer in the MLeap
docs. The steps to creating a custom transformer are:

1. Core Model
_______________
`LengthCounterModel <mleap_model/model/mleapCustomTransformer/src/main/scala/ml/combust/mleap/
core/ feature/LengthCounterModel.scala>`__ defines the inputs and outputs of the transformer.


2. MLeap Transformer
_____________________
`LengthCounter <mleap_model/model/mleapCustomTransformer/src/main/scala/ml/combust/mleap/runtime/
transformer/feature/LengthCounter.scala>`__ inherits from the transformer base class but
allows us to pass in our transformer by redefining the ``UserDefinedFunction``. The
``LengthCounterModel`` is passed as an input to the ``LengthCounter``.


3. Spark Transformer
_____________________
`LengthCounter <mleap_model/model/mleapCustomTransformer/src/main/scala/org/apache/spark/ml/mleap/
feature/LengthCounter.scala>`__ is a spark transformer that knows how to execute against a
Spark DataFrame (just as you would write a custom Spark transformer)

There is an important method within this class:

- ``transform``: applies the LengthCounterModel within the ``transform`` method.


4. MLeap Serialization
_________________________
`LengthCounterOp <mleap_model/model/
mleapCustomTransformer/src/main/scala/ml/combust/mleap/bundle/ops/feature/
LengthCounterOp.scala>`__ defines how we serialize and deserialize our model and transformer
to/from an MLeap ``BundleFile``.

There are two important methods within this class:

-  ``store``: defines how the transformer is stored
-  ``load``:  defines what how the transformer is loaded

5. Spark Serialization
_______________________
`LengthCounterOp <mleap_model/model/mleapCustomTransformer/src/main/scala/org/apache/spark/ml/
bundle/extension/ops/feature/LengthCounterOp.scala>`__  defines how we serialize and
deserialize the custom Spark transformer to/from MLeap.


6. MLeap Registry & Spark Registry
____________________________________
The custom transformer needs to be added to the MLeap registry and the Spark registry with a
`reference.conf <mleap_model/model/mleapCustomTransformer/src/main/resources/reference.conf>`__ file in
our project.


Serving the Model
------------------

The model is put into production by wrapping an HTTP server around the MLeap model bundle.
The HTTP server receives incoming data with a `POST` request and feeds it as input to the
model. Finally, it receives the transformed data/scores and pushes it through the pipeline to the
output.

The `Main <mleap_serving/src/main/scala/com/Microsoft/agogosml/mleap_serving/Main.scala>`__
function provides the functionality.

The `MLModel <mleap_serving/src/main/scala/com/Microsoft/agogosml/mleap_serving/
MLModel.scala>`__ class takes care of loading the model bundle from the ``jar`` file and scoring
the incoming data that is received from the HTTP server.

The ``jar`` file has to be located in the ``mleap_serving/lib/`` directory.


More to be added here <Margaret?>



Process of Running Model
-------------------------

<LACE/MARGARET TO ADD MORE HERE>

<HOW TO RUN MANUALLY?!>

<HOW TO RUN USING DOCKERFILES & FINISH DOCKERFILES>

Jar file is created by the model and CI/CD pipeline picks up the jar file and dumps
into artifacts in Azure DevOps.

Jar then downloaded from artifacts by other CI <Artifact downloader does this>


.. code-block:: bash
    # Add code here to explain
