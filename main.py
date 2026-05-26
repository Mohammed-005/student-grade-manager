import json

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def get_grade(self):
        if 90 <= self.marks <= 100:
            return 'A'
        elif 75 <= self.marks < 90:
            return 'B'
        elif 60 <= self.marks < 70:
            return 'C'
        elif 40 <= self.marks < 60:
            return 'D'
        else:
            return 'F'

    def to_dict(self):
        return {'name': self.name, 'marks': self.marks}

    @staticmethod
    def from_dict(data):
        return Student(data['name'], data['marks'])


class GradeManager:
    def __init__(self, filename="students.json"):
        self.students = {}
        self.filename = filename
        self.load()

    def add_student(self, name, marks):
        if name in self.students:
            return False
        self.students[name] = Student(name, marks)
        return True

    def get_all_students(self):
        return list(self.students.values())

    def search_student(self, name):
        return self.students.get(name)

    def delete_student(self, name):
        return self.students.pop(name, None)

    def get_topper(self):
        if not self.students:
            return None
        return max(self.students.values(), key=lambda s: s.marks)

    def save(self):
        data = [s.to_dict() for s in self.students.values()]
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for item in data:
                    student = Student.from_dict(item)
                    self.students[student.name] = student
        except FileNotFoundError:
            pass


class CLI:
    def __init__(self):
        self.manager = GradeManager()

    def run(self):
        while True:
            print("\n--- Student Grade Manager ---")
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Delete Student")
            print("5. Show Topper")
            print("6. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                name = input("Enter name: ")
                try:
                    marks = float(input("Enter marks: "))
                    success = self.manager.add_student(name, marks)
                    print("Added" if success else "Already exists")
                except ValueError:
                    print("Invalid marks")

            elif choice == "2":
                students = self.manager.get_all_students()
                if not students:
                    print("No students found")
                for s in students:
                    print(f"{s.name} | {s.marks} | {s.get_grade()}")

            elif choice == "3":
                name = input("Enter name: ")
                student = self.manager.search_student(name)
                if student:
                    print(f"{student.name} | {student.marks} | {student.get_grade()}")
                else:
                    print("Not found")

            elif choice == "4":
                name = input("Enter name: ")
                result = self.manager.delete_student(name)
                print("Deleted" if result else "Not found")

            elif choice == "5":
                topper = self.manager.get_topper()
                if topper:
                    print(f"Topper: {topper.name} ({topper.marks})")
                else:
                    print("No data")

            elif choice == "6":
                self.manager.save()
                print("Saved. Exiting...")
                break

            else:
                print("Invalid choice")


if __name__ == "__main__":
    CLI().run()