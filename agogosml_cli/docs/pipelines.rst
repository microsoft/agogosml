Using the generated Build & Release pipelines
=============================================

Prerequisites
-------------

-  Run the CLI generator. The expected output should be 3 json files
   representing 2 build azure devops pipelines:

   -  agogosml build
   -  application build

-  The third json represent the Releast pipeline
-  Import all three files to Azure devops, save the imported pipelines.

|Builds| |Release|

Creating a new build
--------------------

This will be done via the already defined triggers. Whenever a new PR is
made a build will be triggered, creating a new image and pushing it to
the containers registry

|build example|

Defining a new release candidate
--------------------------------

Create a new release |image3| Fill in mandatory paramaters |image4|
Click on 'Deploy chart', the first step |image5| Click 'Deploy' |image6|
Verify info and click 'Deploy' |image7|

.. |Builds| image:: ./_static/import-builds.png
.. |Release| image:: ./_static/import-release.png
.. |build example| image:: ./_static/build-example.png
.. |image3| image:: ./_static/release-1.png
.. |image4| image:: ./_static/release-2.png
.. |image5| image:: ./_static/release-3.png
.. |image6| image:: ./_static/release-4.png
.. |image7| image:: ./_static/release-5.png