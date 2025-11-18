import argparse
import random
import time
from concurrent import futures

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
    parser.add_argument(
        '--max_workers',
        type=int,
        default=50,
        help='Number of concurrent workers for requests (default: 50)'
    )
    parser.add_argument(
        '--num_requests',
        type=int,
        default=1000,
        help='Number of requests to make (default: 1000)'
    )
    return parser.parse_args()


def build_client_stub(cli_args):
    cert = None
    key = None
    if cli_args.client_cert:
        cert = open(cli_args.client_cert, 'rb').read()
        key = open(cli_args.client_key, 'rb').read()

    # gRPC channel options for better performance
    options = [
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),
        ('grpc.keepalive_time_ms', 10000),
        ('grpc.keepalive_timeout_ms', 5000),
        ('grpc.http2.max_pings_without_data', 0),
        ('grpc.http2.min_time_between_pings_ms', 10000),
    ]

    if cli_args.ca_cert:
        ca_cert = open(cli_args.ca_cert, 'rb').read()
        credentials = grpc.ssl_channel_credentials(ca_cert, key, cert)
        channel = grpc.secure_channel(
            cli_args.host + ':' + str(cli_args.port), credentials, options=options)
    else:
        channel = grpc.insecure_channel(
            cli_args.host + ':' + str(cli_args.port), options=options)

    return namer_pb2_grpc.NamerStub(channel)


def make_request(stub):
    """Make a single name request to the server."""
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
    return name_response.full_name


def main():
    args = command_arguments()
    stub = build_client_stub(args)

    start_time = time.time()

    # Use ThreadPoolExecutor for concurrent requests
    with futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        future_to_request = {executor.submit(make_request, stub): i
                            for i in range(args.num_requests)}

        completed = 0
        for future in futures.as_completed(future_to_request):
            try:
                full_name = future.result()
                completed += 1
                #print("Got response: '{}'".format(full_name))
            except Exception as exc:
                print('Request generated an exception: {}'.format(exc))

    time_total = time.time() - start_time
    print("Total time: {}\nTotal QPS: {}\nCompleted: {}/{}".format(
        time_total, args.num_requests / time_total, completed, args.num_requests))


if __name__ == '__main__':
    main()
