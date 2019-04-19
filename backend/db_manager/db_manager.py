from pyArango.connection import Connection
from pyArango.theExceptions import DocumentNotFoundError

entries_to_remove = ('_id', '_rev')

levels = {f[0]: f[1] for f in enumerate(['student', 'teacher', 'principal', 'admin'])}


def purge_doc(doc):
    for x in entries_to_remove:
        doc.pop(x)
    return doc


class DbManager:
    db = None

    def __init__(self):
        self.db = Connection('http://159.65.116.45:8529', 'mason', 'mazzara')['e-sas']

    def get_by_credentials(self, login, password):
        for doc in self.db.collections['user'].fetchAll(rawResults=True):
            if doc['login'] == login and doc['password'] == password:
                purge_doc(doc)
                doc['role'] = levels[doc['level']]
                return doc.pop('_key'), doc
        return None

    def get_assessment(self, course):
        return self.db.collections['course'][course]['assessment']

    def get_student_assessment(self, student, course):
        try:
            doc = purge_doc(self.db.collections['grades'][student + '_' + course].getStore())
        except DocumentNotFoundError:
            course = self.get_course_info(course)[1]
            doc = {x[0]: x[1] for x in zip(course['assessment'], ['']*len(course))}
            return None, doc
        return doc.pop('_key'), doc

    def get_course_info(self, course):
        doc = purge_doc(self.db.collections['course'][course].getStore())
        return doc.pop('_key'), doc

    def get_user_courses(self, user):
        doc = self.db.collections['user'][user]['courses']
        user_courses = []
        for x in doc:
            user_courses.append(self.get_course_info(x))
        return user_courses


db = DbManager()
print(db.get_user_courses('e.noor'))
print()
