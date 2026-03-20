# Text Encryption & Decryption

## What does this program do?
This program encrypts and decrypts text using AES encryption with CBC mode.

## Libraries used
I installed `pycryptodome` to access these imports:
- `AES` from `Crypto.Cipher` — the encryption algorithm used to encrypt and decrypt data
- `get_random_bytes` from `Crypto.Random` — generates a random key of exactly 16, 24, or 32 bytes for 128, 192, or 256-bit encryption
- `pad` and `unpad` from `Crypto.Util.Padding` — CBC mode requires fixed 16 byte blocks, so padding is added to fill any remaining space and removed after decryption
- `b64encode` and `b64decode` from `base64` — converts encrypted binary data into readable and storable text using 64 printable characters

## How it works
A 32 byte key is generated using `get_random_bytes(32)` and stored outside both 
functions so both can access it. Think of the key as a password — the same key 
that encrypts must be used to decrypt.

**Encrypting:**
The `encrypt(plain_text, key)` function creates a new AES cipher object using 
the key and CBC mode. The plain text is first encoded into bytes using `.encode("utf-8")` 
since AES works on raw bytes, not strings. It is then padded to meet CBC's fixed 
16 byte block requirement. The padded data is encrypted and base64 encoded into 
readable text. The function returns both the encoded data and the IV. The IV 
(Initialization Vector) is a random value CBC generates automatically to 
randomize encryption so the same text encrypted twice produces different results. 
It must be returned alongside the encoded data since it is required for decryption.

**Decrypting:**
The `decrypt(encoded, iv)` function works in reverse. A new cipher object is 
created using the key, CBC mode, and the IV. The encoded data is base64 decoded, 
then decrypted, then unpadded. `.decode("utf-8")` converts the result from bytes 
back into a readable string, otherwise it would return with a `b` prefix.

Both functions are called outside, with `encoded, iv = encrypt(...)` using 
**tuple unpacking** to store the two return values into separate variables in 
one line.

Both functions are defined before being called. This follows Python convention of separating function definitions from execution.

## What I learned
- How AES encryption works with CBC mode
- The difference between CBC and CFB mode and why padding is needed for CBC
- What an IV (Initialization Vector) is and why it is necessary for decryption
- How base64 encoding converts binary data into readable text
- How `.encode("utf-8")` and `.decode("utf-8")` convert between strings and bytes
- How to return multiple values from a function and unpack them with tuple unpacking
