from typing import List, Tuple
from hw_01 import normalize_phone

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found. Enter a valid user name."
        except IndexError:
            return "Enter user name please."

    return inner

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args: List[str], contacts: dict) -> str:
    name, phone = args
    contacts[name] = normalize_phone(phone)
    return "Contact added."

@input_error
def change_contact(args: List[str], contacts: dict) -> str:
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = normalize_phone(phone)
    return "Contact updated."

@input_error
def show_phone(args: List[str], contacts: dict) -> str:
    name = args[0]
    return f"{name}: {contacts[name]}"

@input_error
def show_all(contacts: dict) -> str:
    if not contacts:
        return "No contacts saved yet."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input = input("Enter a command: ")
            if not user_input.strip():
                continue
            command, args = parse_input(user_input)
            match command:
                case "close" | "exit":
                    print("Good bye!")
                    break
                case "hello":
                    print("How can I help you?")
                case "add":
                    print(add_contact(args, contacts))
                case "change":
                    print(change_contact(args, contacts))
                case "phone":
                    print(show_phone(args, contacts))
                case "all":
                    print(show_all(contacts))
                case _:
                    print("Invalid command.")

        except (KeyboardInterrupt, EOFError):
            print("\nGood bye!")
            break

if __name__ == "__main__":
    main()