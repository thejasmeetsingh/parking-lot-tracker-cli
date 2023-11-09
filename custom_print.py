"""
A custom class for printing colorful message to the console
"""


class PPrint:
    DEFAULT = '\033[94m'
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'

    def print_default(self, message):
        print(self.DEFAULT + message)

    def print_success(self, message):
        print(self.SUCCESS + message)

    def print_error(self, message):
        print(self.ERROR + message)
