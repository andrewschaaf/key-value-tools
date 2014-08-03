import sys, subprocess, struct
from kvtools import kv32_iteritems


def main():
  for k, v in kv32_iteritems(sys.stdin):
    sys.stdout.write(k + "\n")


if __name__ == '__main__':
  main()
