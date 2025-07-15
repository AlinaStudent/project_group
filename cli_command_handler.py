# cli/command_handler.py

from models.contact import Contact
from services.contact_book import ContactBook
from services.note_book import NoteBook
from utils.utils import load_data, save_data

def run_command_loop():
    contact_book = ContactBook()
    # Завантажуємо контакти з файлу, якщо є
    data = load_data("addressbook.pkl")
    if data:
        contact_book.contacts = data

    note_book = NoteBook()
    # Завантажуємо нотатки з файлу, якщо є
    notes = load_data("notes.pkl")
    if notes:
        note_book.notes = notes

    print("Welcome! Enter a command:")

    while True:
        cmd = input(">>> ").strip().lower()
        # Команди для виходу
        if cmd in ("exit", "close"):
            # Зберігаємо перед виходом
            save_data(contact_book.contacts, "addressbook.pkl")
            save_data(note_book.notes, "notes.pkl")
            print("Good bye!")
            break

        # Інші обробники команд (add, search contact/note) тут...

        # Обробка команди show birthdays <days>
        elif cmd.startswith("show birthdays"):
            parts = cmd.split()
            # Перевіряємо, чи введено три частини і третя — число
            if len(parts) != 3 or not parts[2].isdigit():
                print("Usage: show birthdays <days>")
                continue

            days = int(parts[2])
            # Дні мають бути невід’ємні
            if days < 0:
                print("Please enter a non-negative integer for days.")
                continue

            # Отримуємо список майбутніх днів народження
            upcoming = contact_book.get_birthdays_in(days)
            if not upcoming:
                print(f"No birthdays in the next {days} days.")
            else:
                print("Upcoming birthdays:")
                # Виводимо кожен контакт і дату привітання
                for name, date in upcoming:
                    print(f"{name}: {date.strftime('%Y-%m-%d')}")

        else:
            # Невідома команда
            print("Unknown command. Try again.")