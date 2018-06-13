resources(
  name='ssl-resources',
  sources=globs('ssl/*pem')
)

python_library(
  name='namer-grpc',
  sources=['namer_pb2.py', 'namer_pb2_grpc.py' ]
)

python_library(
  name='namer-library',
  sources='namer.py'
)

python_binary(
  name='namer-server',
  source='server.py',
  zip_safe=False,
  dependencies = [
    ':namer-library',
    ':namer-grpc',
    ':ssl-resources',
    ':protobuf',
    ':grpcio'
  ],
)

python_requirements(
  requirements_relpath='../requirements.txt'
)
