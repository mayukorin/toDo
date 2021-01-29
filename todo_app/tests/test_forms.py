from django.test import TestCase
from todo_app.models.siteUser import SiteUser
from todo_app.forms.siteUserForm import SiteUserLoginForm, SiteUserUpdateForm
from todo_app.forms.taskForm import TaskRegisterForm


class TestSiteUserLoginForm(TestCase):
    def test_clean_username(self):
        
        form = SiteUserLoginForm({"username": "", "password": "abc"})
        self.assertFalse(form.is_valid())

    def test_clean_password(self):

        form = SiteUserLoginForm({"username": "user", "password": ""})

        self.assertFalse(form.is_valid())

    def test_clean_username_and_clean_password(self):

        form = SiteUserLoginForm({"username": "", "password": ""})

        self.assertFalse(form.is_valid())

    def test_clean(self):

        form = SiteUserLoginForm({"username": "user", "password": "abc"})
        self.assertFalse(form.is_valid())

        SiteUser.objects.create_user(username="user", password="abc")
        form = SiteUserLoginForm({"username": "user", "password": "abc"})
        self.assertTrue(form.is_valid())


class TestSiteUserUpdateForm(TestCase):
    def test_clean_username(self):

        form = SiteUserUpdateForm({"username": "", "password": "abc"})
        self.assertFalse(form.is_valid())


class TestTaskRegisterForm(TestCase):
    def test_clean_title(self):

        form = TaskRegisterForm({"title": "", "content": "", "deadline": ""})

        self.assertFalse(form.is_valid())
        form = TaskRegisterForm({"title": "abc", "content": "", "deadline": ""})

        self.assertTrue(form.is_valid())

    def test_deadline_input_formats(self):

        form = TaskRegisterForm(
            {"title": "abc", "content": "", "deadline": "2020-11-10T13:10"}
        )
        self.assertTrue(form.is_valid())
