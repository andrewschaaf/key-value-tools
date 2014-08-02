import os, ctypes, struct, numpy


def kv32_write_item(f, key, value):
  assert len(key) < 2**32
  assert len(value) < 2**32
  f.write(struct.pack('<ii', len(key), len(value)))
  f.write(key)
  f.write(value)


def kv32_iteritems(f):
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


class EVFile:

  def __init__(self, data):
    self.ev_data = data

  def event_as_matrix(self, event_code, ncols=None, dtype=numpy.dtype('float64')):
    assert ncols is not None
    values_size = kvtool_ev_values_size_for_event(self.ev_data, event_code)
    bytes_per_row = ncols * int(dtype.itemsize)
    nrows = int(values_size / bytes_per_row)
    assert values_size == (nrows * bytes_per_row)
    m = numpy.ones((nrows, ncols), dtype=dtype)
    kvtool_ev_extract_values(self.ev_data, m, event_code)
    return m


_repo_root = '/'.join(os.path.abspath(__file__).split('/')[:-2])
_libkvtools = numpy.ctypeslib.load_library('libkvtools', '%s/build' % _repo_root)


def kvtool_ev_values_size_for_event(data, event_code):
  _libkvtools.kvtool_ev_values_size_for_event.restype = ctypes.c_char_p
  _libkvtools.kvtool_ev_values_size_for_event.argtypes = [
    ctypes.c_void_p,  # ev_data
    ctypes.c_long,    # ev_size
    ctypes.c_long,    # event_code_of_interest
    ctypes.c_void_p
  ]
  values_size = ctypes.c_uint64()
  err = _libkvtools.kvtool_ev_values_size_for_event(
    data, len(data), event_code, ctypes.byref(values_size)
  )
  if err is not None:
    raise Exception(err)
  return values_size.value


def kvtool_ev_extract_values(data, m, event_code):
  _libkvtools.kvtool_ev_extract_values.restype = ctypes.c_char_p
  _libkvtools.kvtool_ev_extract_values.argtypes = [
    ctypes.c_void_p,  # ev_data
    ctypes.c_long,    # ev_size
    ctypes.c_long,    # event_code_of_interest
    numpy.ctypeslib.ndpointer(dtype=m.dtype),
    ctypes.c_long     # values_size
  ]
  err = _libkvtools.kvtool_ev_extract_values(
    data, len(data), event_code, m, m.nbytes
  )
  if err is not None:
    raise Exception(err)
