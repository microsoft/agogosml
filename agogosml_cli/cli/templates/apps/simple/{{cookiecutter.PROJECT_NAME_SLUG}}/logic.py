"""
Implements the business logic for {{cookiecutter.PROJECT_NAME_SLUG}}.

Overwrite the sample implementation in this file with your own requirements.
The framework expects a function named `transform` to be present in this
module but helper functions may be added at your convenience.
"""


def transform(data: dict) -> dict:
    """
    Apply the required transformations to the input data.

    The input data for this function is guaranteed to follow the specification
    provided to the framework. Consult `data.spec.yaml` for an example.

    Args:
      data: input object to transform

    >>> transform({'intValue': 100})
    {'intValue': 200}
    """
    data['intValue'] += 100
    return data
