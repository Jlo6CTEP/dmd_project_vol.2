from pyArango.connection import Connection
from pyArango.theExceptions import DocumentNotFoundError, CreationError

from backend.db_manager.documents_structure import course as course_schema
from backend.db_manager.documents_structure import student as user_schema

student_info_to_show = ['name', 'surname', 'login', 'assessments']

entries_to_remove = ('_id', '_rev')


def purge_doc(doc):
    for x in entries_to_remove:
        doc.pop(x)
    return doc


class DbManager:
    db = None

    def __init__(self):
        self.db = Connection('http://127.0.0.1:8529', 'root', '')['e_sas']

    def get_user_by_credentials(self, login, password):
        for doc in self.db.collections['user'].fetchAll(rawResults=True):
            if doc['login'] == login and doc['password'] == password:
                purge_doc(doc)
                return doc.pop('_key'), doc
        return None, None

    def get_course_assessment(self, course):
        return self.db.collections['course'][course]['assessment']

    def get_student_assessment(self, student, courses):
        assessments = {}
        for course in courses:
            try:
                doc = purge_doc(self.db.collections['grades'][student + '_' + course].getStore())
                assessments.update({doc.pop('_key').split('_')[1]: doc})
            except DocumentNotFoundError:
                pass
        return assessments

    def get_course_info(self, course):
        doc = purge_doc(self.db.collections['course'][course].getStore())
        return doc.pop('_key'), doc

    def get_user_courses(self, user):
        doc = self.db.collections['user'][user]['courses']
        user_courses = []
        for x in doc:
            user_courses.append(self.get_course_info(x))
        return user_courses

    def update_user_info(self, user, info):
        for x in info.items():
            doc = self.db.collections['user'][user]
            doc[x[0]] = x[1]
            doc.patch()

    def get_courses(self):
        return [purge_doc(x) for x in self.db.collections['course'].fetchAll(rawResults=True)]

    def remove_assessment(self, course_name, assessment):
        course = self.db.collections['course'][course_name]
        course['assessment'].remove(assessment)
        for x in self.db.collections['grades'].fetchAll():
            if x['_key'].split('_')[1] == course_name:
                del x[assessment]
                x.save()
        course.save()

    def update_assessment(self, course_name, assessment, new_value):
        new_value = list(new_value.keys())[0]
        course = self.db.collections['course'][course_name]
        course['assessment'].remove(assessment)
        course['assessment'].append(new_value)
        for x in self.db.collections['grades'].fetchAll():
            if x['_key'].split('_')[1] == course_name:
                old = x[assessment]
                del x[assessment]
                x[new_value] = old
                x.save()
        course.save()

    def add_assessment(self, course, assessment):
        course = self.db.collections['course'][course]
        course['assessment'].append(assessment)
        course.save()

    def get_students(self):
        doc = {x.pop('_key'): purge_doc(x) for x in
               self.db.collections['user'].fetchAll(rawResults=True) if x['role'] == 'student'}

        grades = {x.pop('_key'): purge_doc(x) for x in self.db.collections['grades'].fetchAll(rawResults=True)}
        [x[1].update({'assessments': {}}) for x in doc.items()]

        for x in grades.items():
            key = x[0].split('_')
            doc[key[0]]['assessments'].update({key[1]: x[1]})
        return doc

    def get_students_for_teacher(self, teacher):
        courses = self.db.collections['user'][teacher]['courses']
        profiles = {}
        for doc in self.db.collections['user'].fetchAll(rawResults=True):
            if len(set(doc['courses']).intersection(set(courses))) != 0 and doc['role'] == 'student':
                doc.update({'assessments': self.get_student_assessment(doc['_key'], courses)})
                purge_doc(doc)
                profiles.update({doc.pop('_key'): doc})
        return profiles

    def edit_assessment_grade(self, user, course, value):
        key, value = list(value.items())[0]
        if self.db.collections['user'][user]['role'] != 'student':
            return
        doc = self.db.collections['grades'][user + '_' + course]
        doc[key] = value
        doc.save()

    def get_users_for_admin(self):
        return [purge_doc(x) for x in self.db.collections['user'].fetchAll(rawResults=True)]

    def insert_course(self, course_info):
        doc = self.db.collections['course'].createDocument()
        for x in course_schema:
            doc[x] = course_info[x]
        doc._key = doc['name']
        doc.save()

    def insert_user(self, key, data):

        doc = self.db.collections['user'].createDocument()
        for x in user_schema:
            doc[x] = data[x]
        doc._key = key

        counter = 0
        flag = True
        while flag:
            try:
                doc.save()
                flag = False
                if counter != 0:
                    key = key + str(counter)
            except CreationError:
                counter += 1
                doc._key = key + str(counter)

        if data['role'] == 'student':
            for x in data['courses']:
                grade = self.db.collections['grades'].createDocument()
                for f in self.get_course_assessment(x):
                    grade[f] = ''
                grade._key = key + '_' + x
                grade.save()
        return key

    def get_teachers_and_students(self):
        return [purge_doc(x) for x in
                self.db.collections['user'].fetchAll(rawResults=True)
                if x['role'] == 'teacher' or x['role'] == 'student']

    def edit_user_courses(self, user, course_list):
        doc = self.db.collections['user'][user]
        old = set(doc['courses'])
        doc['courses'] = course_list
        new = set(doc['courses'])
        doc.patch()

        if len(old) > len(new):
            for x in old - new:
                try:
                    doc = self.db.collections['grades'][user + '_' + x]
                    doc.delete()
                except DocumentNotFoundError:
                    pass

    def spatial_search(self, student_id):
        try:
            self.db.collections['user'][student_id]
        except DocumentNotFoundError:
            return None
        grades_values = {x[1]: x[0] for x in enumerate(['', 'F', 'D', 'C', 'B', 'A'])}
        users = {x['_key']: [x, 0, 0] for x in self.db.collections['user'].fetchAll(rawResults=True)
                 if x['role'] == 'student'}
        grades = [(x.pop('_key'), purge_doc(x)) for x in self.db.collections['grades'].fetchAll(rawResults=True)]
        for x in grades:
            student = users[x[0].split('_')[0]]
            for f in x[1].values():
                grade = grades_values[f]
                student[1] += grade
                if grade != 0:
                    student[2] += 1
        for x in users.values():
            x.append(x[1] / x[2] if x[2] != 0 else 0)
        users = sorted(users.values(), key=lambda x: x[3])
        user = list(filter(lambda x: users[x][0]['_key'] == student_id, range(len(users))))[0]

        forward = min(user + 1, len(users))
        backward = max(user - 1, 0)

        neighbours = []

        while len(neighbours) < 3:
            forward_diff = abs(users[user][3] - users[forward][3])
            backward_diff = abs(users[user][3] - users[backward][3])

            if forward_diff > backward_diff:
                neighbours.append(users[forward])
                forward = min(forward + 1, len(users))
            else:
                neighbours.append(users[backward])
                backward = max(backward - 1, 0)
        neighbours.insert(0, users[user])

        for x in neighbours:
            purge_doc(x[0])

        return neighbours


db = DbManager()