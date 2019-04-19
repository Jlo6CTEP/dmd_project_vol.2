from frontend.assessment_widgets.student_assessment import StudentAssessment
from frontend.course_widgets.uneditable_course import UnEditableCourse
from frontend.courses_page import CoursePage
from frontend.user_pages.base_user_page import BasePage
from backend.db_manager.db_manager import db


class StudentPage(BasePage):

    def __init__(self, parent, user=None):
        super().__init__(parent, user)

        course_info = db.get_user_courses(user.user_id)
        courses_page = CoursePage(2)

        for x in course_info:
            assessment = StudentAssessment(user.user_id, x[0])
            course_widget = UnEditableCourse(x[0], assessment)
            courses_page.add_course(course_widget)
        self.pages.addTab(courses_page, 'My Courses')
