from Crypto.Util.number import getPrime, inverse

# Генеруємо великі прості числа p і g
def generate_primes():
    p = getPrime(1024)  # Велике просте число p
    g = getPrime(512)   # Примітивний корінь modulo p
    return p, g

# Генеруємо ключі
def generate_keys():
    p, g = generate_primes()
    x = getPrime(256)  # Приватний ключ (випадкове число)
    y = pow(g, x, p)   # Публічний ключ
    return (p, g, y), x

# Шифруємо повідомлення
def encrypt(message, public_key):
    p, g, y = public_key
    m = int.from_bytes(message.encode(), 'big')
    k = getPrime(256)  # Випадкове число k
    c1 = pow(g, k, p)
    c2 = (m * pow(y, k, p)) % p
    return c1, c2

# Розшифровуємо шифрований текст
def decrypt(ciphertext, private_key):
    p, g, y = public_key
    x = private_key
    c1, c2 = ciphertext
    s = pow(c1, x, p)
    m = (c2 * inverse(s, p)) % p
    return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()

# Приклад використання
if __name__ == "__main__":
    # Генеруємо ключі
    public_key, private_key = generate_keys()

    # Повідомлення для шифрування
    message = "Text"

    # Шифруємо повідомлення за допомогою публічного ключа
    ciphertext = encrypt(message, public_key)
    print("Encrypted:", ciphertext)

    # Розшифровуємо шифрований текст за допомогою приватного ключа
    decrypted_message = decrypt(ciphertext, private_key)
    print("Decrypted:", decrypted_message)