from inspect import cleandoc
from pathlib import Path

import pytest

from parserconfig import ParserConfig


def configuration_file_exceptions():
    configuration_file_is_a_directory = Path.home()
    directory_error = f'Expected a file but {configuration_file_is_a_directory.absolute()} is a directory.'

    configuration_file_is_not_a_pathlib_object = 'settings.ini'
    attribute_error = f'Expected a pathlib object but received a {type(configuration_file_is_not_a_pathlib_object).__name__!r}.'

    return (
        [IsADirectoryError, configuration_file_is_a_directory, directory_error],
        [AttributeError, configuration_file_is_not_a_pathlib_object, attribute_error]
    )


@pytest.fixture()
def configuration_file_does_not_exist(tmp_path):
    configuration_file = tmp_path.joinpath('settings.ini')
    return configuration_file


@pytest.fixture()
def configuration_file(tmp_path):
    configuration_file = tmp_path.joinpath('settings.ini')
    configuration_file_content = cleandoc(doc="""
                                          [tutorial]
                                          username = my_username
                                          password = my_password
                                          bearer_token = my_bearer_token
                                          """)
    configuration_file.write_text(configuration_file_content)

    return configuration_file


@pytest.fixture(name='ParserConfig')
def loaded_parser(configuration_file):
    return ParserConfig(configuration_file=configuration_file)
