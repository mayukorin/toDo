from django import forms
from todo_app.models.task import Task


class TaskRegisterForm(forms.ModelForm):
    class Meta:
        model = Task

        fields = ("title", "content", "deadline")

        labels = {
            "title": "タスク名",
            "content": "内容",
            "deadline": "締め切り",
        }

        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "content": forms.Textarea(),
        }

        input_formats = {"deadline": ["%Y-%m-%dT%H:%M"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_title(self):

        title = self.cleaned_data["title"]

        if title is None:

            raise forms.ValidationError("タスク名を入力してください")

        return title
