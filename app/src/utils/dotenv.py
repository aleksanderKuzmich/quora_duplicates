import os
from dotenv import find_dotenv, dotenv_values


def load_env_variables():
    dotenv_path = find_dotenv()
    if dotenv_path:
        env_settings = dotenv_values(dotenv_path)
    else:
        env_settings = os.environ
    return env_settings
