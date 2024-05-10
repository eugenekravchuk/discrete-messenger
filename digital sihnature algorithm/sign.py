'''Create a signature for a text file'''
import sys
import hashlib
import random
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
    # Printing the hash if necessary
    hex_hash = "0x" + hasher.hexdigest()
    return int(hex_hash, 0)  # Returns int value of hash


def sign():
    if len(sys.argv) < 2:
        print("Format: python sign.py filename")
    elif len(sys.argv) == 2:
        print("Signing the file...")
        fileName = sys.argv[1]

        # Open key file and secret key file
        with open("key.txt", "r", encoding="utf-8") as file1:
            p = int(file1.readline().strip())
            q = int(file1.readline().strip())
            g = int(file1.readline().strip())
            h = int(file1.readline().strip())

        with open("secretkey.txt", "r", encoding="utf-8") as file2:
            a = int(file2.readline().strip())

        # Signing the file
        loop = True
        while loop:
            r = random.randint(1, q - 1)
            c1 = squareAndMultiply(g, r, p) % q
            c2 = shaHash(fileName) + (a * c1)
            Rinverse = inverse(r, q)
            c2 = (c2 * Rinverse) % q

            if c1 != 0 and c2 != 0:
                loop = False

        # Save the signature
        with open("signature.txt", "w", encoding="utf-8") as file:
            file.write(f"{c1}\n{c2}")
        print("Signature stored at signature.txt")

sign()