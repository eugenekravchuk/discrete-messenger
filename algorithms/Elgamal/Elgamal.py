from Crypto.Util.number import getPrime, inverse

class Elgamal:
    # Генеруємо великі прості числа p і g
    @staticmethod
    def generate_primes():
        p = getPrime(1024)  # Велике просте число p
        g = getPrime(512)   # Примітивний корінь modulo p
        return p, g

    # Генеруємо ключі
    def generate_keys(self):
        p, g = self.generate_primes()
        x = getPrime(256)  # Приватний ключ (випадкове число)
        y = pow(g, x, p)   # Публічний ключ
        return (p, g, y), x

    # Шифруємо повідомлення
    @staticmethod
    def encrypt(message, public_key):
        p, g, y = public_key
        m = int.from_bytes(message.encode(), 'big')
        k = getPrime(256)  # Випадкове число k
        c1 = pow(g, k, p)
        c2 = (m * pow(y, k, p)) % p
        return c1, c2

    # Розшифровуємо шифрований текст
    @staticmethod
    def decrypt(ciphertext, private_key, public_key):
        p, g, y = public_key
        x = private_key
        c1, c2 = ciphertext
        s = pow(c1, x, p)
        m = (c2 * inverse(s, p)) % p
        return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()

# Приклад використання
# if __name__ == "__main__":
#     # Генеруємо ключі
#     elgamal = Elgamal()
#     public_key, private_key = elgamal.generate_keys()

#     # Повідомлення для шифрування
#     message = "Hello world!"
#     # Шифруємо повідомлення за допомогою публічного ключа
#     ciphertext = elgamal.encrypt(message, public_key)
#     print("Encrypted:", ciphertext)

#     # Розшифровуємо шифрований текст за допомогою приватного ключа
#     decrypted_message = elgamal.decrypt(ciphertext, private_key, public_key)
#     print("Decrypted:", decrypted_message)

class ElgamalBig:

    @staticmethod
    def file_read(filename):
        try:
            with open(filename, 'r') as file:
                contents = file.read()
            return contents
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return None

    @staticmethod
    def generate_primes():
        p = getPrime(2048)
        g = getPrime(512)
        return p, g

    def generate_keys(self):
        p, g = self.generate_primes()
        x = getPrime(256)
        y = pow(g, x, p)
        return (p, g, y), x

    @staticmethod
    def encrypt(message, public_key):
        p, g, y = public_key
        k = getPrime(512)
        c1 = pow(g, k, p)
        encrypted_parts = []
        if message is None:
            print("The message is None.")
            return
        for i in range(0, len(message), 128):  # Розбиваємо повідомлення на частини по 128 символів
            part = message[i:i+128]
            bytes_data = part.encode('utf-8')
            c2 = (int.from_bytes(bytes_data, byteorder='big') * pow(y, k, p)) % p
            encrypted_parts.append((c1, c2))
        return encrypted_parts

    @staticmethod
    def decrypt(ciphertexts, private_key, public_key):
        p, g, y = public_key
        x = private_key
        decrypted_parts = []
        for ciphertext in ciphertexts:
            c1, c2 = ciphertext
            s = pow(c1, x, p)
            m = (c2 * inverse(s, p)) % p
            bytes_data = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
            try:
                decrypted_parts.append(bytes_data.decode('utf-8'))
            except UnicodeDecodeError:
                print("Cannot decode the message. The encrypted message may have been tampered with.")
                return None
        return ''.join(decrypted_parts)

if __name__ == "__main__":
    el_big = ElgamalBig()
    public_key, private_key = el_big.generate_keys()
    message = 'Hello world!'
    ciphertexts = el_big.encrypt(message, public_key)
    print("Encrypted:", ciphertexts)
    decrypted_message = el_big.decrypt(ciphertexts, private_key, public_key)
    print("Decrypted:", decrypted_message)