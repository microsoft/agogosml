MLeap Model Example
============================

This documentation walks the user through an MLeap model app example.
This examples includes:

- Creation of custom transformer in Scala
- Creation of Spark Model
- Serving of the Model


MLeap Custom Transformer
-----------------------------

MLeap supports a range of `transformers
<http://mleap-docs.combust.ml/core-concepts/transformers/support.html>`__,
however as these are limited, so it may be necessary for you to write your
own custom implementation.
We have written a simple example of a custom transformer called `LengthCounter`
which returns the count of words as an `Int` given a `String` input.

The steps to creating a custom transformer are:

    1. Build our core model logic that can be shared between Spark and MLeap
    2. Build the MLeap transformer
    3. Build the Spark transformer
    4. Build bundle serialization for MLeap
    5. Build bundle serialization for Spark
    6. Configure the MLeap Bundle registries with the MLeap and Spark custom transformer

<Federica to add more here>

.. code-block:: bash
    # Add code here to explain


Link to the `MLeap documentation
<https://github.com/combust/mleap-docs/blob/master/mleap-runtime/
custom-transformer.md>`__ on custom transformers.

MLeap Model
----------------

Add more detail here

.. code-block:: bash
    # Add code here to explain



Serving the Model
------------------

Add more detail here

.. code:: bash

  # Add code here to explain


Process of Running Model
-------------------------

<LACE/MARGARET TO ADD MORE HERE>

<HOW TO RUN MANUALLY?!>

Jar file is created by the model and CI/CD pipeline picks up the jar file and dumps
into artifacts in Azure DevOps

Jar then downloaded from artifacts by other CI


