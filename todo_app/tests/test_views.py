from django.test import TestCase
from todo_app.models.siteUser import SiteUser
from todo_app.models.task import Task
from django.urls import reverse


def create_task(id, title, content, site_user, done_flag):

    return Task.objects.create(
        id=id, title=title, content=content, site_user=site_user, done_flag=done_flag
    )


class SiteUserRegisterViewTest(TestCase):
    def test_siteUser_register_get(self):

        response = self.client.get(reverse("todo_app:siteUser_register"))
        self.assertTemplateUsed(response, "siteUser/register.html")
        self.assertEqual(response.status_code, 200)

    def test_siteUser_register_post_with_correct_input(self):

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
        siteUsers = SiteUser.objects.all()
        siteUser = siteUsers[0]
        self.assertEqual(siteUsers.count(), 1)
        self.assertEqual(siteUser.username, "test")
        self.assertTrue(siteUser.check_password("abc"))

    def test_siteUser_register_post_with_incorrect_input(self):

        response = self.client.post(
            reverse("todo_app:siteUser_register"),
            {"username": "", "password": "abc", },
            follow=True,
        )
        self.assertFormError(response, "form", "username", "この項目は必須です。")
        self.assertEqual(response.context["form"].data["username"], "")
        self.assertEqual(response.context["form"].data["password"], "abc")
        self.assertTemplateUsed(response, "siteUser/register.html")
        siteUsers = SiteUser.objects.all()
        self.assertEqual(siteUsers.count(), 0)

        response = self.client.post(
            reverse("todo_app:siteUser_register"),
            {"username": "test", "password": "", },
            follow=True,
        )
        self.assertFormError(response, "form", "password", "この項目は必須です。")
        self.assertEqual(response.context["form"].data["username"], "test")
        self.assertEqual(response.context["form"].data["password"], "")
        self.assertTemplateUsed(response, "siteUser/register.html")
        siteUsers = SiteUser.objects.all()
        self.assertEqual(siteUsers.count(), 0)

        response = self.client.post(
            reverse("todo_app:siteUser_register"),
            {"username": "", "password": "", },
            follow=True,
        )
        self.assertFormError(response, "form", "username", "この項目は必須です。")
        self.assertFormError(response, "form", "password", "この項目は必須です。")
        self.assertEqual(response.context["form"].data["username"], "")
        self.assertEqual(response.context["form"].data["password"], "")
        self.assertTemplateUsed(response, "siteUser/register.html")
        siteUsers = SiteUser.objects.all()
        self.assertEqual(siteUsers.count(), 0)


