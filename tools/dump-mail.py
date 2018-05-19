
import sys, os
import asyncore
import sys
import time
sys.path.insert(0, os.getcwd())


import argparse
import threading
import salmon
from salmon.routing import route, route_like, stateless, Router
import salmon.server
import logging
import salmon.encoding

LOGGER = logging.getLogger()



PARSER = argparse.ArgumentParser(description='Receive and set mail')
PARSER.add_argument('--port', type=str, default=1025)
PARSER.add_argument('--host', type=str, default='localhost')
PARSER.add_argument('--dump-dir', type=str, help='Write raw emails to this file')
PARSER.add_argument('--debug', action='store_true', help='Print debug output')

dump_dir = None
def main():
    global dump_dir
    args = PARSER.parse_args()
    dump_dir = args.dump_dir

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    receiver = salmon.server.SMTPReceiver(args.host, args.port)
    Router.load(["__main__"])
    LOGGER.debug('Starting server...')
    receiver.start()

    try:
        while True:
            line = sys.stdin.readline()
            if line == '':
                break
    finally:
        asyncore.close_all()
    LOGGER.debug('Exiting')




@route("(address)@(host)", address=".+", host=".+")
@stateless
def receive(message, address=None, host=None):
    message_text = salmon.encoding.to_string(message.base)
    if dump_dir is not None:
        output_file = os.path.join(dump_dir, str(time.time()))
        with open(output_file, 'w') as stream:
             stream.write(message_text)
        print 'Received mail. Written to:', output_file
    else:
        sys.stdout.write(message_text)



if __name__ == '__main__':
    main()
