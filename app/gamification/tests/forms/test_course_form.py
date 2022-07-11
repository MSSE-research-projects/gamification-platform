from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from app.gamification.forms import CourseForm


class CourseFormTest(TestCase):
    def test_upload_file_with_valid_extension(self):
        filename = 'app/gamification/tests/files/course_file.json'
        file = open(filename, 'rb')
        file = SimpleUploadedFile(filename, file.read())
        form = CourseForm(files={'file': file})

        self.assertTrue(form.is_valid())

    def test_upload_file_with_invalid_extension(self):
        filename = 'app/gamification/tests/files/course_file.txt'
        file = open(filename, 'rb')
        file = SimpleUploadedFile(filename, file.read())
        form = CourseForm(files={'file': file})

        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)

    def test_upload_file_with_valid_format(self):
        filename = 'app/gamification/tests/files/course_file.json'
        file = open(filename, 'rb')
        file = SimpleUploadedFile(filename, file.read())
        form = CourseForm(files={'file': file})

        self.assertTrue(form.is_valid())

    def test_upload_file_with_invalid_format(self):
        filename = 'app/gamification/tests/files/invalid_format.json'
        file = open(filename, 'rb')
        file = SimpleUploadedFile(filename, file.read())
        form = CourseForm(files={'file': file})

        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)
