import os
import sys
import pkgutil
import argparse

from architect import __version__
from architect.exceptions import (
    BaseArchitectError,
    CommandNotProvidedError,
    CommandError,
    CommandArgumentError
)

commands = {}

for _, name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    commands[name] = {'module': __import__('architect.commands.{0}'.format(name), fromlist=['architect.commands'])}


class ArgumentParser(argparse.ArgumentParser):
    def result(self, message):
        """Prints command execution result in a common format"""
        self._print_message('{0}: result: {1}\n'.format(self.prog, str(message)), sys.stdout)

    def error(self, message):
        """Redefines some of argparse's error messages to be more friendly"""
        commands_list = commands.keys()

        if 'too few arguments' in message:
            message = str(CommandNotProvidedError(allowed=commands_list))
        elif 'invalid choice' in message and ', '.join(map(repr, commands_list)) in message:
            message = str(CommandError(current=message.split("'")[1], allowed=commands_list))
        elif 'unrecognized arguments' in message:
            command = [cmd for cmd in sys.argv[1:] if not cmd.startswith('-')][0]
            command_arguments = []

            for args in commands[command]['module'].arguments:
                arg = list(args.keys())[0]
                command_arguments.append('{0} ({1})'.format(arg[1], arg[0]))

            message = str(CommandArgumentError(current=message.split(': ')[1], allowed=command_arguments))

        self.exit(2, '{0}: error: {1}\n'.format(self.prog, message[:1].lower() + message[1:]))


def main():
    """Initialization function for all commands"""
    parser = ArgumentParser(prog='architect')
    parser.add_argument('-v', '--version', action='version', version='Architect {0}'.format(__version__))

    subparsers = parser.add_subparsers(title='commands', help='run one of the commands for additional functionality')

    for command in commands:
        commands[command]['parser'] = subparsers.add_parser(
            command,
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=100)
        )

        for argument in commands[command]['module'].arguments:
            for names, options in argument.items():
                commands[command]['parser'].add_argument(*names, **options)

        commands[command]['parser'].set_defaults(func=commands[command]['module'].run)

    args = parser.parse_args()

    # Starting from Python 3.3 the check for empty arguments was removed
    # from argparse for some strange reason, so we have to emulate it here
    try:
        command = args.func.__module__.split('.')[-1]
    except AttributeError:
        parser.error('too few arguments')

    try:
        commands[command]['parser'].result(args.func(vars(args)))
    except BaseArchitectError as e:
        commands[command]['parser'].error(str(e))
