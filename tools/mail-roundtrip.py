import sys
import argparse
import os
sys.path.insert(0, os.getcwd())
import email
import salmon.encoding
data = sys.stdin.read()


PARSER = argparse.ArgumentParser(description='')
PARSER.add_argument('--no-canonicalize', action='store_false', default=None, dest='canonicalize')
PARSER.add_argument('--python', action='store_true', default=None, help='Use python rather than salmon to roundtrip')
args = PARSER.parse_args()


if args.python:
    message = email.message_from_string(data)
    print(message.as_string())
else:
    if args.canonicalize is not None:
        salmon.encoding.CANONICALIZE_ENCODING = args.canonicalize
    message = salmon.encoding.from_string(data)
    result = salmon.encoding.to_string(message)
    print(result)
