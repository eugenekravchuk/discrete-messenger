"""Python program to implement ECDSA"""
import hashlib
import random

class EllipticCurve:
    def __init__(self):
        self.p = pow(2, 255) - 19
        self.a = -1
        self.d = self.findPositiveModulus(-121665 * self.findModInverse(121666, self.p), self.p)
        self.base = 15112221349535400772501151409588531511454012693041857206046113283949847762202, \
46316835694926478169428394003475163141307993866256225615783033603165251855960

    @staticmethod
    def findPositiveModulus(a, p):
        if a < 0:
            a = (a + p * int(abs(a)/p) + p) % p
        return a

    @staticmethod
    def textToInt(text):
        '''
        Function for typecasting from string to int
        '''
        encoded_text = text.encode('utf-8')
        hex_text = encoded_text.hex()
        int_text = int(hex_text, 16)
        return int_text

    @staticmethod
    def gcd(a, b):
        '''
        Function to find greatest common divisor(gcd) of a and b
        '''
        while a != 0:
            a, b = b % a, a
        return b


    def findModInverse(self, a, m):
        '''Function to find the modular inverse of a mod m'''
        if a < 0:
            a = (a + m * int(abs(a)/m) + m) % m

        # no mod inverse if a & m aren't
        # relatively prime
        if self.gcd(a, m) != 1:
            return None

        # Calculate using the Extended
        # Euclidean Algorithm:
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:

            q = u3 // v3 
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

    def applyDoubleAndAddMethod(self, P, k, a, d, mod):

        additionPoint = (P[0], P[1])
        kAsBinary = bin(k) 
        kAsBinary = kAsBinary[2:len(kAsBinary)] 

        for i in range(1, len(kAsBinary)):
            currentBit = kAsBinary[i: i+1]

            additionPoint = self.pointAddition(additionPoint, additionPoint, a, d, mod)

            if currentBit == '1':
                additionPoint = self.pointAddition(additionPoint, P, a, d, mod)

        return additionPoint

    def pointAddition(self, P, Q, a, d, mod):
        '''Function to calculate the point addition '''
        x1 = P[0]; y1 = P[1]
        x2 = Q[0]; y2 = Q[1]

        x3 = (((x1*y2 + y1*x2) % mod) * self.findModInverse(1+d*x1*x2*y1*y2, mod)) % mod
        y3 = (((y1*y2 - a*x1*x2) % mod) * self.findModInverse(1- d*x1*x2*y1*y2, mod)) % mod

        return x3, y3

    def generate_keys(self):
        private_key = random.getrandbits(256)
        public_key = self.applyDoubleAndAddMethod(self.base, private_key, self.a, self.d, self.p)
        return private_key, public_key

    @staticmethod
    def hashing(message):
        hash_obj = hashlib.sha256()
        hash_obj.update(int.to_bytes(message, length=(message.bit_length() + 7) // 8, \
byteorder='big'))
        return int.from_bytes(hash_obj.digest(), byteorder='big')

    def sign(self, message, public_key, private_key):
        message = self.textToInt(message)
        r = self.hashing(self.hashing(message) + message) % self.p
        R = self.applyDoubleAndAddMethod(self.base, r, self.a, self.d, self.p)
        h = self.hashing(R[0] + public_key[0] + message) % self.p
        s = r + h * private_key
        return R, s

    def verify(self, message, r, sig, public_key):
        h = self.hashing(r[0] + public_key[0] + self.textToInt(message)) % self.p
        P1 = self.applyDoubleAndAddMethod(self.base, sig, self.a, self.d, self.p)

        P2 = self.pointAddition(r, self.applyDoubleAndAddMethod(public_key, h, self.a, \
self.d, self.p), self.a, self.d, self.p)
        return P1[0] == P2[0] and P1[1] == P2[1]


# #Example of usage
# # ax^2 + y^2 = 1 + dx^2y^2
# # ed25519
# ec = EllipticCurve()


# # print("curve: ",a,"x^2 + y^2 = 1 + ",d,"x^2 y^2")

# print("----------------------")
# print("Key Generation: ")

# # privateKey = 47379675103498394144858916095175689
# # 779086087640336534911165206022228115974270 #32 byte secret key
#  #32 byte secret key
# pr_k, pub_k = ec.generate_keys()
# print("private key: ",pr_k)
# print("public key: ", pub_k)

# message = "Hello, world!"
# # Function for hashing the message

# # ---------------------------------------
# # sign
# R, s = ec.sign(message, pub_k, pr_k)

# print("----------------------")
# print("Signing:")
# print("message: ",message)
# print("Signature (R, s)")
# print("R: ",R)
# print("s: ",s)


# # -----------------------------------
# # verify
# new_message = message

# print("----------------------")
# print("Verification:")
# print("result")
# result = ec.verify(new_message, R, s, pub_k)
# print(f"Received message is valid: {result}")
# # ----------------------------------