class SiteUserUpdateViewTest(TestCase):
    def setUp(self):

        self.site_user1 = SiteUser.objects.create_user(
            username="siteuser1", password="abc"
        )
        self.client.force_login(self.site_user1)
        self.site_user2 = SiteUser.objects.create_user(
            username="siteuser2", password="abc"
        )

    def test_siteUser_update_get(self):

        response = self.client.get(reverse("todo_app:siteUser_update"))
        self.assertTemplateUsed(response, "siteUser/update.html")
        self.assertEqual(response.status_code, 200)

    def test_siteUser_update_post_with_correct_input(self):

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
        siteUsers = SiteUser.objects.all()
        self.assertEqual(siteUsers.count(), 2)
        siteUser1 = SiteUser.objects.get(pk=self.site_user1.id)
        self.assertEqual(siteUser1.username, "siteuser3")
        self.assertTrue(siteUser1.check_password("abc"))

        self.client.force_login(self.site_user2)
        response = self.client.post(
            reverse("todo_app:siteUser_update"),
            {"username": "siteuser4", "password": "ccc", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("todo_app:siteUser_login"),
            status_code=302,
            target_status_code=200,
        )
        self.assertContains(response, "会員情報の更新が完了しました")
        siteUsers = SiteUser.objects.all()
        self.assertEqual(siteUsers.count(), 2)
        siteUser1 = SiteUser.objects.get(pk=self.site_user2.id)
        self.assertEqual(siteUser1.username, "siteuser4")
        self.assertTrue(siteUser1.check_password("ccc"))

    def test_siteUser_update_post_with_incorrect_input(self):

        response = self.client.post(
            reverse("todo_app:siteUser_update"),
            {"username": "", "password": "cda", },
            follow=True,
        )

        self.assertFormError(response, "form", "username", "名前を入力してください")
        self.assertEqual(response.context["form"].data["username"], "")
        self.assertEqual(response.context["form"].data["password"], "cda")
        self.assertTemplateUsed(response, "siteUser/update.html")
        siteUsers = SiteUser.objects.all()
        self.assertEqual(siteUsers.count(), 2)
        siteUser1 = SiteUser.objects.get(pk=self.site_user1.id)
        self.assertEqual(siteUser1.username, "siteuser1")
        self.assertTrue(siteUser1.check_password("abc"))

        response = self.client.post(
            reverse("todo_app:siteUser_update"),
            {"username": "", "password": "", },
            follow=True,
        )
        self.assertFormError(response, "form", "username", "名前を入力してください")
        self.assertEqual(response.context["form"].data["username"], "")
        self.assertEqual(response.context["form"].data["password"], "")
        self.assertTemplateUsed(response, "siteUser/update.html")
        siteUsers = SiteUser.objects.all()
        self.assertEqual(siteUsers.count(), 2)
        siteUser1 = SiteUser.objects.get(pk=self.site_user1.id)
        self.assertEqual(siteUser1.username, "siteuser1")
        self.assertTrue(siteUser1.check_password("abc"))

        response = self.client.post(
            reverse("todo_app:siteUser_update"),
            {"username": "siteuser2", "password": "cda", },
            follow=True,
        )

        self.assertFormError(response, "form", None, "その名前のユーザーは既に登録されています")
        self.assertEqual(response.context["form"].data["username"], "siteuser2")
        self.assertEqual(response.context["form"].data["password"], "cda")
        self.assertTemplateUsed(response, "siteUser/update.html")
        siteUsers = SiteUser.objects.all()
        self.assertEqual(siteUsers.count(), 2)
        siteUser1 = SiteUser.objects.get(pk=self.site_user1.id)
        self.assertEqual(siteUser1.username, "siteuser1")
        self.assertTrue(siteUser1.check_password("abc"))


class SiteUserLoginViewTest(TestCase):
    def setUp(self):

        self.site_user = SiteUser.objects.create_user(
            username="testuser", password="abc"
        )

    def test_siteUser_login_get(self):

        response = self.client.get(reverse("todo_app:siteUser_login"))
        self.assertTemplateUsed(response, "siteUser/login.html")
        self.assertEqual(response.status_code, 200)

    def test_siteUser_login_post_with_correct_input(self):

        response = self.client.post(
            reverse("todo_app:siteUser_login"),
            {"username": "testuser", "password": "abc", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("todo_app:task_list", kwargs={"page": 1}),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(response.context["user"].username, "testuser")

    def test_siteUser_login_post_with_incorrect_input(self):

        response = self.client.post(
            reverse("todo_app:siteUser_login"),
            {"username": "", "password": "abc", },
            follow=True,
        )
        self.assertFormError(response, "form", "username", "名前を入力してください")
        self.assertEqual(response.context["form"].data["username"], "")
        self.assertEqual(response.context["form"].data["password"], "abc")
        self.assertTemplateUsed(response, "siteUser/login.html")

        response = self.client.post(
            reverse("todo_app:siteUser_login"),
            {"username": "testuser", "password": "", },
            follow=True,
        )
        self.assertFormError(response, "form", "password", "パスワードを入力してください")
        self.assertEqual(response.context["form"].data["username"], "testuser")
        self.assertEqual(response.context["form"].data["password"], "")
        self.assertTemplateUsed(response, "siteUser/login.html")

        response = self.client.post(
            reverse("todo_app:siteUser_login"),
            {"username": "", "password": "", },
            follow=True,
        )
        self.assertFormError(response, "form", "username", "名前を入力してください")
        self.assertFormError(response, "form", "password", "パスワードを入力してください")
        self.assertEqual(response.context["form"].data["username"], "")
        self.assertEqual(response.context["form"].data["password"], "")
        self.assertTemplateUsed(response, "siteUser/login.html")

        response = self.client.post(
            reverse("todo_app:siteUser_login"),
            {"username": "testuserr", "password": "abc", },
            follow=True,
        )
        self.assertFormError(response, "form", None, "名前かパスワードが間違っています")
        self.assertEqual(response.context["form"].data["username"], "testuserr")
        self.assertEqual(response.context["form"].data["password"], "abc")
        self.assertTemplateUsed(response, "siteUser/login.html")


class SiteUserLogoutViewTest(TestCase):
    def setUp(self):

        self.site_user = SiteUser.objects.create_user(
            username="testuser", password="abc"
        )
        self.client.force_login(self.site_user)

    def test_siteUser_logout(self):

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


class TaskListViewTest(TestCase):
    def setUp(self):

        self.site_user = SiteUser.objects.create_user("testuser")
        self.client.force_login(self.site_user)

    def test_no_tasks(self):

        response = self.client.get(reverse("todo_app:task_list", kwargs={"page": 1}))
        self.assertQuerysetEqual(response.context["tasks"].object_list, [])
        self.assertTemplateUsed(response, "task/list.html")
        self.assertEqual(response.status_code, 200)

    def test_two_tasks(self):

        create_task(1, "task1", "", self.site_user, False)
        create_task(2, "task2", "", self.site_user, False)

        response = self.client.get(reverse("todo_app:task_list", kwargs={"page": 1}))
        self.assertQuerysetEqual(
            response.context["tasks"].object_list, ["<Task: task1>", "<Task: task2>"]
        )
        self.assertTemplateUsed(response, "task/list.html")
        self.assertEqual(response.status_code, 200)

    def test_page_with_no_task(self):

        create_task(1, "task1", "", self.site_user, False)

        response = self.client.get(reverse("todo_app:task_list", kwargs={"page": 2}))
        self.assertQuerysetEqual(
            response.context["tasks"].object_list, ["<Task: task1>"]
        )
        self.assertTemplateUsed(response, "task/list.html")
        self.assertEqual(response.status_code, 200)


class TaskRegisterViewTest(TestCase):
    def setUp(self):

        self.site_user = SiteUser.objects.create_user("testuser")
        self.client.force_login(self.site_user)

    def test_task_register(self):

        response = self.client.get(reverse("todo_app:task_register"))
        self.assertTemplateUsed(response, "task/register.html")
        self.assertEqual(response.status_code, 200)

    def test_task_register_with_correct_input(self):

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
        tasks = Task.objects.all().order_by("id")
        task1 = tasks[0]
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(task1.title, "task1")
        self.assertEqual(task1.content, "abc")
        self.assertEqual(task1.deadline.strftime("%Y-%m-%d %H:%M"), "2020-05-10 03:12")
        self.assertEqual(task1.done_flag, False)

        response = self.client.post(
            reverse("todo_app:task_register"),
            {"title": "task2", "content": "", "deadline": "", },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("todo_app:task_list", kwargs={"page": 1}),
            status_code=302,
            target_status_code=200,
        )
        self.assertQuerysetEqual(
            response.context["tasks"].object_list, ["<Task: task1>", "<Task: task2>"]
        )
        tasks = Task.objects.all().order_by("id")
        task2 = tasks[1]
        self.assertEqual(tasks.count(), 2)
        self.assertEqual(task2.title, "task2")
        self.assertEqual(task2.content, "")
        self.assertEqual(task2.deadline, None)
        self.assertEqual(task2.done_flag, False)

    def test_task_register_with_incorrect_input(self):

        response = self.client.post(
            reverse("todo_app:task_register"),
            {"title": "", "content": "abc", "deadline": "2020-05-10T12:12", },
            follow=True,
        )
        self.assertFormError(response, "form", "title", "タスク名を入力してください")
        self.assertEqual(response.context["form"].data["content"], "abc")
        self.assertEqual(response.context["form"].data["deadline"], "2020-05-10T12:12")
        self.assertTemplateUsed(response, "task/register.html")
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 0)


class TaskShowViewTest(TestCase):
    def setUp(self):

        self.site_user = SiteUser.objects.create_user("testuser")
        self.client.force_login(self.site_user)
        response = self.client.get(reverse("todo_app:task_list", kwargs={"page": 1}))
        create_task(1, "task1", "", self.site_user, False)

    def test_exist_task_show(self):

        response = self.client.get(reverse("todo_app:task_show", kwargs={"task_id": 1}))
        self.assertTemplateUsed(response, "task/show.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["task"].title, "task1")

    def test_not_exist_task_show(self):

        response = self.client.get(reverse("todo_app:task_show", kwargs={"task_id": 2}))
        self.assertEqual(response.status_code, 404)


class TaskUpdateViewTest(TestCase):
    def setUp(self):

        self.site_user = SiteUser.objects.create_user("testuser")
        self.client.force_login(self.site_user)
        response = self.client.get(reverse("todo_app:task_list", kwargs={"page": 1}))
        create_task(1, "task1", "abc", self.site_user, False)

    def test_task_update_get_with_exist_task(self):

        response = self.client.get(
            reverse("todo_app:task_update", kwargs={"task_id": 1})
        )
        self.assertEqual(response.context["deadline_format_necessity"], 1)
        self.assertTemplateUsed(response, "task/edit.html")
        self.assertEqual(response.status_code, 200)

    def test_task_update_get_with_not_exist_task(self):

        response = self.client.get(
            reverse("todo_app:task_update", kwargs={"task_id": 2})
        )
        self.assertEqual(response.status_code, 404)

    def test_task_update_post_with_not_exist_task(self):

        response = self.client.post(
            reverse("todo_app:task_update", kwargs={"task_id": 2}),
            {"title": "task2", "content": "def", "deadline": "2020-05-10T12:12", },
            follow=True,
        )
        self.assertEqual(response.status_code, 404)

    def test_task_update_post_with_correct_input(self):

        response = self.client.post(
            reverse("todo_app:task_update", kwargs={"task_id": 1}),
            {"title": "task2", "content": "def", "deadline": "2020-05-10T12:12", },
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
        tasks = Task.objects.all().order_by("id")
        task1 = tasks[0]
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(task1.title, "task2")
        self.assertEqual(task1.content, "def")
        self.assertEqual(task1.deadline.strftime("%Y-%m-%d %H:%M"), "2020-05-10 03:12")
        self.assertEqual(task1.done_flag, False)

        response = self.client.post(
            reverse("todo_app:task_update", kwargs={"task_id": 1}),
            {"title": "task2", "content": "", "deadline": "", },
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
        tasks = Task.objects.all().order_by("id")
        task1 = tasks[0]
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(task1.title, "task2")
        self.assertEqual(task1.content, "")
        self.assertEqual(task1.deadline, None)
        self.assertEqual(task1.done_flag, False)

    def test__task_update_post_with_incorrect_input(self):

        response = self.client.post(
            reverse("todo_app:task_update", kwargs={"task_id": 1}),
            {"title": "", "content": "abc", "deadline": "2020-05-10T12:12", },
            follow=True,
        )
        self.assertFormError(response, "form", "title", "タスク名を入力してください")
        self.assertEqual(response.context["form"].data["content"], "abc")
        self.assertEqual(response.context["form"].data["deadline"], "2020-05-10T12:12")
        self.assertEqual(response.context["deadline_format_necessity"], 0)
        self.assertTemplateUsed(response, "task/edit.html")
        tasks = Task.objects.all().order_by("id")
        task1 = tasks[0]
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(task1.title, "task1")
        self.assertEqual(task1.content, "abc")
        self.assertEqual(task1.done_flag, False)


class TaskDoneViewTest(TestCase):
    def setUp(self):

        self.site_user = SiteUser.objects.create_user("testuser")
        self.client.force_login(self.site_user)
        response = self.client.get(reverse("todo_app:task_list", kwargs={"page": 1}))
        create_task(1, "task1", None, self.site_user, False)
        create_task(2, "task2", None, self.site_user, False)

    def test_exist_task_done1(self):

        response = self.client.get(reverse("todo_app:task_done", kwargs={"task_id": 1}))
        self.assertRedirects(
            response,
            reverse(
                "todo_app:task_list", kwargs={"page": self.client.session.get("page")}
            ),
            status_code=302,
            target_status_code=200,
        )
        task1 = Task.objects.get(pk=1)
        self.assertEqual(task1.done_flag, True)

    def test_exist_task_done2(self):

        response = self.client.get(reverse("todo_app:task_done", kwargs={"task_id": 2}))
        response = self.client.get(reverse("todo_app:task_done", kwargs={"task_id": 2}))
        self.assertRedirects(
            response,
            reverse(
                "todo_app:task_list", kwargs={"page": self.client.session.get("page")}
            ),
            status_code=302,
            target_status_code=200,
        )
        task2 = Task.objects.get(pk=2)
        self.assertEqual(task2.done_flag, False)

    def test_non_exist_task_done(self):

        response = self.client.get(reverse("todo_app:task_done", kwargs={"task_id": 3}))
        self.assertEqual(response.status_code, 404)


class TaskDeleteViewTest(TestCase):
    def setUp(self):

        self.site_user = SiteUser.objects.create_user("testuser")
        self.client.force_login(self.site_user)
        response = self.client.get(reverse("todo_app:task_list", kwargs={"page": 1}))
        create_task(1, "task1", None, self.site_user, False)

    def test_task_delete_post_with_exist_task(self):

        response = self.client.post(
            reverse("todo_app:task_delete", kwargs={"task_id": 1}), follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                "todo_app:task_list", kwargs={"page": self.client.session.get("page")}
            ),
            status_code=302,
            target_status_code=200,
        )
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 0)

    def test_task_delete_post_with_not_exist_task(self):

        response = self.client.post(
            reverse("todo_app:task_delete", kwargs={"task_id": 2}), follow=True
        )
        self.assertEqual(response.status_code, 404)
