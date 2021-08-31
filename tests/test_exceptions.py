""" Validate responses and conditions for errors. """

import re

import pytest

from parserconfig import ParserConfig
from conftest import configuration_file_exceptions


def escape(message):
    """
    To match a literal string that may contain special characters, the pattern can first be escaped with re.escape.
    """
    return re.escape(pattern=message)


@pytest.mark.parametrize(argnames='exception, configuration_file, error_message', argvalues=configuration_file_exceptions())
@pytest.mark.parametrize(argnames='create_configuration_file', argvalues=[True, False], ids=repr)
def test_exceptions(exception, configuration_file, error_message, create_configuration_file):
    """
    When the configuration file is not a Pathlib object, raise AttributeError.
    When the configuration file is a Pathlib object, but it is a directory, raise IsADirectoryError.
    """

    with pytest.raises(exception) as error:
        ParserConfig(configuration_file=configuration_file, create_configuration_file=create_configuration_file)

    assert error.match(regexp=escape(message=error_message))


def test_file_not_found(configuration_file_does_not_exist):
    """ When the configuration file is a Pathlib object, but not found on the filesystem, raise FileNotFoundError. """
    with pytest.raises(FileNotFoundError) as error:
        ParserConfig(configuration_file=configuration_file_does_not_exist)

    message = f'{configuration_file_does_not_exist.absolute()} not found on the filesystem.'
    assert error.match(regexp=escape(message=message))
