'''DSA algorithm implementation'''
import hashlib
from Crypto.Util.number import inverse, getPrime, isPrime
import random
from math import gcd

class DSA:

    @staticmethod
    def loopIsPrime(number):
        # Looping to reduce probability of Rabin-Miller false positives
        is_number_prime = True
        for _ in range(20):
            is_number_prime *= isPrime(number)
            if not is_number_prime:
                return is_number_prime
        return is_number_prime

    @staticmethod
    def modexp(base, exp, modulus):
        return pow(base, exp, modulus)

    @staticmethod
    def square_multiply(x, c, n):
        z = 1
        # Getting the value of l by converting c into binary representation and getting its length
        c = bin(c)[2:][::-1]  # Optimized version of "{0:b}".format(c)[::-1]

        l = len(c)
        for i in range(l - 1, -1, -1):
            z = pow(z, 2) % n
            if c[i] == '1':
                z = (z * x) % n
        return z

    def generate_key(self):
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
            g = self.square_multiply(t, (p - 1) // q, p)

            if 512 <= L <= 1024 and L % 64 == 0 and (gcd(p - 1, q)) > 1 \
                and self.square_multiply(g, q, p) == 1:
                loop = False

                a = random.randint(2, q - 1)
                h = self.square_multiply(g, a, p)

                public_key = (p, q, g, h)
                private_key = a
                return public_key, private_key

    def sign(self, plaintext, public_key, private_key):
        p, q, g, h = public_key
        a = private_key

        # Signing the text
        loop = True
        while loop:
            r = random.randint(1, q - 1)
            c1 = self.square_multiply(g, r, p) % q
            c2 = self.shaHash(plaintext) + (a * c1)
            Rinverse = inverse(r, q)
            c2 = (c2 * Rinverse) % q

            if c1 != 0 and c2 != 0:
                loop = False
        return c1, c2

    @staticmethod
    def shaHash(text, blocksize=65536):
        hasher = hashlib.sha1()
        buf = text.encode()  # Конвертуємо стрічку в байти
        start = 0
        end = min(blocksize, len(buf))
        while start < len(buf):
            hasher.update(buf[start:end])
            start = end
            end = min(start + blocksize, len(buf))
        hex_hash = "0x" + hasher.hexdigest()
        return int(hex_hash, 0) 

    def verification(self, received_text, public_key, signature):
        (p, q, g, h) = public_key
        c1, c2 = signature

        # Calculate t1 and t2
        t1 = self.shaHash(received_text)
        inverseC2 = inverse(c2, q)
        t1 = (t1 * inverseC2) % q

        t2 = inverse(c2, q)
        t2 = (t2 * c1) % q

        # Calculate valid1 and valid2
        valid1 = self.square_multiply(g, t1, p)
        valid2 = self.square_multiply(h, t2, p)
        valid = ((valid1 * valid2) % p) % q

        # Check validity
        return valid == c1

# if __name__ == "__main__":
#     with open("D:\Дискретна\Комп'ютерний проект 2\discrete-messenger\digital sihnature algorithm\primary_text.txt", 'r', encoding='utf-8') as file:
#         plaintext = file.read()

#     dsa = DSA()
#     public_key, private_key = dsa.generate_key()

#     print(dsa.verification(plaintext, public_key, dsa.sign(plaintext, public_key, private_key)))
