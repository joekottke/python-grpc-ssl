import argparse
import random
import time

import grpc

from proto import namer_pb2
from proto import namer_pb2_grpc

prefixes = ['Dr.', 'Honorary', 'Judge']
suffixes = ['III', 'II', 'The Great', 'BDFL', 'Esq']
first_names = ['Jim', 'Henry', 'Michael', 'Robert', 'Ronald',
               'Sarah', 'Alison', 'Kimberly', 'Sasha', 'Norma']
last_names = ['Smith', 'Jones', 'Cooper', 'Hunter', 'Baker',
              'Watson', 'Redmond', 'Williams', 'Crick', 'Moore']


def command_arguments():
    parser = argparse.ArgumentParser(description='GRPC-based namer client.')
    parser.add_argument(
        '--host',
        type=str,
        required=True,
        help='The server hostname or address.'
    )
    parser.add_argument(
        '--port',
        type=int,
        required=True,
        help='The server port'
    )
    parser.add_argument(
        '--ca_cert',
        type=str,
        required=False,
        help='CA cert or bundle.'
    )
    parser.add_argument(
        '--client_cert',
        type=str,
        required=False,
        help='Client certificate used for client identification and auth.'
    )
    parser.add_argument(
        '--client_key',
        type=str,
        required=False,
        help='Client certificate key.'
    )
    return parser.parse_args()


def build_client_stub(cli_args):
    cert = None
    key = None
    if cli_args.client_cert:
        cert = open(cli_args.client_cert, 'rb').read()
        key = open(cli_args.client_key, 'rb').read()

    if cli_args.ca_cert:
        ca_cert = open(cli_args.ca_cert, 'rb').read()
        credentials = grpc.ssl_channel_credentials(ca_cert, key, cert)
        channel = grpc.secure_channel(
            cli_args.host + ':' + str(cli_args.port), credentials)
    else:
        channel = grpc.insecure_channel(
            cli_args.host + ':' + str(cli_args.port))

    return namer_pb2_grpc.NamerStub(channel)


def main():
    args = command_arguments()
    stub = build_client_stub(args)

    start_time = time.time()
    for _ in range(1000):
        prefix = None
        suffix = None
        middle = None
        first = random.choice(first_names)
        last = random.choice(last_names)
        if random.randint(0, 1):
            middle = random.choice(first_names)
        if random.randint(0, 1):
            prefix = random.choice(prefixes)
        if random.randint(0, 1):
            suffix = random.choice(suffixes)
        name_request = namer_pb2.NameRequest(
            first_name=first, last_name=last,
            middle_name=middle, prefix=prefix, suffix=suffix
        )
        name_response = stub.EnglishFullName(name_request)
        #print("Got response: '{}'".format(name_response.full_name))
    time_total = time.time() - start_time
    print("Total time: {}\nTotal QPS: {}".format(
        time_total, 1000 / time_total))


if __name__ == '__main__':
    main()
