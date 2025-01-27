
import json
import os

class CarNumber:
    def __init__(self, number, price, status="Available"):
        self.number = number
        self.price = price
        self.status = status

    def __str__(self):
        return f"Number: {self.number}, Price: {self.price}, Status: {self.status}"

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(data):
        return CarNumber(**data)


class User:
    def __init__(self, username, address):
        self.username = username
        self.address = address
        self.purchased_numbers = []

    def __str__(self):
        return f"User: {self.username}, Address: {self.address}"

    def to_dict(self):
        return {
            "username": self.username,
            "address": self.address,
            "purchased_numbers": [number.to_dict() for number in self.purchased_numbers]
        }

    @staticmethod
    def from_dict(data):
        user = User(data["username"], data["address"])
        user.purchased_numbers = [CarNumber.from_dict(n) for n in data.get("purchased_numbers", [])]
        return user


class Sale:
    def __init__(self, car_number, user, date):
        self.car_number = car_number
        self.user = user
        self.date = date

    def __str__(self):
        return f"Car: {self.car_number.number}, Buyer: {self.user.username}, Date: {self.date}"

    def to_dict(self):
        return {
            "car_number": self.car_number.to_dict(),
            "user": self.user.to_dict(),
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Sale(
            CarNumber.from_dict(data["car_number"]),
            User.from_dict(data["user"]),
            data["date"]
        )


def save_data(car_numbers, users, sales):
    data = {
        "car_numbers": [number.to_dict() for number in car_numbers],
        "users": [user.to_dict() for user in users],
        "sales": [sale.to_dict() for sale in sales]
    }
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    if not os.path.exists("data.json"):
        save_data([], [], [])

    with open("data.json", "r") as file:
        data = json.load(file)
    return (
        [CarNumber.from_dict(n) for n in data["car_numbers"]],
        [User.from_dict(u) for u in data["users"]],
        [Sale.from_dict(s) for s in data["sales"]]
    )


def admin_menu(car_numbers, users, sales):
    while True:
        admin_choice = input("""
1. Yangi avto raqam qo'shish
2. Avto raqamlarni ko'rish
3. Savdo tarixini ko'rish
4. Chiqish
Tanlovni kiriting: """)

        if admin_choice == "1":
            number = input("Avto raqamni kiriting: ")
            price = float(input("Narxni kiriting: "))
            car_numbers.append(CarNumber(number, price))
            print(f"Avto raqam {number} qo'shildi.")
            save_data(car_numbers, users, sales)
        elif admin_choice == "2":
            print("\n".join(map(str, car_numbers)))
        elif admin_choice == "3":
            print("\n".join(map(str, sales)))
        elif admin_choice == "4":
            break
        else:
            print("Noto'g'ri tanlov!")


def user_menu(user, car_numbers, sales):
    while True:
        user_choice = input("""
1. Avto raqamlarni ko'rish
2. Avto raqam sotib olish
3. Sotib olingan avto raqamlarni ko'rish
4. Chiqish
Tanlovni kiriting: """)

        if user_choice == "1":
            print("\n".join(map(str, car_numbers)))
        elif user_choice == "2":
            number_id = input("Sotib olish uchun avto raqamni kiriting: ")
            number = next((n for n in car_numbers if n.number == number_id and n.status == "Available"), None)
            if number:
                print(f"Avto raqam {number.number} sotib olindi!")
                number.status = "Sold"
                user.purchased_numbers.append(number)
                sales.append(Sale(number, user, "2025-01-09"))
                save_data(car_numbers, [user], sales)
            else:
                print("Avto raqam mavjud emas.")
        elif user_choice == "3":
            print("\n".join(map(str, user.purchased_numbers)))
        elif user_choice == "4":
            break
        else:
            print("Noto'g'ri tanlov!")


def main():
    car_numbers, users, sales = load_data()

    while True:
        print("\nAvto Raqam Savdosi Tizimiga Xush Kelibsiz")
        choice = input("""
1. Admin sifatida kirish
2. Foydalanuvchi sifatida kirish
3. Chiqish
Tanlovni kiriting: """)

        if choice == "1":
            admin_username = input("Admin foydalanuvchi nomi: ")
            admin_password = input("Admin paroli: ")
            if admin_username == "admin" and admin_password == "admin123":
                admin_menu(car_numbers, users, sales)
            else:
                print("Foydalanuvchi nomi yoki parol noto'g'ri.")

        elif choice == "2":
            user_action = input("""
1. Foydalanuvchi nomi bilan kirish
2. Yangi foydalanuvchi yaratish
Tanlovni kiriting: """)

            if user_action == "1":
                username = input("Foydalanuvchi nomingizni kiriting: ")
                user = next((u for u in users if u.username == username), None)
                if user:
                    print(f"Xush kelibsiz, {user.username}!")
                    user_menu(user, car_numbers, sales)
                else:
                    print("Foydalanuvchi topilmadi.")
            elif user_action == "2":
                username = input("Yangi foydalanuvchi nomini kiriting: ")
                address = input("Manzilingizni kiriting: ")
                user = User(username, address)
                users.append(user)
                print(f"Yangi foydalanuvchi yaratildi: {user.username}")
                save_data(car_numbers, users, sales)
            else:
                print("Noto'g'ri tanlov!")

        elif choice == "3":
            print("Tizimdan chiqilmoqda.")
            break
        else:
            print("Noto'g'ri tanlov!")


if __name__ == "__main__":
    main()

