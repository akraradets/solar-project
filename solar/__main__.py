import argparse
import sys
from pathlib import Path


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(
    prog="solar-cli",
    description="This is the CLI section of the Solar Project",
    # epilog="Thanks for using %(prog)s! :)",
)

parser.add_argument("task", type=int)
args = parser.parse_args()

# target_dir = Path(args.path)

# if not target_dir.exists():
#     print("The target directory doesn't exist")
#     raise SystemExit(1)

# for entry in target_dir.iterdir():
#     print(entry.name)
