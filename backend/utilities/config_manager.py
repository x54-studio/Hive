# utilities/config_manager.py
import os
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(key, default=None, required=False):
    """
    Retrieve the value of the environment variable 'key'.

    :param key: The environment variable name.
    :param default: The default value to return if not set.
    :param required: If True, raise an error if the variable is not set.
    :return: The value of the environment variable.
    """
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Environment variable '{key}' is required but not set.")
    return value
