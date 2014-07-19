import subprocess


def main():

  kv32 = read_data('foo.kv32')
  check_communicate(['mkdir', '-p', 'temp'])
  check_communicate(['rm', '-rf', 'temp'])
  check_communicate(['mkdir', '-p', 'temp'])

  (out, err) = check_communicate(['../build/kv32-to-leveldb', 'temp'], stdin=kv32)
  assert out == ''
  assert err == ''

  (out, err) = check_communicate(['../build/leveldb-to-kv32', 'temp'])
  assert out == kv32
  assert err == ''

  print 'OK'


def read_data(path):
  with open(path, 'rb') as f:
    return f.read()


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
