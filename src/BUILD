python_library(
  name='namer-grpc',
  sources=globs('proto/*.py')
)

python_library(
  name='namer-library',
  sources='namer.py'
)

python_binary(
  name='namer-client',
  source='client.py',
  dependencies = [
    ':namer-grpc',
    ':protobuf',
    ':grpcio'
  ],
)
python_binary(
  name='namer-server',
  source='server.py',
  dependencies = [
    ':namer-library',
    ':namer-grpc',
    ':protobuf',
    ':grpcio'
  ],
)

python_requirements(
  requirements_relpath='../requirements.txt'
)
