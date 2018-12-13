MLeap Model Example
============================

This documentation walks the user through an MLeap model app example.

This examples includes:

- Training and serializing ML Model with Spark and MLeap
- Training model on Azure Databricks
- Creation of Custom Transformer for MLeap in Scala
- Serving the Model

Requirements to Run Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `azure-cli 2.0 <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest>`__
-  `Java 8 <https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html>`__
-  `scala 2.11 <https://www.scala-lang.org/>`__
-  `sbt 1.2.1 <https://www.scala-sbt.org/>`__
-  `Apache Spark > 2.3 <https://spark.apache.org/>`__
-  `mleap > 0.12.0 <https://github.com/combust/mleap>`__
-  `jq <https://stedolan.github.io/jq/download/>`__


Train and serialize ML Model with Spark and MLeap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MLeap provides functionality to serialize trained pipelines and algorithms to a ``BundleFile`` which can then easily be loaded back into a lightweight MLeap runtime for scoring without Spark dependencies. Our example implements a pipeline with a trained model and a simple custom transformer.

`ModelTrainer <mleap_model/trainer/src/main/scala/com/Microsoft/agogosml/mleap_model_trainer/ModelTrainer.scala>`__ contains our model training code for training on a Spark cluster. This imports the custom transformer ``LengthCounter``. The Spark model is a simple classification model on the `Spam or Ham` dataset which is then serialized as an MLeap ``BundleFile`` and saved as a ``jar``.

`ModelTrainerApp <mleap_model/trainer/src/main/scala/com/Microsoft/agogosml/mleap_model_trainer/ModelTrainerApp.scala>`__ executes the training of the Spark model in a Spark session (locally or on a cluster).

Train model on Azure Databricks
--------------------------------------

While this model can be trained with a local installation of Spark due to the limited size of the dataset, an appropriate cluster would be required if training with much larger production datasets. This solution comes with automated deployment scripts to easily train the model on `Azure Databricks <https://azure.microsoft.com/en-au/services/databricks/>`__, a managed Apache Spark platform which can easily scale to handle very large Spark workloads.

Running the deployment scripts will:

1. Deploy an Azure Databricks workspace and Azure Blob storage with a container called ``databricks``, mounted on DBFS within Azure Databricks.
2. Upload SMSSpamCollection.tsv dataset to blob storage.
3. Rebuild the ModelTrainer JAR file locally with ``sbt clean assembly`` and upload this JAR to blob storage.
4. Create a two node Spark cluster on Azure Databricks with the necessary packages installed, along with ModelTrainer JAR.
5. Upload necessary Databricks notebooks to train the model on Azure Databricks.


To deploy ModelTrainer on Azure Databricks:

1. Ensure you have the necessary pre-requisites.
2. cd into the `mleap_model <mleap_model/>`__ folder.
3. Run: ``make deploy`` to deploy the solution. Alternatively, run ``make deploy_w_docker`` to avoid installing pre-requisites. This will build and run a docker container locally with the necessary pre-requisites. The deployment will prompt for the following:
    - Azure Resource Group
    - Data center location
    - Azure Subscription
    - `Databricks workspace url and access token <https://docs.azuredatabricks.net/api/latest/authentication.html#token-management>`__
4. After the deployment has completed, in the Azure Portal, navigate to the newly deployed Azure Databricks workspace. 
5. Open the **agogos > 02_train_model notebook**. Run the notebook to train and serialize the model blob storage (mounted via DBFS).


MLeap Custom Transformer
-----------------------------

MLeap supports a range of `transformers
<http://mleap-docs.combust.ml/core-concepts/transformers/support.html>`__, however as these are limited, so it may be necessary for you to write your own custom implementation. We have written a simple example of a custom transformer called ``LengthCounter`` which returns the count of words as an ``Int`` given a ``String`` input.

There are a number of `standard steps <https://github.com/combust/mleap-docs/blob/master/mleap-runtime/ custom-transformer.md>`__  for creating a custom transformer in the MLeap docs. The steps to creating a custom transformer are:


1. Core Model
_______________
`LengthCounterModel <mleap_model/trainer/custom_transformer/src/main/scala/ml/combust/mleap/core/feature/LengthCounterModel.scala>`__ defines the inputs and outputs of the transformer.


2. MLeap Transformer
_____________________
`LengthCounter <mleap_model/trainer/custom_transformer/src/main/scala/ml/combust/mleap/runtime/transformer/feature/LengthCounter.scala>`__ inherits from the transformer base class but allows us to pass in our transformer by redefining the ``UserDefinedFunction``. The ``LengthCounterModel`` is passed as an input to the ``LengthCounter``.


3. Spark Transformer
_____________________
`LengthCounter <mleap_model/trainer/custom_transformer/src/main/scala/org/apache/spark/ml/mleap/feature/LengthCounter.scala>`__ is a spark transformer that knows how to execute against a Spark DataFrame (just as you would write a custom Spark transformer)

There is an important method within this class:

- ``transform``: applies the LengthCounterModel within the ``transform`` method.


4. MLeap Serialization
_________________________
`LengthCounterOp <mleap_model/trainer/custom_transformer/src/main/scala/ml/combust/mleap/bundle/ops/feature/LengthCounterOp.scala>`__ defines how we serialize and deserialize our model and transformer to/from an MLeap ``BundleFile``.

There are two important methods within this class:

-  ``store``: defines how the transformer is stored
-  ``load``:  defines what how the transformer is loaded

5. Spark Serialization
_______________________
`LengthCounterOp <mleap_model/trainer/custom_transformer/src/main/scala/org/apache/spark/ml/bundle/extension/ops/feature/LengthCounterOp.scala>`__  defines how we serialize and deserialize the custom Spark transformer to/from MLeap.


6. MLeap Registry & Spark Registry
____________________________________
The custom transformer needs to be added to the MLeap registry and the Spark registry with a `reference.conf <mleap_model/trainer/custom_transformer/src/main/resources/reference.conf>`__ file in our project.



Serving the Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~

An HTTP server is used to access the MLeap model in production. The server receives incoming data with a `POST` request and feeds it as input to the model. Finally, it receives the model prediction and pushes it, along with any other desired data, through the pipeline to the output. Please refer to our `design documents <https://github.com/Microsoft/agogosml/blob/master/docs/DESIGN.rst>`_ for more details.

Running this sample application locally with Docker is documented in our `developer guide <https://github.com/Microsoft/agogosml/blob/master/docs/DEVELOPER_GUIDE.rst>`_, with a couple of additional steps. First ensure that the mleap model is manually placed in the ``mleap_serving/assets`` directory. If your model requires a custom transformer, ensure that the ``jar`` file for the custom transformer is located in the ``mleap_serving/lib/`` directory.

.. code:: bash

    docker run -e PORT=5000
             -e OUTPUT_URL=
             -e MODEL_PATH=/app/sample_model.zip 
             -p 5000:5000

While these steps are necessary for running locally, in production, the model and jar files are picked up via a build pipeline and placed into the correct folders before the sample app runs.

With the app running on the specified port, send a POST request containing JSON data that follows the schema your model expects.

