# TLS authentication in Python gRPC

## Intro

## TLS Basics
![Basic Certificate Hierarchy](certificate-hierarchy-basic.png)

### Chain of Trust, Transitive Trust
![Certificate Panel](certificate-panel.png)

### Root certificate stores

## Generate Certificates

### CFSSL

### Generate CA Certificate and Config
```sh
cd ./ssl
cfssl gencert -initca ca-csr.json | cfssljson -bare ca
```

### Generate Server and Client certificates

Note that the server name in the server certificate needs to be the same as the server name that you connect to. This can be accomplished by setting a name in your `/etc/hosts` file, or by having the name in DNS.

#### Server Certificate

```sh
cd ./ssl
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -hostname='node04.example.com,node.example.com' server-csr.json | cfssljson -bare server
```

#### Client Certificate

```sh
cd ./ssl
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json client-csr.json | cfssljson -bare client
```

## TLS Server Identification and Authentication

### Client trusts the certificate authority cert, thus the server.
This is similar to the browser use-case

This has also been written about by Sandtable [here](https://www.sandtable.com/using-ssl-with-grpc-in-python/).

## TLS Client Identification and Authentication

### Client and Server trust the certificate authority, and therefor, each other