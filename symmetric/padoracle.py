#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM

from util.convert import hstr_to_ascii, ascii_to_hstr
from util.error import PadOracleError


def _split_cipher(cipher):
    """Split 'cipher' [string] into 16-chars blocks [List<List<int>>]."""
    cipher = hstr_to_ascii(cipher)
    if not cipher or len(cipher)%16 != 0:
        raise PadOracleError("Cipher size must be a multiple of 16 bytes")
    clist = [[] for i in range(len(cipher)//16)]
    for i in range(0, len(cipher), 16):
        tmp = cipher[i:i+16]
        for j in range(0, 16):
            clist[i//16].append(tmp[j])
    return clist


def _merge_cipher(clist):
    """Flatten 'clist' [List<List<int>>] and return the corresponding string [bytes]."""
    cipher = [e for sublist in clist for e in sublist]
    return bytes(cipher)


def _next_block(clist, plain, n, offset, sock, err):
    """Compute 'plain' for the 'n'-th block."""
    for i in range(16-offset):
        pad = offset+1+i
        clist_tmp = [[e for e in sublist] for sublist in clist]
        for j in range(pad-1):
            clist_tmp[-2-n][-1-j] = pad ^ plain[-1-n][-1-j] ^ clist[-2-n][-1-j]

        for j in range(256):

            data = sock.recv(1024)
            clist_tmp[-2-n][-pad] = j
            sock.sendall(ascii_to_hstr(_merge_cipher(clist_tmp)))
            data = sock.recv(1024)
            if err not in data:
                plain[-1-n][-pad] = pad ^ clist_tmp[-2-n][-pad] ^ clist[-2-n][-pad]
                break
    return plain


def padding_oracle(cipher, host):
    """Padding oracle attack on CBC encryption mode.

    Keyword arguments:
    cipher [hex string] -- ciphertext
    host [dictionnary] -- oracle info (IP, port and error message)
    Output:
    plain [bytes] -- decoded plaintext
    """
    clist = _split_cipher(cipher)
    plain = [[0 for i in clist[0]] for j in range(len(clist) - 1)]

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((host["hostname"], host["port"]))
        # Compute padding
        padding = 0
        for i in range(16):
            data = s.recv(1024)
            data = s.recv(1024)
            print(data)
            clist[-2][i] = (clist[-2][i] + 1) % 256
            s.sendall(ascii_to_hstr(_merge_cipher(clist)))
            clist[-2][i] = (clist[-2][i] - 1) % 256
            data = s.recv(1024)
            print(data)
            if host["error"] in data or b"invalid" in data or b"Error" in data:
                padding = 16 - i
                break
        # Update plain with the previously found padding
        for i in range(padding):
            plain[-1][-1-i] = padding
        # Compute plain using the oracle
        offset = padding
        for n, _ in enumerate(plain):
            _next_block(clist, plain, n, offset, s, host["error"])
            offset = 0

    return _merge_cipher(plain)[:-padding]
