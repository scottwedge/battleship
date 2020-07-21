#!/usr/bin/python3

import sys

"""Try passing parameters to python script
   both required and option parameters
   with default values for each
"""

def main():
    full_command_line = str(sys.argv)
    length = len(sys.argv)

    print("CLI=", full_command_line, length)

    for n in sys.argv:
        print(n)

if __name__ == "__main__":
	main()
