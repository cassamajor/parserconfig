""" Validate responses and conditions for errors. """


def test_load_configuration_file(ParserConfig):
    """ Verify the configuration file loads successfully. """
    ParserConfig.load_configuration_file()
    assert ParserConfig.configuration_file_parser.sections() == ['tutorial']


def test_unload_configuration_file(ParserConfig):
    """ Verify the configuration file can be unloaded. """
    ParserConfig.unload_configuration_file()
    assert not ParserConfig.configuration_file_parser.sections()


def test_credentials_kwargs(ParserConfig):
    """ Verify the credentials method returns the expected value. """
    credentials = ParserConfig.credentials('username', 'password', section='tutorial')
    assert dict(username='my_username', password='my_password') == credentials


def test_credentials_unpack_multiple_values(ParserConfig):
    """ Verify the credentials method returns the expected value. """
    username, password = ParserConfig.credentials('username', 'password', section='tutorial').values()
    assert username == 'my_username'
    assert password == 'my_password'


def test_credentials_unpack_single_value(ParserConfig):
    """ Verify the credentials method returns the expected value. """
    bearer_token, *_ = ParserConfig.credentials('bearer_token', section='tutorial').values()
    assert bearer_token == 'my_bearer_token'
    assert _ == []


def test_credentials_get_single_value(ParserConfig):
    """ Verify the credentials method returns the expected value. """
    credentials = ParserConfig.credentials('bearer_token', section='tutorial')
    assert credentials.get('bearer_token') == 'my_bearer_token'


def test_save_configuration_file(ParserConfig):
    """ Verify modifications made to the configuration file are saved. """
    ParserConfig.configuration_file_parser['tutorial']['example'] = 'my_example'

    ParserConfig.save_configuration_file()
    ParserConfig.unload_configuration_file()
    ParserConfig.load_configuration_file()

    assert ParserConfig.configuration_file_parser.get(section='tutorial', option='example') == 'my_example'
