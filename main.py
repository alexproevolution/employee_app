import asyncio
import sys
from datetime import datetime
from database import DatabaseManager
from models import Employee
from services import EmployeeService


class EmployeeApplication:
    def __init__(self):
        self.db = DatabaseManager()

    async def initialize(self):
        await self.db.connect()

    async def cleanup(self):
        await self.db.disconnect()

    async def mode_create_table(self):
        await self.db.create_table()
        print("Table 'employees' created successfully")

    async def mode_add_employee(self, args: list):
        if len(args) < 3:
            print("Usage: myApp 2 \"Full Name\" YYYY-MM-DD Gender")
            return

        full_name = args[0]
        birth_date = datetime.strptime(args[1], "%Y-%m-%d").date()
        gender = args[2]

        employee = Employee(full_name, birth_date, gender)
        employee_id = await self.db.add_employee(employee)

        print(f"Employee added successfully with ID: {employee_id}")
        print(f"Age: {employee.calculate_age()} years")

    async def mode_show_all(self):
        employees = await self.db.get_all_employees()

        print(f"{'Full Name':<30} {'Birth Date':<12} {'Gender':<8} {'Age':<4}")
        print("-" * 60)

        for full_name, birth_date, gender in employees:
            emp = Employee(full_name, birth_date, gender)
            age = emp.calculate_age()
            print(f"{full_name:<30} {birth_date:<12} {gender:<8} {age:<4}")

    async def mode_generate_data(self):
        print("Generating 1,000,000 random employees...")

        batch_size = 10000
        total_generated = 0

        for i in range(0, 1000000, batch_size):
            batch = [EmployeeService.generate_random_employee() for _ in range(batch_size)]
            await self.db.bulk_insert_employees(batch)
            total_generated += len(batch)
            print(f"Generated {total_generated} employees...")

        print("Generating 100 specific employees...")
        specific_employees = EmployeeService.generate_specific_employees(100)
        await self.db.bulk_insert_employees(specific_employees)

        print("Data generation completed successfully!")

    async def mode_search_male_f(self):
        results, execution_time = await self.db.find_male_f_surnames()

        print(f"Found {len(results)} employees:")
        for full_name, birth_date, gender in results[:10]:
            print(f"  {full_name} | {birth_date} | {gender}")

        if len(results) > 10:
            print(f"  ... and {len(results) - 10} more")

        print(f"Execution time: {execution_time:.4f} seconds")

    async def run(self):
        if len(sys.argv) < 2:
            print("Usage: python main.py <mode> [arguments]")
            print("Modes: 1-create table, 2-add employee, 3-show all, 4-generate data, 5-search male F")
            return

        mode = sys.argv[1]
        args = sys.argv[2:]

        try:
            await self.initialize()

            if mode == "1":
                await self.mode_create_table()
            elif mode == "2":
                await self.mode_add_employee(args)
            elif mode == "3":
                await self.mode_show_all()
            elif mode == "4":
                await self.mode_generate_data()
            elif mode == "5":
                await self.mode_search_male_f()
            else:
                print(f"Unknown mode: {mode}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await self.cleanup()

if __name__ == "__main__":
    app = EmployeeApplication()
    asyncio.run(app.run())
