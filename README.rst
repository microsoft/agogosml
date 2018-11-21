Agogosml
========

+------------+-----------------+
|            | Status          | 
+============+=================+
| Framework  | |Build status1| |
+------------+-----------------+
| CLI        | |Build status2| |
+------------+-----------------+


.. |Build status1| image:: https://dev.azure.com/csedevil/agogosml/_apis/build/status/agogosml-CI
   :target: https://dev.azure.com/csedevil/agogosml/_build/latest?definitionId=37
.. |Build status2| image:: https://dev.azure.com/csedevil/agogosml/_apis/build/status/CLI-CI%20(master)
   :target: https://dev.azure.com/csedevil/agogosml/_build/latest?definitionId=32

agogosml is a data processing pipeline project that addresses the common
need for operationalizing ML models. This covers the complete workflow
of training, deploying, scoring and monitoring the models in production
at scale. 


Features
========

-  Re-usable/canonical data processing pipeline supporting multiple data streaming technologies (Kafka and Azure EventHub) and deployment to Kuberentes.
-  CI/CD pipeline using Azure DevOps to deploy versioned and immutable pipeline.
-  Blue/Green deployments, automatic role-backs or redeployment of a specific version.


Roadmap
=======

-  Dashboard to explore real-time and historical model input, predictions and performance
-  Model monitoring to detect unexpected changes in input data and predictions
-  Triggers to take actions if input or predictions diverge from expected ranges
-  Anonymize/remove PII data and keep track of PII data used for model training
-  Revoke and retrain models if certain records need to be removed due to customers that want their data revoked


Quick Links
===========

-  `Getting Started <./docs/GETTING_STARTED.md>`__
-  `Contributing / Developer guide <./CONTRIBUTING.rst>`__
-  `License <./LICENSE>`__
-  `Microsoft Open Source Code of Conduct <https://opensource.microsoft.com/codeofconduct/>`__
-  `Backlog <https://dev.azure.com/csedevil/agogosml/_workitems/recentlyupdated>`__
-  `Design and Architecture <./docs/DESIGN.md>`__


Contributing
============

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