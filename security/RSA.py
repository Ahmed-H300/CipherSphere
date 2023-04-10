from Crypto.Util import number

class RSA:
    # RSA Init
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.p = 0
        self.q = 0
        self.n = 0
        self.phi = 0
        self.e = 0
        self.d = 0
        self.public_key = ()
        self.private_key = ()
        self.generate_key()
        self.generate_primes()
    
    # generate Keys
    def generate_key(self):
        self.generate_primes()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.get_public_chosen(self.phi)
        self.d = pow(self.e, -1, self.phi)
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    # Generate Primes for P and Q.
    def generate_primes(self):
        self.p = number.getPrime(self.key_size // 2)
        while not number.isPrime(self.p):
            self.p = number.getPrime(self.key_size // 2)
        
        self.q = number.getPrime(self.key_size // 2)
        while (not number.isPrime(self.q)) and (self.p != self.q):
            self.q = number.getPrime(self.key_size // 2)
    
    # choose suitable  E
    def get_public_chosen(self, phi):
        m = max(self.p, self.q)
        """
        Generate a random integer e where 1 < e < phi and gcd(e, phi) = 1.
        """
        while True:
            e = number.getRandomRange(m, phi)
            if number.GCD(e, phi) == 1:
                return e

    # Encrypt Word
    def encrypt_word(self, word):
        return pow(word, self.e, self.n)

    # Decrypt Word
    def decrypt_word(self, word):
        return pow(word, self.d, self.n)
    
    # Encrypt Text
    def encrypt_text(self, text):
        encrypted_text = []
        for word in text:
            encrypted_text.append(self.encrypt_word(word))
        return (encrypted_text)
    # Decrypt Text
    def decrypt_text(self, text):
        decrypted_text = []
        for word in text:
            decrypted_text.append(self.decrypt_word(word))
        return (decrypted_text)

