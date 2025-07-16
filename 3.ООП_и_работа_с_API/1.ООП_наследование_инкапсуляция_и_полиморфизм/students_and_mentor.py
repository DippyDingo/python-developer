class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and
                course in lecturer.courses_attached and
                course in self.courses_in_progress):

            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _average_rating(self):
        """Рассчитывает среднюю оценку из всех курсов (с исправлением)"""
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0

    def __str__(self):
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        avg_rating = self._average_rating()
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_rating:.1f}\n"
                f"Курсы в процессе изучения: {courses_in_progress}\n"
                f"Завершенные курсы: {finished_courses}")

    # Методы сравнения студентов по средней оценке
    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_rating() < other._average_rating()

    def __le__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_rating() <= other._average_rating()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_rating() == other._average_rating()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_rating(self):
        """Рассчитывает среднюю оценку за лекции"""
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        avg_rating = self._average_rating()
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg_rating:.1f}")

    # Методы сравнения лекторов по средней оценке
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_rating() < other._average_rating()

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_rating() <= other._average_rating()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_rating() == other._average_rating()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):

            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# Тестирование
if __name__ == "__main__":
    # Создаем объекты
    student1 = Student('Руби', 'Фокс', 'Жен')
    student1.courses_in_progress = ['Python', 'Git']
    student1.finished_courses = ['Введение в программирование']

    student2 = Student('Алиса', 'Смит', 'Жен')
    student2.courses_in_progress = ['Python', 'Java']

    lecturer1 = Lecturer('Джони', 'Деп')
    lecturer1.courses_attached = ['Python']

    lecturer2 = Lecturer('Алекмей', 'Смирнов')
    lecturer2.courses_attached = ['Python']

    reviewer = Reviewer('Иван', 'Перышкин')
    reviewer.courses_attached = ['Python']

    # Выставляем оценки (с реальными курсами)
    reviewer.rate_hw(student1, 'Python', 9)
    reviewer.rate_hw(student1, 'Python', 10)
    reviewer.rate_hw(student2, 'Python', 8)

    student1.rate_lecture(lecturer1, 'Python', 10)
    student2.rate_lecture(lecturer1, 'Python', 9)
    student1.rate_lecture(lecturer2, 'Python', 8)

    # Проверка __str__
    print("=== Reviewer ===")
    print(reviewer)
    print("\n=== Lecturer 1 ===")
    print(lecturer1)
    print("\n=== Lecturer 2 ===")
    print(lecturer2)
    print("\n=== Student 1 ===")
    print(student1)
    print("\n=== Student 2 ===")
    print(student2)

    # Проверка сравнений
    print("\n=== Сравнения ===")
    print("Лекторы:", lecturer1 > lecturer2)  # True (9.5 > 8)
    print("Студенты:", student1 > student2)  # True (9.5 > 8)
    print("Лекторы равны:", lecturer1 == lecturer2)  # False