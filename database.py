import aiosqlite
from models import Employee
from typing import List
import time
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        self.db_path = "employees.db"

    async def connect(self):
        """Для SQLite соединение устанавливается автоматически."""
        pass

    async def disconnect(self):
        """Для SQLite соединение закрывается автоматически."""
        pass

    async def create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.execute('''
                CREATE INDEX IF NOT EXISTS idx_gender_fullname
                ON employees(gender, full_name)
            ''')
            await db.commit()


    async def add_employee(self, employee: Employee) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO employees (full_name, birth_date, gender)
                VALUES (?, ?, ?)
            ''', (employee.full_name, employee.birth_date.isoformat(), employee.gender))
            await db.commit()
            return cursor.lastrowid


    async def get_all_employees(self) -> List[tuple]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                SELECT DISTINCT full_name, birth_date, gender
                FROM employees 
                ORDER BY full_name
            ''')
            rows = await cursor.fetchall()

            # Преобразуем строку даты обратно в объект date
            result = []
            for row in rows:
                full_name, birth_date_str, gender = row
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
                result.append((full_name, birth_date, gender))

            return result


    async def bulk_insert_employees(self, employees: List[Employee]):
        async with aiosqlite.connect(self.db_path) as db:
            data = [(emp.full_name, emp.birth_date.isoformat(), emp.gender) for emp in employees]
            await db.executemany('''
                INSERT INTO employees (full_name, birth_date, gender)
                VALUES (?, ?, ?)
            ''', data)
            await db.commit()


    async def find_male_f_surnames(self) -> tuple[List[tuple], float]:
        start_time = time.time()

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                SELECT full_name, birth_date, gender 
                FROM employees 
                WHERE gender = 'Male' AND full_name LIKE 'F%'
            ''')
            rows = await cursor.fetchall()

        end_time = time.time()
        execution_time = end_time - start_time

        return rows, execution_time
