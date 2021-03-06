# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 10:50:43 2020

@author: Mayuko

"""


from django.urls import path
from . import views

app_name = "todo_app"

urlpatterns = [
    path(
        "siteUser/register",
        views.siteUser_view.siteUser_register_view,
        name="siteUser_register",
    ),
    path(
        "siteUser/update",
        views.siteUser_view.siteUser_update_view,
        name="siteUser_update",
    ),
    path(
        "siteUser/login", views.siteUser_view.siteUser_login_view, name="siteUser_login"
    ),
    path(
        "siteUser/logout/<int:from_flag>/",
        views.siteUser_view.siteUser_logout_view,
        name="siteUser_logout",
    ),
    path("task/list/<int:page>/", views.task_view.task_list_view, name="task_list"),
    path("task/register", views.task_view.task_register_view, name="task_register"),
    path("task/show/<int:task_id>/", views.task_view.task_show_view, name="task_show",),
    path(
        "task/update/<int:task_id>/",
        views.task_view.task_update_view,
        name="task_update",
    ),
    path(
        "task/delete/<int:task_id>/",
        views.task_view.task_delete_view,
        name="task_delete",
    ),
    path("task/done/<int:task_id>/", views.task_view.task_done_view, name="task_done",),
]
