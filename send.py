import pyDes
import ssl
import smtplib
import os
import random
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class PGPProject:
    def __init__(self):
        self.sender_email = ""
        self.receiver_email = ""
        self.sender_password = ""
        self.message = ""

    def generate_key(self):
        key = random.getrandbits(56)  # 56-bit key
        return key

    def encrypt_key(self, key, public_key):
        encryptor = PKCS1_OAEP.new(public_key)
        return encryptor.encrypt(key.to_bytes(8, "big"))

    def encrypt_message(self, message, key):
        key = key.to_bytes(8, "big")
        DES = pyDes.des(key, pyDes.CBC, IV=b"\0\0\0\0\0\0\0\0",
                        pad=None, padmode=pyDes.PAD_PKCS5)
        return DES.encrypt(message.encode())

    def send_email(self):
        lk = len(self.encrypted_key)
        lm = len(self.encrypted_message)
        intk = int.from_bytes(self.encrypted_key, "big", signed=False)
        intm = int.from_bytes(self.encrypted_message, "big", signed=False)
        message = f"{lk}-{intk}-{lm}-{intm}"

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = "PGP Projesi"
        msg.attach(MIMEText(message, "plain"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as connection:
            connection.login(self.sender_email, self.sender_password)
            connection.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            print("E-mail başarıyla gönderildi.")

    def run(self):
        self.sender_email    = input("E-mail adresiniz   : ")
        self.sender_password = input("Şifreniz        : ")
        self.receiver_email  = input("Alıcı e-mail     : ")
        self.message         = input("Mesaj                  : ")

        public_key = self.get_public_key()
        session_key = self.generate_key()
        self.encrypted_key = self.encrypt_key(session_key, public_key)
        self.encrypted_message = self.encrypt_message(self.message, session_key)

        encrypted_message_str = base64.b64encode(self.encrypted_message).decode("utf-8")
        print("Şifrelenmiş mesaj:", encrypted_message_str)

        self.send_email()

    @staticmethod
    def get_public_key():
        key_pair = None
        if os.path.exists("keyPair.pem"):
            with open("keyPair.pem", "rb") as f:
                key_pair = RSA.importKey(f.read())
        if not key_pair:
            key_pair = RSA.generate(1024)
            with open("keyPair.pem", "wb") as f:
                f.write(key_pair.exportKey("PEM"))
        return key_pair.publickey()


if __name__ == "__main__":
    pgp_project = PGPProject()
    pgp_project.run()
