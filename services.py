import random
from datetime import date, timedelta
from models import Employee
from typing import List


class EmployeeService:
    FIRST_NAMES_MALE = ["Ivan", "Petr", "Sergey", "Alexander", "Dmitry", "Alexey", "Maxim"]
    FIRST_NAMES_FEMALE = ["Anna", "Maria", "Elena", "Olga", "Irina", "Natalia", "Svetlana"]
    LAST_NAMES = ["Ivanov", "Petrov", "Sidorov", "Smirnov", "Kuznetsov", "Popov", "Volkov"]
    MIDDLE_NAMES_MALE = ["Ivanovich", "Petrovich", "Sergeevich", "Alexandrovich"]
    MIDDLE_NAMES_FEMALE = ["Ivanovna", "Petrovna", "Sergeevna", "Alexandrovna"]

    @staticmethod
    def generate_random_employee() -> Employee:
        gender = random.choice(["Male", "Female"])

        if gender == "Male":
            first_name = random.choice(EmployeeService.FIRST_NAMES_MALE)
            last_name = random.choice(EmployeeService.LAST_NAMES)
            middle_name = random.choice(EmployeeService.MIDDLE_NAMES_MALE)
        else:
            first_name = random.choice(EmployeeService.FIRST_NAMES_FEMALE)
            last_name = random.choice(EmployeeService.LAST_NAMES)
            middle_name = random.choice(EmployeeService.MIDDLE_NAMES_FEMALE)

        full_name = f"{last_name} {first_name} {middle_name}"

        end_date = date.today() - timedelta(days=18*365)
        start_date = end_date - timedelta(days=(65-18)*365)
        random_days = random.randint(0, (end_date - start_date).days)
        birth_date = start_date + timedelta(days=random_days)

        return Employee(full_name, birth_date, gender)

    @staticmethod
    def generate_specific_employees(count: int) -> List[Employee]:
        employees = []
        first_names = ["Fred", "Frank", "Felix", "Ford", "Finn"]
        last_names = ["Fisher", "Fletcher", "Foster", "Ford", "Fox"]

        for _ in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            middle_name = random.choice(["James", "John", "Robert", "Michael"])
            full_name = f"{last_name} {first_name} {middle_name}"

            end_date = date.today() - timedelta(days=18*365)
            start_date = end_date - timedelta(days=(65-18)*365)
            random_days = random.randint(0, (end_date - start_date).days)
            birth_date = start_date + timedelta(days=random_days)

            employees.append(Employee(full_name, birth_date, "Male"))

        return employees
