# Pretty Good Privacy (PGP) Simulation

This project is a Python application simulating the Pretty Good Privacy (PGP) algorithms.

## How to Use

To run the project, you need Python 3 and the necessary packages installed.

1. Run `receive.py` to receive encrypted messages.
2. Run `send.py` to encrypt and send messages.
3. 2 mail account you must have.

## Requirements

- Python 3
- Crypto package (to install: `pip install pycryptodome`)
- pyDes package (to install: `pip install pyDes`)

## Running the Project

-Before running the project, you have to create new accounts. I created account with google mail and I got help with this
youtube link ---> https://www.youtube.com/watch?v=g_j6ILT-X0k&t=189s&ab_channel=ThePyCoach

1. Run `send.py` to encrypts the message, adds a keyPair to the message and sends it.
2. The code will ask you for your email and password and then ask for the message you want to send.
3. Run  `receive.py` to decrypt incoming encrypted messages with keyPair.
4. The code will ask you for your email and password. You must enter the second mail account after then you can see sending message.
