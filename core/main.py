
import sys


def main():
    if sys.version[:3] < '3.6':
        raise TypeError("Expected minimum version({}), "
                        "Got version({})".format(
                         "3.6", sys.version[:3]))
    print("hello bitLabs")

