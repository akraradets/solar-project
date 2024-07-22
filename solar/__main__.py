import argparse
from argparse import RawTextHelpFormatter
import sys
from pathlib import Path


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        message = f"error: {message}\n"
        # sys.stderr.write('error: %s\n' % message)
        eprint(message=message)
        self.print_help()
        sys.exit(1)

def eprint(message:str):
    message = f"\033[01;31m{message}\033[0m"
    print(message, file=sys.stderr)

description = """
Supply the argument `task` as an integer number.
Each interger means the followings.

Task
====
  1: prepare project structure
  2: split tile
"""

parser = MyParser(
    prog="solar-cli",
    description=description,
    formatter_class=RawTextHelpFormatter
    # epilog="Thanks for using %(prog)s! :)",
)

parser.add_argument("task", type=int, help="The specific task you want to run.")
args = parser.parse_args()

task:int = args.task
if(task == 1):
    from solar.prepare_project import run
    # 1: prepare project structure
    # raise NotImplementedError
    run()
elif(task == 2):
    # 2: split tile
    raise NotImplementedError
else:
    # Supply the incorrect interger
    # sys.stderr.write(f"The {task=} is not a valid task number.")
    eprint(f"error: The {task=} is not a valid task number.")
    sys.exit(1)
    # raise ValueError(f"The {task=} is not a valid task number.")
