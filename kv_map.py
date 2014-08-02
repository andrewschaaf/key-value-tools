import sys, subprocess, struct


def main():
  bash_command = sys.argv[1]
  for (k, v) in iteritems(sys.stdin):
    (v2, stderr) = check_communicate(['bash', '-c', bash_command], stdin=v)
    write_item(sys.stdout, k, v2)


def write_item(f, key, value):
  assert len(value) < 2**32
  f.write(struct.pack('<ii', len(key), len(value)))
  f.write(key)
  f.write(value)


def iteritems(f):
  while True:
    sizes = f.read(8)
    if len(sizes) == 0:
      return
    assert len(sizes) == 8
    key_size, value_size = struct.unpack('<ii', sizes)
    key = f.read(key_size)
    value = f.read(value_size)
    assert len(key) == key_size
    assert len(value) == value_size
    yield (key, value)


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
