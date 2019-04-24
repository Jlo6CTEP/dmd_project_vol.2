import json
import os
import re
from random import sample, randint

from backend.db_manager.db_manager import db

students_number = 3000
teachers_number = 100
courses_number = 100
courses_per_student = [2, 4]

names = sample(open('../test_data/first_name.txt').read().split(','), students_number + teachers_number)
surnames = sample(open('../test_data/last_name.txt').read().split(','), students_number + teachers_number)
courses = sample(set(open('../test_data/courses.txt').read().split(',')), courses_number)

regex = re.compile('[^a-zA-Z]')
for x in courses:
    dic = {
        "name": x,
        "description": x,
        "assessment": ['mid', 'final']
    }
    db.insert_course(dic)
    print('Course {} added'.format(x))

grades_values = ['F', 'D', 'C', 'B', 'A']

for x in range(students_number + teachers_number):
    name = regex.sub('', names[x])
    surname = regex.sub('', surnames[x])
    dic = {"name": name,
           "surname": surname,
           "login": name[0] + surname, "password": name[0] + surname,
           "courses": sample(courses, randint(*courses_per_student)),
           "registration date": '{}/{}/20{}'.format(randint(1, 12), randint(1, 28), randint(16, 19)),
           "role": "student" if x < students_number else "teacher"}
    key = db.insert_user(name[0] + '.' + surname, dic)
    for f in dic['courses']:
        db.edit_assessment_grade(key, f, {'mid': sample(grades_values, 1)[0]})
        db.edit_assessment_grade(key, f, {'final': sample(grades_values, 1)[0]})

    print("{} {} added".format("student" if x < students_number else "teacher", name + ' ' + surname))