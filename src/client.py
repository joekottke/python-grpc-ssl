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

channel = grpc.insecure_channel('localhost:454545')

stub = namer_pb2_grpc.NamerStub(channel)

for i in xrange(1000):
  first = first_names[random.randint(0,9)] 
  last = last_names[random.randint(0,9)] 
  name_request = namer_pb2.NameRequest(first_name=first, last_name=last)
  name_response = stub.EnglishFullName(name_request)
  print("Got response: '{}'".format(name_response.full_name))
