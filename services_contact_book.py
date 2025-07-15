# services/contact_book.py

from datetime import datetime, timedelta
import re

def is_valid_email(email):
    # Перевіряємо, чи відповідає рядок формату email
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_phone(phone):
    # Перевіряємо, чи складається телефон з 10–15 цифр (може починатися з +)
    return bool(re.match(r"^\+?\d{10,15}$", phone))


class ContactBook:
    def __init__(self):
        # Словник контактів: ключ — ім'я, значення — об'єкт Contact
        self.contacts = {}

    def add_contact(self, contact):
        # Додаємо контакт, якщо email та телефон валідні
        if not is_valid_email(contact.email) or not is_valid_phone(contact.phone):
            raise ValueError("Invalid phone or email")
        self.contacts[contact.name] = contact

    def find(self, name):
        # Повертаємо контакт за ім'ям або None
        return self.contacts.get(name)

    def get_birthdays_in(self, days):
        """
        Повертаємо список (ім'я, дата_привітань) для контактів,
        чиї дні народження наступають протягом `days` днів.
        Якщо день народження випадає на вихідний, переносимо на понеділок.
        """
        today = datetime.today().date()
        upcoming = []

        # Перебираємо всі контакти
        for c in self.contacts.values():
            try:
                # Парсимо рядок з датою народження у форматі YYYY-MM-DD
                bd = datetime.strptime(c.birthday, "%Y-%m-%d").date()
            except ValueError:
                # Якщо формат некоректний — пропускаємо контакт
                continue

            # Обчислюємо наступну появу дня народження:
            # спочатку поточний рік
            next_bd = bd.replace(year=today.year)
            # якщо вже пройшла — беремо наступний рік
            if next_bd < today:
                next_bd = next_bd.replace(year=today.year + 1)

            # Різниця в днях між сьогоденням і наступним днем народження
            delta = (next_bd - today).days

            # Якщо це в межах заданого інтервалу
            if 0 <= delta <= days:
                # Якщо день випадає на суботу (5) — +2 дні до понеділка
                if next_bd.weekday() == 5:
                    next_bd += timedelta(days=2)
                # Якщо на неділю (6) — +1 день до понеділка
                elif next_bd.weekday() == 6:
                    next_bd += timedelta(days=1)

                # Додаємо пару (ім'я, скоригована дата)
                upcoming.append((c.name, next_bd))

        return upcoming

    def search_contacts(self, query):
        # Фільтруємо контакти за підрядком у імені
        return [c for c in self.contacts.values() if query.lower() in c.name.lower()]

    def edit_contact(self, name, **kwargs):
        # Редагуємо дані існуючого контакту
        contact = self.contacts.get(name)
        if not contact:
            return False
        for k, v in kwargs.items():
            setattr(contact, k, v)
        return True

    def delete_contact(self, name):
        # Видаляємо контакт за ім'ям і повертаємо його або None
        return self.contacts.pop(name, None)