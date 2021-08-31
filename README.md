# ParserConfig

ParserConfig initializes ConfigParser in fewer lines of code.

## Installation
Requires Python 3.7+:
```shell
python -m pip install parserconfig
```

## Usage
To follow along, create a `settings.ini` file in your home directory with the following content:
```ini
[tutorial]
username = my_username
password = my_password
bearer_token = my_bearer_token
```

The configuration file can be read using the following code:
```python
from pathlib import Path
from parserconfig import ParserConfig

configuration_file = Path.home().joinpath('settings.ini')
settings = ParserConfig(configuration_file=configuration_file)
```

The `credentials` helper method returns a dictionary containing key/value pairs. This can be leveraged in several ways:
```python
credentials = settings.credentials('username', 'password', section='tutorial')
print(f'{credentials = }. Kwargs unpacking is supported via **credentials')

username, password = credentials.values()
print(f'{username = }, {password = }')
```

The pattern for querying a single value varies slightly: 
```python
bearer_token = settings.credentials('bearer_token', section='tutorial')
print(f'{bearer_token = }. Single value also supports kwargs unpacking via **bearer_token')

bearer = bearer_token.get('bearer_token')
print(f'{bearer = }')

token, *_ = bearer_token.values()
print(f'{token = }')
```

Access to [ConfigParser](https://docs.python.org/3/library/configparser.html) is provided via `configuration_file_parser`, and can be used to enable ExtendedInterpolation:
```python
from configparser import ConfigParser, ExtendedInterpolation

settings.configuration_file_parser = ConfigParser(interpolation=ExtendedInterpolation())
settings.load_configuration_file()
```

### Advanced Usage
- [management_api_tools](https://github.com/Fauxsys/management_api_tools.git) uses parserconfig to insert data into pytest during test execution.
- [offprem](https://github.com/Fauxsys/offprem.git) creates subclasses of parserconfig.

## Local Development and Testing
### Development
Development and testing should be done in a virtual environment.
```shell
$ git clone https://github.com/Fauxsys/parserconfig.git
$ cd parserconfig
$ python -m venv venv --prompt parserconfig
$ source venv/bin/activate
(parserconfig) $ python -m pip install -U pip
```
Install parserconfig locally.
```shell
(parserconfig) $ python -m pip install -e ".[test]"
```

### Testing
You can test any changes locally with pytest.
```shell
(parserconfig) $ python -m pytest --cov=parserconfig 
```

You can also test parserconfig as an installed package.
```shell
(parserconfig) $ python -m tox
```

### Building a wheel
```shell
(parserconfig) $ python -m pip install build
(parserconfig) $ python -m build --wheel
```

There should now be a wheel in the `dist` directory.
```shell
(parserconfig) $ ls -1 dist
parserconfig-1.0.0-py3-none-any.whl
```