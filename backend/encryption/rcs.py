'''Rabin Cryptosystem algorithm'''
import base64
import random

class RCS:
    '''Rabin cryptosystem algorithm'''
    @staticmethod
    def string_to_big_number(s):
        """Convert a string to a single large number."""
        bytes_data = s.encode('utf-8')
        base64_encoded = base64.b64encode(bytes_data)
        return int.from_bytes(base64_encoded, byteorder='big')

    @staticmethod
    def big_number_to_string(num):
        """Convert a single large number back to a string."""
        bytes_data = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
        base64_decoded = base64.b64decode(bytes_data)
        return base64_decoded.decode('utf-8')

    @staticmethod
    def is_prime(n, k=5):
        """Miller-Rabin primality test."""
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False

        def check(a, s, d, n):
            x = pow(a, d, n)
            if x == 1:
                return True
            for _ in range(s - 1):
                if x == n - 1:
                    return True
                x = pow(x, 2, n)
            return x == n - 1

        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1
        for _ in range(k):
            a = random.randint(2, n - 1)
            if not check(a, s, d, n):
                return False
        return True

    def generate_prime(self, bits=1024):
        """Generate a random prime number with specified number of bits."""
        while True:
            n = random.getrandbits(bits)
            if n % 2 != 0 and n % 4 == 3 and self.is_prime(n):
                return n

    @staticmethod
    def gcd(a, b):
        """Calculate the greatest common divisor of two numbers."""
        while b:
            a, b = b, a % b
        return a

    def extended_gcd(self, a, b):
        """Extended Euclidean algorithm to find gcd and Bézout coefficients."""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def mod_inverse(self, a, m):
        """Modular multiplicative inverse."""
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            raise Exception('Modular inverse does not exist')
        return x % m

    def generate_keypair(self, bits):
        """Generate public and private keys."""
        p = self.generate_prime(bits)
        q = self.generate_prime(bits)
        while p == q:
            q = self.generate_prime(bits)
        n = p * q
        return (n, p, q)

    def encrypt(self, plaintext, n):
        """Encrypt plaintext using Rabin cryptosystem."""
        text_to_bites = self.string_to_big_number(plaintext)
        ciphertext = pow(text_to_bites, 2, n)
        return ciphertext

    def decrypt(self, ciphertext, p, q, n):
        """Decrypt ciphertext using Rabin cryptosystem."""
        # Calculate square roots of the ciphertext modulo p and q
        m1 = pow(ciphertext, (p + 1) // 4, p)
        m2 = pow(ciphertext, (q + 1) // 4, q)

        # Use Chinese Remainder Theorem to find four possible roots modulo n
        # There are two pairs of roots: (m1, m2) and (-m1, m2) (mod p*q)
        _, yp, yq = self.extended_gcd(p, q)
        r1 = (yp * p * m2 + yq * q * m1) % n
        r2 = n - r1
        r3 = (yp * p * m2 - yq * q * m1) % n
        r4 = n - r3

        # Return the four possible roots
        #Choose the correct one
        for m in [r1, r2, r3, r4]:
            # print(self.big_number_to_string(m))
            try:
                return self.big_number_to_string(m)
            except Exception:
                pass


# # Example usage
# rcs = RCS()
# plaintext = "hello"
# # message = rcs.string_to_big_number(plaintext)
# print("Original plaintext:", plaintext)

# # Generate keys
# public_key, p, q = rcs.generate_keypair(1024)
# n = public_key
# print("Public key (n):", n)

# # Encrypt plaintext
# ciphertext = rcs.encrypt(plaintext, n)
# print("Encrypted ciphertext:", ciphertext)

# # Decrypt ciphertext
# decrypted = rcs.decrypt(ciphertext, p, q, n)
# print(f"Decrypted plaintext: {decrypted}")
