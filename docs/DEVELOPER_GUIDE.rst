Developer Guide
===============

We love pull requests from everyone. By participating in this project,
you agree to abide by the `Microsoft Open Source Code of
Conduct <https://opensource.microsoft.com/codeofconduct/>`__




Setting up the Agogosml Library for Development
-----------------------------------------------



Setting up the CLI for Development
----------------------------------

agogosml_cli is a cli tool developed with Python using the
`Click\_ <https://click.palletsprojects.com/en/7.x/>`__ in combination
with `cookiecutter <https://github.com/audreyr/cookiecutter>`__. 

To get started with the project, it is recommended you install `pipenv <https://pipenv.readthedocs.io/en/latest/>` 
as we use Pipfiles to list dependencies. The project currently requires Python 3.7 (we may add backward compatibility
over time). We do not support Python 2 and nor do we plan on it. 

Installing Dependencies (and Dev Dependencies):

.. code:: bash

    $ cd agogosml_cli/
    $ pipenv install --dev

Running Tests:

.. code:: bash

    $ pipenv run make test

Running Linter:

.. code:: bash

    $ pipenv run make lint



Before Submitting a PR to the Project
-------------------------------------

Make sure the tests pass

Make your change. Add tests for your change. Make the tests pass

Push to your fork and `submit a pull
request <https://github.com/Microsoft/agogosml/pulls>`__.


At this point you’re waiting on us. We like to at least comment on pull
requests within three business days (and, typically, one business day).
We may suggest some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is
accepted:

-  Write tests.
-  Follow our `engineering
   playbook <https://github.com/Microsoft/code-with-engineering-playbook>`__
-  Write a `good commit
   message <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`__.
