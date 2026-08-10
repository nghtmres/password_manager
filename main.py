import json
import secrets
import string
from cryptography.fernet import Fernet

def load_key():
    with open("secret.key", "rb") as file:
        return file.read()

key = load_key()
cipher = Fernet(key)

def add_password():
        
    service = input("Enter the service name: ").strip().title()
    username = input("Enter the username: ").strip()

    choice = input("Do you want to generate a password? (y/n): ").strip().lower()

    if choice == "y":
        password = generate_password()

        if password is None:
            return
        
    else:
        password = input("Enter the password: ").strip()

    encrypted_password = cipher.encrypt(password.encode()).decode()
    passwords.append({
        "service": service,
        "username": username,
        "password": encrypted_password
    })

    save_passwords()
    print(f"Password for {service} added successfully.")

def view_passwords():

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
        print("No saved passwords found.")
        return []

def save_passwords():
    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

def search_passwords():
    if not passwords:
        print("No saved accounts.")
        return
    
    search_term = input("Enter the service name to search: ").strip().title()

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

def edit_password():
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

passwords = load_passwords()

def main():

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
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            search_passwords()
        elif choice == "4":
            delete_password()
        elif choice == "5":
            edit_password()
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

