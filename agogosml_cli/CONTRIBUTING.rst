Contributing to the Agogosml CLI
================================

Getting Started
---------------

To get started with the project, it is recommended you install `pipenv <https://pipenv.readthedocs.io/en/latest/>` 
as we use Pipfiles to list dependencies. The project currently requires Python 3.7 (we may add backward compatibility
over time). We do not support Python 2 and nor do we plan on it. 

Installing Dependencies (and Dev Dependencies)
----------------------------------------------

.. code:: bash

    $ cd agogosml_cli/
    $ pipenv install --dev

Running Tests
-------------

.. code:: bash

    $ pipenv run make test

Running Linter
-------------

.. code:: bash

    $ pipenv run make lint
