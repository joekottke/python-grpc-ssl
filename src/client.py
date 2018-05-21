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
        help='The server hostname or address'
    )
    parser.add_argument(
        '--use_tls',
        action='store_true',
        help='Enable TLS Connectivity'
    )
    parser.add_argument(
        '--ca_cert',
        type=str,
        help='CA cert or bundle.'
    )
    return parser.parse_args()


def build_client_stub(cli_args):
    if cli_args.use_tls:
        if cli_args.ca_cert:
            root_certs = open(cli_args.ca_cert).read()
        else:
            root_certs = None
        credentials = grpc.ssl_channel_credentials(root_certs)
        channel = grpc.secure_channel(
            cli_args.host + ':' + str(cli_args.port), credentials)
    else:
        channel = grpc.insecure_channel(
            cli_args.host + ':' + str(cli_args.port))
    return namer_pb2_grpc.NamerStub(channel)


def main():
    args = command_arguments()
    stub = build_client_stub(args)

    for i in xrange(1000):
        prefix = None
        suffix = None
        middle = None
        first = first_names[random.randint(0, 9)]
        last = last_names[random.randint(0, 9)]

        if random.randint(0, 1):
            middle = first_names[random.randint(0, 9)]

        if random.randint(0, 1):
            prefix = prefixes[random.randint(0, 2)]

        if random.randint(0, 1):
            suffix = suffixes[random.randint(0, 4)]

        name_request = namer_pb2.NameRequest(
            first_name=first, last_name=last,
            middle_name=middle, prefix=prefix, suffix=suffix
        )

        name_response = stub.EnglishFullName(name_request)
        print("Got response: '{}'".format(name_response.full_name))

if __name__ == '__main__':
    main()
