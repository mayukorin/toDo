from django.test import TestCase
from todo_app.models.task import Task
from django.urls import reverse


class ToDoAppTest(TestCase):
    def setUp(self):

        response = self.client.post(
            reverse("todo_app:siteUser_register"),
            {"username": "test", "password": "abc", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("todo_app:siteUser_login"),
            status_code=302,
            target_status_code=200,
        )

        response = self.client.post(
            reverse("todo_app:siteUser_register"),
            {"username": "test2", "password": "abc", },
            follow=True,
        )

        response = self.client.post(
            reverse("todo_app:siteUser_login"),
            {"username": "test", "password": "abc", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("todo_app:task_list", kwargs={"page": 1}),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_site_user_login_and_logout(self):

        response = self.client.get(
            reverse("todo_app:siteUser_logout", kwargs={"from_flag": 0}), follow=True
        )
        self.assertRedirects(
            response,
            reverse("todo_app:siteUser_login"),
            status_code=302,
            target_status_code=200,
        )
        self.assertContains(response, "ログアウトしました")
        self.assertFalse(response.context["user"].is_authenticated)

    def test_site_user_login_and_update(self):

        response = self.client.post(
            reverse("todo_app:siteUser_update"),
            {"username": "siteuser3", "password": "", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("todo_app:siteUser_login"),
            status_code=302,
            target_status_code=200,
        )
        self.assertContains(response, "会員情報の更新が完了しました")
        self.assertFalse(response.context["user"].is_authenticated)

        response = self.client.post(
            reverse("todo_app:siteUser_login"),
            {"username": "siteuser3", "password": "abc", },
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse("todo_app:task_list", kwargs={"page": 1}),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_site_user_login_and_task_register_and_update_and_delete(self):

        response = self.client.post(
            reverse("todo_app:task_register"),
            {"title": "task1", "content": "abc", "deadline": "2020-05-10T12:12", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("todo_app:task_list", kwargs={"page": 1}),
            status_code=302,
            target_status_code=200,
        )
        self.assertQuerysetEqual(
            response.context["tasks"].object_list, ["<Task: task1>"]
        )
        tasks = Task.objects.all()
        task1 = tasks[0]
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(task1.site_user, response.context["user"])

        response = self.client.post(
            reverse("todo_app:task_update", kwargs={"task_id": task1.id}),
            {"title": "task2", "content": "abc", "deadline": "2020-05-10T12:12", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("todo_app:task_list", kwargs={"page": 1}),
            status_code=302,
            target_status_code=200,
        )
        self.assertQuerysetEqual(
            response.context["tasks"].object_list, ["<Task: task2>"]
        )
        tasks = Task.objects.all()
        task1 = tasks[0]
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(task1.site_user, response.context["user"])

        response = self.client.post(
            reverse("todo_app:task_delete", kwargs={"task_id": task1.id}), follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                "todo_app:task_list", kwargs={"page": self.client.session.get("page")}
            ),
            status_code=302,
            target_status_code=200,
        )
        self.assertQuerysetEqual(response.context["tasks"].object_list, [])

    def test_another_site_user_task(self):

        response = self.client.post(
            reverse("todo_app:task_register"),
            {"title": "task1", "content": "abc", "deadline": "2020-05-10T12:12", },
            follow=True,
        )
        tasks = Task.objects.all()
        task1 = tasks[0]
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(task1.site_user.username, "test")
        self.assertRedirects(
            response,
            reverse("todo_app:task_list", kwargs={"page": 1}),
            status_code=302,
            target_status_code=200,
        )
        self.assertQuerysetEqual(
            response.context["tasks"].object_list, ["<Task: task1>"]
        )
        response = self.client.get(
            reverse("todo_app:siteUser_logout", kwargs={"from_flag": 0}), follow=True
        )

        response = self.client.post(
            reverse("todo_app:siteUser_login"),
            {"username": "test2", "password": "abc", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                "todo_app:task_list", kwargs={"page": self.client.session.get("page")}
            ),
            status_code=302,
            target_status_code=200,
        )
        self.assertQuerysetEqual(response.context["tasks"].object_list, [])
