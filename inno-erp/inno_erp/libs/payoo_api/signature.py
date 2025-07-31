import base64
from hashlib import sha512

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class SignatureHandler:
	def __init__(self, private_key_pem: str, payoo_public_key_pem: str):
		self.private_key = RSA.import_key(private_key_pem)
		self.payoo_public_key = RSA.import_key(payoo_public_key_pem)

	def sign(self, data: str) -> str:
		h = SHA256.new(data.encode("utf-8"))
		signature = pkcs1_15.new(self.private_key).sign(h)
		return base64.b64encode(signature).decode("utf-8")

	def verify(self, signature_b64: str, data: str) -> bool:
		h = SHA256.new(data.encode("utf-8"))
		decoded_signature = base64.b64decode(signature_b64)
		try:
			pkcs1_15.new(self.payoo_public_key).verify(h, decoded_signature)
			return True
		except (ValueError, TypeError):
			return False

	@staticmethod
	def hash_credential(credential: str) -> str:
		return sha512(credential.encode("utf-8")).hexdigest()
