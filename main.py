import json
import secrets
import string
import hashlib
import base64
from cryptography.fernet import Fernet

def load_master_hash():
    try:
        with open("master.hash", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def load_or_create_salt():
    try:
        with open("salt.bin", "rb") as file:
            return file.read()
    except FileNotFoundError:
        salt = secrets.token_bytes(16)
        with open("salt.bin", "wb") as file:
            file.write(salt)
        return salt

def add_password(cipher):
        
    service = input("Enter the service name: ").strip().title()
    if not service:
        print("Service name cannot be empty.")
        return
    
    username = input("Enter the username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    choice = input("Do you want to generate a password? (y/n): ").strip().lower()

    if choice == "y":
        password = generate_password()
        if password is None:
            return
        
    else:
        password = input("Enter the password: ").strip()
        if not password:
            print("Password cannot be empty.")
            return

    encrypted_password = cipher.encrypt(password.encode()).decode()
    passwords.append({
        "service": service,
        "username": username,
        "password": encrypted_password
    })

    save_passwords()
    print(f"Password for {service} added successfully.")

def view_passwords(cipher):

    if not passwords:
        print("No saved accounts.")
        return

    print("\nSaved Accounts:")
    for idx, entry in enumerate(passwords, start=1):
        decrypted_password = cipher.decrypt(entry["password"].encode()).decode()
        print(f"{idx}. Service: {entry['service']}, Username: {entry['username']}, Password: {decrypted_password}")

def load_passwords():

    try:
        with open("passwords.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_passwords():
    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

def search_passwords(cipher):
    if not passwords:
        print("No saved accounts.")
        return
    
    search_term = input("Enter the service name to search: ").strip().title()

    if not search_term:
        print("Service name cannot be empty.")
        return

    for entry in passwords:
        if entry["service"] == search_term:
            decrypted_password = cipher.decrypt(entry["password"].encode()).decode()
            print(
                f"Service: {entry['service']}, "
                f"Username: {entry['username']}, "
                f"Password: {decrypted_password}"
            )
            return
    print(f"No saved account found for {search_term}.")

def delete_password():
    if not passwords:
        print("No saved accounts.")
        return
    
    delete_term = input("Enter the service name to delete: ").strip().title()
    if not delete_term:
        print("Service name cannot be empty.")
        return
    
    matches = []

    for idx, entry in enumerate(passwords):
        if entry["service"] == delete_term:
            matches.append((idx, entry))
            
    if not matches:
        print(f"No saved account found for {delete_term}.")
        return
    
    for number, (idx, entry) in enumerate(matches, start=1):
        print(
            f"{number}. Service: {entry['service']}, "
            f"Username: {entry['username']}"
        )

    try:
        choice = int(input("Enter the number of the account to delete: ")) - 1
        real_index, selected_entry = matches[choice]

    except (ValueError, IndexError):
        print("Invalid choice.")
        return
    
    confirm = input(
        f"Delete password for {selected_entry['service']} "
        f"({selected_entry['username']})? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Delete operation cancelled.")
        return

    del passwords[real_index]
    save_passwords()
    print(f"Password for {delete_term} deleted successfully.")

def edit_password(cipher):
    if not passwords:
        print("No saved accounts.")
        return

    for idx, entry in enumerate(passwords, start=1):
        print(f"{idx}. Service: {entry['service']}, Username: {entry['username']}")

    try:
        choice = int(input("Enter the number of the account to edit: ")) - 1
    except ValueError:
        print("Invalid input.")
        return

    if choice < 0 or choice >= len(passwords):
        print("Invalid choice.")
        return

    entry = passwords[choice]
    print(f"Editing password for {entry['service']} ({entry['username']})")
    new_password = input("Enter the new password: ").strip()
    
    if not new_password:
        print("Password cannot be empty.")
        return
    
    entry["password"] = cipher.encrypt(new_password.encode()).decode()
    save_passwords()
    print(f"Password for {entry['service']} updated successfully.")

def generate_password():

    try:
        length = int(input("Enter the desired password length: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if length < 8:
        print("Password length must be at least 8 characters.")
        return
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))

    print(f"Generated password: {password}")
    return password

def derive_key(master_password):
    return hashlib.pbkdf2_hmac("sha256", master_password.encode(), salt, 600_000, dklen=64)

def authenticate_master_password():
    stored_master_hash = load_master_hash()

    if stored_master_hash is None:
        master_password = input("Set a master password: ").strip()

        if not master_password:
            print("Master password cannot be empty.")
            return

        confirm_password = input("Confirm master password: ").strip()
        
        if master_password != confirm_password:
            print("Passwords do not match.")
            return
        
        derived = derive_key(master_password)
        
        verification_hash = derived[:32]
        encryption_key = derived[32:]

        with open("master.hash", "w") as file:
            file.write(verification_hash.hex())

        print("Master password created.")
        return encryption_key

    else:
        master_password = input("Enter master password: ").strip()

        derived = derive_key(master_password)

        verification_hash = derived[:32]
        encryption_key = derived[32:]

        if verification_hash.hex() != stored_master_hash:
            print("Incorrect master password.")
            return
        
        return encryption_key


salt = load_or_create_salt()
passwords = load_passwords()


def main():

    encryption_key = authenticate_master_password()

    if encryption_key is None:
        return

    fernet_key = base64.urlsafe_b64encode(encryption_key)
    cipher = Fernet(fernet_key)

    while True:

        print("\nPassword Manager")
        print("1. Add password")
        print("2. View saved accounts")
        print("3. Search passwords")
        print("4. Delete password")
        print("5. Edit password")
        print("6. Generate password")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_password(cipher)
        elif choice == "2":
            view_passwords(cipher)
        elif choice == "3":
            search_passwords(cipher)
        elif choice == "4":
            delete_password()
        elif choice == "5":
            edit_password(cipher)
        elif choice == "6":
            generate_password()
        elif choice == "7":
            save_passwords()
            print("Exiting the program.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()