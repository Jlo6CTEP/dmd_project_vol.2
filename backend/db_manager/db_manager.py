from pyArango.connection import Connection
from pyArango.theExceptions import DocumentNotFoundError

from backend.db_manager.documents_structure import course as course_schema

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

    def remove_assessment(self, course, assessment):
        print(course, assessment)

    def update_assessment(self, course, assessment, new_value):
        print(course, assessment, new_value)

    def add_assessment(self, course, assessment):
        print(course, assessment)

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
        print(user, course, value)

    def get_users_for_admin(self):
        return [purge_doc(x) for x in self.db.collections['user'].fetchAll(rawResults=True)]

    def insert_course(self, course_info):
        doc = self.db.collections['course'].createDocument()
        for x in course_schema:
            doc[x] = course_info[x]
        doc._key = doc['name']
        doc.save()

    def insert_user(self, key, data):
        print(key, data)

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


db = DbManager()

