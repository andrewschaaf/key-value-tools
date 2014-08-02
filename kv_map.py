import sys, subprocess, struct
from kvtools import kv32_write_item, kv32_iteritems


def main():
  bash_command = sys.argv[1]
  for k, v in kv32_iteritems(sys.stdin):
    (v2, stderr) = check_communicate(['bash', '-c', bash_command], stdin=v)
    kv32_write_item(sys.stdout, k, v2)


def check_communicate(arr, stdin=None):
  kwargs = {
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE
  }
  if stdin is not None:
    kwargs['stdin'] = subprocess.PIPE
  p = subprocess.Popen(arr, **kwargs)
  (out, err) = p.communicate(stdin)
  assert p.returncode == 0, repr([out, err])
  return (out, err)


if __name__ == '__main__':
  main()
