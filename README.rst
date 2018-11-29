Agogosml
========

+------------+------------------------------------------+
|            | Status                                   |
+============+==========================================+
| Agogosml   | |Build status1| |Documentation status1|  |
+------------+------------------------------------------+
| CLI        | |Build status2| |Documentation status2|  |
+------------+------------------------------------------+


.. |Build status1| image:: https://dev.azure.com/csedevil/agogosml/_apis/build/status/agogosml-CI
   :target: https://dev.azure.com/csedevil/agogosml/_build/latest?definitionId=37
.. |Build status2| image:: https://dev.azure.com/csedevil/agogosml/_apis/build/status/CLI-CI%20(master)
   :target: https://dev.azure.com/csedevil/agogosml/_build/latest?definitionId=32

.. |Documentation status1| image:: https://readthedocs.org/projects/agogosml/badge/?version=latest
    :target: https://agogosml.readthedocs.io/en/latest/?badge=latest
    :alt: Agogosml Library Documentation Status

.. |Documentation status2| image:: https://readthedocs.org/projects/agogosml_cli/badge/?version=latest
    :target: https://agogosml_cli.readthedocs.io/en/latest/?badge=latest
    :alt: Agogosml CLI Documentation Status

Agogosml is a data processing pipeline project that addresses the common
need for operationalizing ML models. This covers the complete workflow
of training, deploying, scoring and monitoring the models in production
at scale.


Features
--------

-  Re-usable/canonical data processing pipeline supporting multiple data streaming technologies (Kafka and Azure EventHub) and deployment to Kubernetes.
-  CI/CD pipeline using Azure DevOps to deploy versioned and immutable pipeline.
-  Blue/Green deployments, automatic role-backs or redeployment of a specific version.

Quick Install & Run
-------------------

The following quick install instructions assumes you have the azure-cli, Python 3.7, Docker and Terraform installed.

.. code-block:: bash

   # 1. Installing the CLI
    pip install agogosml_cli

    # 2. Create a directory for your project
    mkdir hello-agogosml
    cd hello-agogosml

    # 3. Init the project
    agogosml init

    # 4. Fill in the manifest.json (Docker Container Registry, Azure Subscription, etc).
    vi manifest.json

    # 5. Generate the code for the projects
    agogosml generate

The generated folder structure consists of the input reader, customer app and output writer as well as the Azure DevOps pipelines for CI/CD.

For more detailed information, see the `User Guide <./docs/USER_GUIDE.rst>`__

Architecture
------------

The agogosml package was developed to provide a Data Engineer with a simple
configurable data pipeline consisting of three components: an input reader,
app (that holds a trained ML model) and an output writer. The three
components are instrumented using one Docker container per component.

Input Reader
~~~~~~~~~~~~
The input reader acts as the data receiver and obtains the data required as
input for the ML model. The package supports both Kafka and EventHub.


Output Writer
~~~~~~~~~~~~~
The output writer receives the scored data from the app and sends it onto
a streaming client (a Kafka or Eventhub instance).


App
~~~
The app receives data from the input reader and feeds it to the ML model
for scoring. Once scored the data is sent onto the output writer.

For more information about the design, see the `Design Documentation <./docs/DESIGN.rst>`__


Links
-----

-  `User Guide - Getting Started <./docs/USER_GUIDE.rst>`__
-  `Developer Guide <./docs/DEVELOPER_GUIDE.rst>`__
-  `License <./LICENSE>`__
-  `Microsoft Open Source Code of Conduct <https://opensource.microsoft.com/codeofconduct/>`__
-  `Backlog <https://dev.azure.com/csedevil/agogosml/_workitems/recentlyupdated>`__
-  `Design and Architecture <./docs/DESIGN.rst>`__

Contributing
------------

This project welcomes contributions and suggestions. Most contributions
require you to agree to a Contributor License Agreement (CLA) declaring
that you have the right to, and actually do, grant us the rights to use
your contribution. For details, visit `https://cla.microsoft.com`_.

When you submit a pull request, a CLA-bot will automatically determine
whether you need to provide a CLA and decorate the PR appropriately
(e.g., label, comment). Simply follow the instructions provided by the
bot. You will only need to do this once across all repos using our CLA.

This project has adopted the `Microsoft Open Source Code of Conduct`_.
For more information see the `Code of Conduct FAQ`_ or contact
opencode@microsoft.com with any additional questions or comments.

.. _`https://cla.microsoft.com`: https://cla.microsoft.com
.. _Microsoft Open Source Code of Conduct: https://opensource.microsoft.com/codeofconduct/
.. _Code of Conduct FAQ: https://opensource.microsoft.com/codeofconduct/faq/
