#!/usr/bin/python3

import sys

"""Try passing parameters to python script
   both required and option parameters
   with default values for each
"""

def handle_args(s):
    cli = s
    length = len(s)
    return (cli, length)


def main():
    (cli, length) = handle_args(sys.argv)

    print("CLI=", cli, length)

    for n in cli:
        print(n)

if __name__ == "__main__":
	main()
