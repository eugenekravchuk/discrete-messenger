'''Create public and private keys'''
import random
from math import gcd
from Crypto.Util.number import getPrime, isPrime

def loopIsPrime(number):
    # Looping to reduce probability of Rabin-Miller false positives
    is_number_prime = True
    for _ in range(20):
        is_number_prime *= isPrime(number)
        if not is_number_prime:
            return is_number_prime
    return is_number_prime


def modexp(base, exp, modulus):
    return pow(base, exp, modulus)


def squareAndMultiply(x, c, n):
    z = 1
    # Getting the value of l by converting c into binary representation and getting its length
    c = bin(c)[2:][::-1]  # Optimized version of "{0:b}".format(c)[::-1]

    l = len(c)
    for i in range(l - 1, -1, -1):
        z = pow(z, 2) % n
        if c[i] == '1':
            z = (z * x) % n
    return z


def keyGeneration():
    print("Computing key values, please wait...")
    loop = True
    while loop:
        k = random.randrange(2**(415), 2**(416))  # 416 bits
        q = getPrime(160)
        p = (k * q) + 1
        while not isPrime(p):
            k = random.randrange(2**(415), 2**(416))  # 416 bits
            q = getPrime(160)
            p = (k * q) + 1

        L = p.bit_length()

        # Calculate `g` as t^(p-1)/q % p
        # If g^q % p == 1, we found `g`
        t = random.randint(1, p - 1)
        g = squareAndMultiply(t, (p - 1) // q, p)

        if 512 <= L <= 1024 and L % 64 == 0 and (gcd(p - 1, q)) > 1 \
            and squareAndMultiply(g, q, p) == 1:
            loop = False

            a = random.randint(2, q - 1)
            h = squareAndMultiply(g, a, p)

            with open("key.txt", "w", encoding='utf-8') as file1:
                file1.write(f"{p}\n")
                file1.write(f"{q}\n")
                file1.write(f"{g}\n")
                file1.write(f"{h}\n")

            with open("secretkey.txt", "w", encoding='utf-8') as file2:
                file2.write(f"{a}\n")

            print("Verification key stored at key.txt and secret key stored at secretkey.txt")

keyGeneration()
