import os, sys, subprocess
import numpy


REPO_ROOT = '/'.join(os.path.abspath(__file__).split('/')[:-2])
BUILD_DIR = "%s/build" % REPO_ROOT


def main():

  check_communicate(['mkdir', '-p', 'temp'])
  check_communicate(['rm', '-rf', 'temp'])
  check_communicate(['mkdir', '-p', 'temp'])

  test_kv32_tools()
  test_ev_tools()
  test_python_library()

  print 'OK'


def test_kv32_tools():
  foo_kv32 = read_data('foo.kv32')
  (out, err) = check_communicate(['%s/kv32-to-leveldb' % BUILD_DIR, 'temp'], stdin=foo_kv32)
  assert out == ''
  assert err == ''
  (out, err) = check_communicate(['%s/leveldb-to-kv32' % BUILD_DIR, 'temp'])
  assert out == foo_kv32
  assert err == ''
  (out, err) = check_communicate(['%s/bin/kv-map' % REPO_ROOT, 'wc'], stdin=foo_kv32)
  assert out == read_data('foo-wc.kv32')
  assert err == ''


def test_ev_tools():
  (out, err) = check_communicate([
                                  '%s/ev-values' % BUILD_DIR,
                                  '-k', '127',
                                  '%s/test/foo.ev' % REPO_ROOT])
  assert out == 'abcdef123'
  assert err == ''


def test_python_library():
  sys.path.append('%s/python' % REPO_ROOT)
  from kvtools import EVFile

  m = EVFile('').event_as_matrix(123, ncols=3)
  assert m.shape == (0, 3)

  float_zero = '\x00' * 4
  float_one = '\x00\x00\x80\x3F'
  row = chr(123) + chr(8) + float_zero + float_one
  m = EVFile(row * 3).event_as_matrix(123, ncols=2, dtype=numpy.dtype('float32'))
  assert m.shape == (3, 2)
  for i in range(3):
    assert m[i, 0] == 0
    assert m[i, 1] == 1

  assert_raises(
            "unexpected EOF after event code",
            lambda: EVFile('\x01').event_as_matrix(123, ncols=3))

  EVFile('\x01\x00').event_as_matrix(123, ncols=3)

  assert_raises(
            "unexpected EOF after value size",
            lambda: EVFile('\x01\x03xy').event_as_matrix(123, ncols=3))


def assert_raises(message, f):
  try:
    f()
  except Exception as e:
    assert str(e) == message
    return
  raise Exception("Expected exception: %s" % repr(message))


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
