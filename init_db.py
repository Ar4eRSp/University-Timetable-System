import sqlite3


def init_database():
    conn = sqlite3.connect('TimeTableTest.db')
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Classrooms (
        classroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ФИО TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Disciplines (
        discip_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Classes (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        classroom INTEGER NOT NULL,
        discipline INTEGER NOT NULL,
        start_datetime TEXT NOT NULL,
        end_datetime TEXT NOT NULL,
        teacher INTEGER NOT NULL,
        colour TEXT NOT NULL,
        allDay INTEGER DEFAULT 0,
        FOREIGN KEY (classroom) REFERENCES Classrooms(classroom_id),
        FOREIGN KEY (discipline) REFERENCES Disciplines(discip_id),
        FOREIGN KEY (teacher) REFERENCES Teachers(teacher_id)
    )
    ''')

    # Добавление тестовых данных
    test_data = [
        # Аудитории
        ("INSERT INTO Classrooms (number) VALUES ('101')"),
        ("INSERT INTO Classrooms (number) VALUES ('202')"),
        ("INSERT INTO Classrooms (number) VALUES ('305')"),

        # Преподаватели
        ("INSERT INTO Teachers (ФИО) VALUES ('Иванов Иван Иванович')"),
        ("INSERT INTO Teachers (ФИО) VALUES ('Петрова Мария Сергеевна')"),
        ("INSERT INTO Teachers (ФИО) VALUES ('Сидоров Алексей Викторович')"),

        # Дисциплины
        ("INSERT INTO Disciplines (name) VALUES ('Математика')"),
        ("INSERT INTO Disciplines (name) VALUES ('Физика')"),
        ("INSERT INTO Disciplines (name) VALUES ('Информатика')"),
        ("INSERT INTO Disciplines (name) VALUES ('История')"),

        # Пример занятия
        ("""
        INSERT INTO Classes (classroom, discipline, start_datetime, end_datetime, teacher, colour, allDay) 
        VALUES (
            1, 
            1, 
            '2025-06-25T09:00:00', 
            '2023-06-25T10:30:00', 
            1, 
            'bg-gradient-primary', 
            0
        )
        """)
    ]

    for query in test_data:
        try:
            cursor.execute(query)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print("База данных успешно инициализирована!")


if __name__ == "__main__":
    init_database()