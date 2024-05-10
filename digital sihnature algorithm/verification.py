'''Verification module'''
import sys
import hashlib
from Crypto.Util.number import inverse


def squareAndMultiply(x, c, n):
    z = 1
    # Getting value of l by converting c into binary representation and getting its length
    c = bin(c)[2:][::-1]  # Optimized version of "{0:b}".format(c)[::-1]

    l = len(c)
    for i in range(l - 1, -1, -1):
        z = pow(z, 2) % n
        if c[i] == '1':
            z = (z * x) % n
    return z


def shaHash(fileName):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(fileName, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    hex_hash = "0x" + hasher.hexdigest()
    return int(hex_hash, 0)  # Returns int value of hash


def verification():
    if len(sys.argv) < 2:
        print("Format: python sign.py filename")
    elif len(sys.argv) == 2:
        print("Checking the signature...")
        fileName = sys.argv[1]

        # Open key file
        with open("key.txt", "r", encoding='utf-8') as file1:
            p = int(file1.readline().rstrip())
            q = int(file1.readline().rstrip())
            g = int(file1.readline().rstrip())
            h = int(file1.readline().rstrip())

        # Open signature file
        with open("signature.txt", "r", encoding='utf-8') as file2:
            c1 = int(file2.readline().rstrip())
            c2 = int(file2.readline().rstrip())

        # Calculate t1 and t2
        t1 = shaHash(fileName)
        inverseC2 = inverse(c2, q)
        t1 = (t1 * inverseC2) % q

        t2 = inverse(c2, q)
        t2 = (t2 * c1) % q

        # Calculate valid1 and valid2
        valid1 = squareAndMultiply(g, t1, p)
        valid2 = squareAndMultiply(h, t2, p)
        valid = ((valid1 * valid2) % p) % q

        # Check validity
        if valid == c1:
            print("Valid signature")
        else:
            print("Invalid signature")


# Run the verification function
verification()
