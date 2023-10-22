from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import base64
import random


class CryptOperations:

    def __init__(self) -> None:
        self.my_id = self.generate_secure_id()
        self.pub_key, self.__priv_key = self.generate_keys(self.my_id)
        self.my_key = self.serialize_rsa_public_key(self.pub_key)

    def generate_keys(self, prefix):
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        # Generate public key
        public_key = private_key.public_key()
        # Save private key
        with open(f"{prefix}_private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))
        # Save public key
        with open(f"{prefix}_public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ))
        return public_key, private_key

    def sign_message(self, message):
        signature = self.__priv_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, public_key_pem, message, signature):
        public_key = serialization.load_pem_public_key(public_key_pem)
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

    def generate_secure_id(self, length=32):
        # Generate random bytes
        random_bytes = int.to_bytes(random.getrandbits(length * 8), length, 'big')
        # Encode the bytes in URL-safe base64 format
        secure_id = base64.urlsafe_b64encode(random_bytes).rstrip(b'=')
        return secure_id.decode('utf-8')

    def serialize_rsa_public_key(self, public_key) -> tuple:
        public_numbers = public_key.public_numbers()
        return (public_numbers.n, public_numbers.e)

    def deserialize_rsa_public_key(tuple_representation: tuple):
        modulus, exponent = tuple_representation
        # Construct the RSA public numbers and then the public key
        public_numbers = rsa.RSAPublicNumbers(e=exponent, n=modulus)
        public_key = public_numbers.public_key(backend=default_backend())
        return public_key
