from django.db import models

class CourseManager(models.Manager):
    def get_by_natural_key(self, course_name, university_name):
        return self.get(course_name=course_name, university_name=university_name)

class UniversityManager(models.Manager):
    def get_by_natural_key(self, university_name):
        return self.get(university_name=university_name)

