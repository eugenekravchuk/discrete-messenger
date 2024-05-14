from flask import Flask, jsonify, request, render_template
from encryption.elgamal import generate_keys, encrypt, decrypt
from encryption.rcs import RCS
from encryption.dsa import DSA
from encryption.rsa import primefiller, setkeys, encoder, decoder

app = Flask(__name__)
rcs = RCS()
dsa = DSA()

@app.route('/')
def home():
    return "Home"

@app.route('/test')
def test():
    return {"members":["Member1"]}

@app.route('/generate_keys_eg')
def generate_keys_eg():
    public_key, private_key = generate_keys()
    public_key = [str(i) for i in public_key]
    private_key = str(private_key)
    return {'private_key': private_key, 'public_key': public_key}

@app.route('/encrypt_eg')
def encrypt_eg():
    message = request.args.get('message')
    public_key1 = request.args.get('public_key1')
    public_key2 = request.args.get('public_key2')
    public_key3 = request.args.get('public_key3')
    public_key = tuple((int(public_key1), int(public_key2), int(public_key3)))
    encrypted_message = encrypt(message, public_key)
    return jsonify({'encrypted_message': [str(i) for i in encrypted_message[0]], 'original': message})

@app.route('/decrypt_eg')
def decrypt_eg():
    encrypted_message1 = request.args.get('encrypted_message1')
    encrypted_message2 = request.args.get('encrypted_message2')
    encrypted_message = [(int(encrypted_message1), int(encrypted_message2))]
    public_key1 = request.args.get('public_key1')
    public_key2 = request.args.get('public_key2')
    public_key3 = request.args.get('public_key3')
    private_key = request.args.get('private_key')
    public_key = tuple((int(public_key1), int(public_key2), int(public_key3)))
    private_key = int(private_key)
    decrypted_message = decrypt(encrypted_message, private_key, public_key)
    return jsonify({'decrypted_message': decrypted_message})

@app.route('/generate_keys_rcs')
def generate_keys_rcs():
    public_key, p, q = rcs.generate_keypair(1024)
    public_key = str(public_key)
    private_key = [str(p), str(q)]
    return {'private_key': private_key, 'public_key': public_key}

@app.route('/encrypt_rcs')
def encrypt_rcs():
    message = request.args.get('message')
    public_key = int(request.args.get('public_key'))
    ciphertext = rcs.encrypt(message, public_key)
    return jsonify({'encrypted_message': str(ciphertext)})

@app.route('/decrypt_rcs')
def decrypt_rcs():
    encrypted_message = request.args.get('encrypted_message')
    private_key1 = request.args.get('private_key1')
    private_key2 = request.args.get('private_key2')
    public_key = request.args.get('public_key')
    decrypted = rcs.decrypt(int(encrypted_message), int(private_key1), int(private_key2), int(public_key))
    return jsonify({'decrypted_message': decrypted})

@app.route('/generate_keys_rsa')
def generate_keys_rsa():
    primes = primefiller()
    public_key, private_key, n = setkeys(primes)
    public_key = str(public_key)
    n = str(n)
    private_key = str(private_key)
    return {'private_key': private_key, 'public_key': public_key, 'n': n}

@app.route('/encrypt_rsa')
def encrypt_rsa():
    message = request.args.get('message')
    n = int(request.args.get('n'))
    public_key = int(request.args.get('public_key'))
    ciphertext = encoder(message, public_key, n)
    return jsonify({'encrypted_message': ciphertext})

@app.route('/decrypt_rsa')
def decrypt_rsa():
    encrypted_messages = list(map(int, request.args.getlist('encrypted_message[]')))
    private_key = int(request.args.get('private_key'))
    n = int(request.args.get('n'))
    decrypted = decoder(encrypted_messages, private_key, n)
    return jsonify({'decrypted_message': decrypted})

@app.route('/generate_keys_dsa')
def generate_keys_dsa():
    public_key, private_key = dsa.generate_key()
    public_key = [str(i) for i in public_key]
    private_key = str(private_key)
    return {'private_key': private_key, 'public_key': public_key}

@app.route('/sign_dsa')
def encrypt_dsa():
    message = request.args.get('message')
    public_key1 = int(request.args.get('public_key1'))
    public_key2 = int(request.args.get('public_key2'))
    public_key3 = int(request.args.get('public_key3'))
    public_key4 = int(request.args.get('public_key4'))
    public_key = (public_key1, public_key2, public_key3, public_key4)
    private_key = int(request.args.get('private_key'))
    signature = dsa.sign(message, public_key, private_key)
    return jsonify({'signature': [str(s) for s in signature]})

@app.route('/verify_dsa')
def decrypt_dsa():
    public_key1 = int(request.args.get('public_key1'))
    public_key2 = int(request.args.get('public_key2'))
    public_key3 = int(request.args.get('public_key3'))
    public_key4 = int(request.args.get('public_key4'))
    public_key = (public_key1, public_key2, public_key3, public_key4)
    signature1 = request.args.get('signature1')
    signature2 = request.args.get('signature2')
    message = request.args.get('message')
    verified = dsa.verification(message, public_key, (int(signature1), int(signature2)))
    return jsonify({'verified': verified})


if __name__ == '__main__':
    app.run()
