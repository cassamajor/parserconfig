#!/usr/bin/env python3

""" A ConfigParser Overlay. """

from dataclasses import dataclass, field
from configparser import ConfigParser
from pathlib import Path
import logging


@dataclass
class ParserConfig:
    """ Initialize ConfigParser to read from a configuration file. """
    configuration_file: Path
    configuration_file_parser: ConfigParser = field(default_factory=ConfigParser, init=False, repr=False)
    create_configuration_file: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        """ Setup the configuration file. """
        try:
            self.load_configuration_file()
        except AttributeError as error:
            message = f'Expected a pathlib object but received a {type(self.configuration_file).__name__!r}. {error}.'
            raise AttributeError(message) from error
        except IsADirectoryError as error:
            message = f'Expected a file but {self.configuration_file.absolute()} is a directory.'
            raise IsADirectoryError(message) from error
        except FileNotFoundError as error:
            message = f'{self.configuration_file.absolute()} not found on the filesystem.'
            raise FileNotFoundError(message) from error

    def load_configuration_file(self) -> None:
        """ Load the configuration file into ConfigParser. """
        if self.create_configuration_file:
            self.configuration_file.touch()

        self.configuration_file_parser.read_string(string=self.configuration_file.read_text())
        logging.info(f'Loaded {self.configuration_file}')

    def unload_configuration_file(self) -> None:
        """ Initialize an empty ConfigParser. """
        self.configuration_file_parser = ConfigParser()
        logging.info(f'Initialized an empty ConfigParser')

    def save_configuration_file(self) -> None:
        """ Write modifications made to configuration_file_parser to configuration_file. """
        # Open with write access because existing sections/options are already loaded into the parser
        # Using append on a loaded ConfigParser will likely result in DuplicateSectionError
        with self.configuration_file.open('w') as configuration_file:
            self.configuration_file_parser.write(configuration_file)

        logging.info(f'Content written successfully to {self.configuration_file}')

    def credentials(self, *options: str, section: str) -> dict:
        """ Read the configuration file. Return options and values as key pairs. """
        return {option: self.configuration_file_parser.get(section=section, option=option) for option in options}
