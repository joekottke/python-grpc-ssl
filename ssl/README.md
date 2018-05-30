# SSL setup

## CFSSL

Files in this directory are meant to be used with the CFSSL toolkit, which can be found at the [CFSSL Website](https://cfssl.org/)

## Files

While it is not required for basic testing, it is otherwise assumed that files in this directory will be modified with your own details, particularly the `ca-config.json` and `ca-csr.json` files.

## Generate Certificate Authority

```sh
 cfssl gencert -initca ca-csr.json | cfssljson -bare ca
```

This will generate the files `ca.pem` and `ca-key.pem`. These files will be used to generate the client and server certificates, and the `ca.pem` file will be used to verify the client and server to each other, respectively.

## Generate client certificate

```sh
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json client-csr.json | cfssljson -bare client
```

This will generate the files `client.pem` and `client-key.pem`.

**_Note:_** You will get a warning from this command:

```
[WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
```

As this certificate is to be used for a client, and not a server, it is acceptable that the hosts field is missing.

## Generate server certificate

```sh
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -hostname=<your server hostname> server-csr.json | cfssljson -bare server
```

This will generate the files `server.pem` and `server-key.pem`.
