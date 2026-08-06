import json

def add_password():
    service = input("Enter the service name: ").strip().title()
    username = input("Enter the username: ").strip()
    password = input("Enter the password: ").strip()

    passwords.append({
        "service": service,
        "username": username,
        "password": password
    })
    save_passwords()
    print(f"Password for {service} added successfully.")

def view_passwords():

    if not passwords:
        print("No saved accounts.")
        return

    print("\nSaved Accounts:")
    for idx, entry in enumerate(passwords, start=1):
        print(f"{idx}. Service: {entry["service"]}, Username: {entry["username"]}, Password: {entry["password"]}")

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
            print(
                f"Service: {entry['service']}, "
                f"Username: {entry['username']}, "
                f"Password: {entry['password']}"
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
            f"Username: {entry['username']}, "
            f"Password: {entry['password']}"
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

passwords = load_passwords()

def main():

    while True:
        print("\nPassword Manager")
        print("1. Add password")
        print("2. View saved accounts")
        print("3. Search passwords")
        print("4. Delete password")
        print("5. Exit")

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
            save_passwords()
            print("Exiting the program.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()