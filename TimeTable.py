import sqlite3
from datetime import datetime, date, timedelta


class TimeTable():
    def __init__(self, filename):
        self.database = filename
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        # словарь classroom_id: number
        self.classrooms = dict()
        self.classrooms_reverse = dict()

        for classroom in (cursor.execute(f"SELECT * from Classrooms").fetchall()):
            self.classrooms[classroom[0]] = classroom[1]
            self.classrooms_reverse[classroom[1]] = classroom[0]


        # словарь teacher_id: ФИО
        self.teachers = dict()
        self.teachers_reverse = dict()
        for teacher in (cursor.execute(f"SELECT * from Teachers").fetchall()):
            self.teachers[teacher[0]] = teacher[1]
            self.teachers_reverse[teacher[1]] = teacher[0]

        # словарь discip_id: name
        self.disciplines = dict()
        self.disciplines_reverse = dict()

        for discipline in (cursor.execute(f"SELECT * from Disciplines").fetchall()):
            self.disciplines[discipline[0]] = discipline[1]
            self.disciplines_reverse[discipline[1]] = discipline[0]




        # словарь всех классов
        self.classes = dict()
        for clas in (cursor.execute(f"SELECT * from Classes").fetchall()):
            self.classes[clas[0]] = {'allDay': clas[7],
                                     'discipline': self.disciplines[clas[2]],
                                     'classroom': self.classrooms[clas[1]],
                                     'start_datetime': clas[3],
                                     'end_datetime': clas[4],
                                     'teacher': self.teachers[clas[5]],
                                     'colour': clas[6],
                                     'class_id': clas[0]
                                     }


        connection.close()


    def classroom_timetable(self, classroom):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(f"select * from classes where classroom in (select classroom_id from classrooms where number = {classroom})")
        data = cursor.fetchall()
        data = [list(i) for i in data]
        timetable = []
        for clas in data:
            timetable.append((datetime.strptime(clas[3], "%H:%M"),datetime.strptime(clas[4], "%H:%M")))

        connection.close()
        return timetable


    def get_events(self):
        self.__init__(self.database)
        events = []
        for clas in self.classes.values():
            events.append({
                'allDay': bool(clas['allDay']),
                'title': clas['discipline'],
                'start': clas['start_datetime'],
                'end': clas['end_datetime'],
                'classNames': [clas['colour']],
                'extendedProps': {'context': 'TODO'},
                'classroom': clas['classroom'],
                'teacher': clas['teacher'],
                'class_id': clas['class_id']

            }
            )
        return events


    def add_event(self, event):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        query = """
        INSERT INTO Classes (
            classroom, 
            discipline, 
            start_datetime, 
            end_datetime, 
            teacher, 
            colour, 
            allDay
        ) VALUES (
            :classroom, 
            :discipline, 
            :start, 
            :end, 
            :teacher, 
            :colour, 
            :allDay
        )
        """
        params = {
            'classroom': self.classrooms_reverse[event['classroom']],
            'discipline': self.disciplines_reverse[event['title']],
            'start': datetime.strptime(event['start'], "%Y-%m-%dT%H:%M:%S").isoformat(),
            'end': event['end'],
            'teacher': self.teachers_reverse[event['teacher']],
            'colour': event['classNames'],
            'allDay': 0
        }
        # cursor.execute(f"INSERT INTO Classes (classroom, discipline, start_datetime, end_datetime, teacher, colour, allDay) VALUES ({event['classroom']}, {event['title']}, {event['start']}, {event['end']}, {event['teacher']}, {event['classNames'][0]}, {event['allDay']})")
        cursor.execute(query, params)
        connection.commit()
        connection.close()


    def delete_event(self, id):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Classes WHERE class_id = ?", (id,))
        connection.commit()
        connection.close()

    def teacher_timetable(self, name):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from Classes where teacher in (Select teacher_id from Teachers where ФИО = '{name}')")
        data = cursor.fetchall()
        data = [list(i) for i in data]
        timetable = []
        for clas in data:
            timetable.append((datetime.strptime(clas[3], "%H:%M"), datetime.strptime(clas[4], "%H:%M")))

        connection.close()
        return timetable




    def is_classroom_avail(self, start_time, end_time, classroom):
        start_time = datetime.strptime(start_time, "%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M")

        schedule = self.classroom_timetable(classroom)
        if len(schedule) == 0:
            return True
        if len(schedule) == 1:
            if schedule[0][0] <= start_time <= schedule[0][1] or schedule[0][0] <= end_time <= schedule[0][1] \
                    or (schedule[0][0] >= start_time and schedule[0][1] <= end_time):
                return False
            else:
                return True

        for i in range(1, len(schedule)):
            print(schedule[i])
            if schedule[i - 1][1] >= start_time or end_time >= schedule[i][0]:
                return False
        return True


    def add_class(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        print('Введите название дисциплины: ')
        discipline = input()
        print('Введите номер аудитории: ')
        clas = int(input())
        print('Введите время начала: ')
        start_time = input()
        print('Введите время конца: ')
        end_time = input()

        if self.is_classroom_avail(start_time, end_time, clas):
            print("Выбранное время свободно")
        else:
            print("Выбранное время занято")
            return

        cursor.execute(f"select discip_id from Disciplines where name = '{discipline}'")
        discip_id = cursor.fetchall()[0][0]

        cursor.execute(f"select classroom_id from Classrooms where number = '{clas}'")
        classroom = cursor.fetchall()[0][0]

        cursor.execute(
            f"INSERT INTO Classes (classroom, discipline, start_time, end_time) VALUES ({classroom}, {discip_id}, '{start_time}', '{end_time}')")
        connection.commit()
        connection.close()

