# openssh-key-v1 format

Description of the `openssh-key-v1` on-disk format.

## 1. Base64 encoded

The file is a textfile with a number of lines. A base64 encoded block is enclosed by 'begin' and 'end' markers:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG.....
...
...
-----END OPENSSH PRIVATE KEY-----
```

Check for the markers, concatenate the lines in between and base64-decode to [bytestring](#2-bytestring).

## 2. bytestring

The first 15 bytes contain `b'openssh-key-v1\x00'` as an identification tag indicating that this is indeed
an openssh-key-v1 key.

The rest of the bytestring is various aspects encoded in unsigned integers and [Strings](#23-String):

```
b'openssh-key-v1\x00'
[String] cipher name
[String] KDF name
[String] KDF options
[UInt32] number of keys (n)
[String] public key 0
 ...
[String] public key n-1
[String] secretkey blob
```

For an unencrypted key both the cipher and KDF name must be `b'none'` and the KDF options must be empty `b''`.

There should only be one key inside and we ignore the public key directly following.

The [secretkey blob](#3-secretkey-blob) is the last String in this bytestring. No data should follow afterwards.

### 2.1. UInt8

This is simply an unsigned number of 8 bits: a `char`.
```
data = readBytes(1)
return struct.unpack('>B' data)[0]
```

### 2.2. UInt32

This is four bytes representing a 32 bit unsigned integer in big-endian format.
```
data = readBytes(4)
return struct.unpack('>I' data)[0]
```

### 2.3. String

A String is a variable length data with its length prepended as an UInt32. I.e.:

```
...
  4 bytes [UInt32] b'\x00\x00\x01\x0f' = 271
271 bytes [binary] ...
...
```
```
length_b = readBytes(4)
length = struct.unpack('>I' length_b)[0]
return readBytes(length)
```

## 3. secretkey blob

The secret key blob would usually be encrypted. Since hostkeys are usually not encrypted we can just use it as-is.
It is in itself a bytestring:

```
[UInt32] magic number 1
[UInt32] magic number 2
[String] key type          }
 ... key contents          } repeated for n keys
[String] key comment       }
[UInt 8] padding \x01
[UInt 8] padding \x02
[UInt 8] padding \x03
 ... until secretkey blob reaches next encryption blocksize (256)
```

The contents vary depending on the key type:

### 3.1. ssh-ed25519

```
[String] key type         # = b'ssh-ed25519'
[String] public key       # 32 bytes
[String] secret key       # 64 bytes, repeating public key in last 32 bytes
[String] key comment      # username@hostname
```

### 3.2. ecdsa-sha2-nistp256

```
[String] key type         # = b'ecdsa-sha2-nistp256'
[String] curve            # = b'nistp256'
[String] public key       # ???
[String] secret key       # ???
[String] key comment      # username@hostname
```

As you can see, I am still not sure what format exactly the keys are and how to make them compatible with TinySSH's format.

### 3.3. others

Other key types are possible but are not supported by TinySSH.
