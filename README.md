# Password Manager

## About

- A command-line password manager built with Python. Users can add, view, search, edit, delete, and generate passwords. Passwords are encrypted and protected by a master password.
- Passwords are encrypted using Fernet and a key derived from the master password using PBKDF2.

## Features

- Add passwords
- View saved accounts
- Search passwords
- Delete passwords
- Edit passwords
- Generate secure passwords
- Master password protection
- Encrypted password storage

## Technologies

- Python
- JSON
- Cryptography / Fernet
- PBKDF2

## How to run

1. Clone repository
2. Navigate to the project folder.
3. Install dependencies:

```bash
pip install cryptography
```

4. Run:

 ```bash
 python main.py
 ```