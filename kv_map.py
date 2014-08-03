import argparse, sys, os, subprocess, struct
from kvtools import kv32_write_item, kv32_iteritems


def main():

  args = parse_args()
  value_path = result_path = None
  if args.bash.find('$VALUE_FILE') != -1:
    value_path = os.path.join(args.temp_dir, "kv-map-pid%d-value" % os.getpid())
  if args.bash.find('$RESULT_FILE') != -1:
    result_path = os.path.join(args.temp_dir, "kv-map-pid%d-result" % os.getpid())

  command = args.bash
  if value_path:
    command = command.replace('$VALUE_FILE', value_path)
  if result_path:
    command = command.replace('$RESULT_FILE', result_path)

  num_items = 0
  for k, v in kv32_iteritems(sys.stdin):
    if value_path is None:
      kwargs = {'stdin': v}
    else:
      kwargs = {}
      with open(value_path, 'wb') as f:
        f.write(v)
    (v2, stderr) = check_communicate(['bash', '-c', command], **kwargs)
    if result_path is not None: 
      with open(result_path, 'rb') as f:
        v2 = f.read()
      os.remove(result_path)
    kv32_write_item(sys.stdout, k, v2)
    num_items += 1

  if num_items > 0:
    if value_path is not None:
      os.remove(result_path)
    if result_path is not None:
      os.remove(result_path)


def parse_args():
  parser = argparse.ArgumentParser(description='Apply a function to the stream.')

  parser.add_argument(
          '--bash', required=True,
           help="""
The command that transforms each value.
All substrings "$VALUE_FILE" will be replaced by the single-quote-escaped temp path for current value. All substrings "$RESULT_FILE" will be replaced by the single-quote-escaped temp path to which the command must write the result. If "$VALUE_FILE" is not a substring of the command, stdin will be used. If "$RESULT_FILE" is not a substring of the command, stdout will be used.""")

  parser.add_argument(
          '--temp-dir', dest='temp_dir', type=verify_dir, help="""
Required iff you use "$VALUE_FILE" or "$RESULT_FILE".
The dir must already exist and its path must not contain "'".
Both requirements are verified.""")

  args = parser.parse_args()

  if (args.temp_dir is not None) and (args.temp_dir.find("'") != -1):
    parser.error("--temp-dir must not contain \"'\".\n")

  if command_uses_temp_dir(args.bash) and (args.temp_dir is None):
    parser.error("--temp-dir is required when you use _FILE magic in your command.\n")

  return args


def command_uses_temp_dir(command):
  return (
    (command.find('$VALUE_FILE') != -1) or
    (command.find('$RESULT_FILE') != -1))


def verify_dir(path):
  if not os.path.isdir(path):
    raise argparse.ArgumentTypeError("%r is not a directory" % path)
  return path


def check_communicate(arr, stdin=None):
  kwargs = {
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE
  }
  if stdin is not None:
    kwargs['stdin'] = subprocess.PIPE
  p = subprocess.Popen(arr, **kwargs)
  (out, err) = p.communicate(stdin)
  assert p.returncode == 0, repr([arr, out, err])
  return (out, err)


if __name__ == '__main__':
  main()
