from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import pyDes
import imaplib
import email
import re
import os


class PGPProject:
    def __init__(self):
        self.email_address = ""
        self.password = ""

    def get_private_key(self):
        key_pair = None
        if os.path.exists("keyPair.pem"):
            with open("keyPair.pem", "rb") as f:
                key_pair = RSA.importKey(f.read())
        if not key_pair:
            key_pair = RSA.generate(1024)
            with open("keyPair.pem", "wb") as f:
                f.write(key_pair.exportKey("PEM"))
        return key_pair

    def decrypt_key(self, encrypted_key, private_key):
        decryptor = PKCS1_OAEP.new(private_key)
        return decryptor.decrypt(encrypted_key)

    def decrypt_message(self, encrypted_message, key):
        key = key.to_bytes(8, "big")
        DES = pyDes.des(key, pyDes.CBC, IV=b"\0\0\0\0\0\0\0\0",
                        pad=None, padmode=pyDes.PAD_PKCS5)
        return DES.decrypt(encrypted_message, padmode=pyDes.PAD_PKCS5)

    def extract_message(self, encrypted_key, encrypted_message):
        private_key = self.get_private_key()
        session_key = self.decrypt_key(encrypted_key, private_key)
        session_key = int.from_bytes(session_key, "big")
        return self.decrypt_message(encrypted_message, session_key)

    def receive_email(self):
        with imaplib.IMAP4_SSL("imap.gmail.com") as connection:
            connection.login(self.email_address, self.password)
            connection.select("inbox")

            _, data = connection.search(None, '(SUBJECT "PGP Projesi")')

            message = ""

            _, data = connection.fetch(data[0].split()[-1], "(RFC822)")

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode())
                    message = msg.get_payload()[0].get_payload()
                    break
            if not message:
                print("Herhangi bir mesajınız yok.")
                exit(-1)
            key_message = list(map(int, re.findall("[0-9]+", str(message))))
            lk = key_message[0]
            lm = key_message[2]
            intk = key_message[1]
            intm = key_message[3]
            return intk.to_bytes(lk, "big"), intm.to_bytes(lm, "big")

    def run(self):
        
        self.email_address = input("E-mail@    : ")
        self.password = input("Şifre           : ") 
 
        received_email = self.receive_email()

        received_message = self.extract_message(received_email[0], received_email[1]).decode("utf-8")
        print("Alınan Mesaj:\n" + received_message)


if __name__ == "__main__":
    pgp_project = PGPProject()
    pgp_project.run()
