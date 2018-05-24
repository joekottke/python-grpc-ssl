import argparse
import random

import grpc

import namer_pb2
import namer_pb2_grpc

prefixes = ['Dr.', 'Honorary', 'Judge']
suffixes = ['III', 'II', 'The Great', 'BDFL', 'Esq']
first_names = ['Jim', 'Henry', 'Michael', 'Robert', 'Ronald',
               'Sarah', 'Alison', 'Kimberly', 'Sasha', 'Norma']
last_names = ['Smith', 'Jones', 'Cooper', 'Hunter', 'Baker',
              'Watson', 'Redmond', 'Williams', 'Crick', 'Moore']


def command_arguments():
    parser = argparse.ArgumentParser(description='GRPC-based namer client.')
    parser.add_argument(
        '--port',
        type=int,
        default=31000,
        help='The server port'
    )
    parser.add_argument(
        '--host', type=str, default='127.0.0.1',
        help='The server hostname or address.'
    )
    parser.add_argument(
        '--ca_cert',
        type=str,
        required=True,
        help='CA cert or bundle.'
    )
    parser.add_argument(
        '--client_cert',
        type=str,
        required=True,
        help='Client certificate used for client identification and auth.'
    )
    parser.add_argument(
        '--client_key',
        type=str,
        required=True,
        help='Client certificate key.'
    )
    return parser.parse_args()


def build_client_stub(cli_args):
    ca_cert = open(cli_args.ca_cert).read()
    cert = open(cli_args.client_cert).read()
    key = open(cli_args.client_key).read()
    credentials = grpc.ssl_channel_credentials(ca_cert, key, cert)
    channel = grpc.secure_channel(
        cli_args.host + ':' + str(cli_args.port), credentials)
    return namer_pb2_grpc.NamerStub(channel)


def main():
    args = command_arguments()
    stub = build_client_stub(args)

    for i in xrange(1000):
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
        print("Got response: '{}'".format(name_response.full_name))


if __name__ == '__main__':
    main()
