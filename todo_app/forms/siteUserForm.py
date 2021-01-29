from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ObjectDoesNotExist
from todo_app.models.siteUser import SiteUser


class SiteUserRegisterForm(forms.ModelForm):
    class Meta:

        model = SiteUser

        fields = ("username", "password")

        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "名前"}),
            "password": forms.PasswordInput(attrs={"placeholder": "パスワード"}),
        }

        labels = {"username": "名前", "password": "パスワード"}

        requireds = {"username": False, "password": False}

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


class SiteUserUpdateForm(forms.Form):

    username = forms.CharField(
        label="ユーザ名",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    password = forms.CharField(
        label="パスワード",
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            render_value=True,
            attrs={"class": "form-control", "placeholder": "パスワードは変更するときのみ入力してください", },
        ),
    )

    def __init__(self, username=None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.username_cache = None

        if username:

            self.fields["username"].widget.attrs["value"] = username
            self.username_cache = username

        if self.errors:

            for field_key in self.fields:

                if field_key in self.errors:

                    self.fields[field_key].widget.attrs[
                        "class"
                    ] = "form-control is-invalid"

    def clean_username(self):

        username = self.cleaned_data["username"]

        if len(username) == 0:

            raise forms.ValidationError("名前を入力してください")

        return username

    def clean(self):

        username = self.cleaned_data.get("username")

        try:
            site_user = get_user_model().objects.get(username=username)

        except ObjectDoesNotExist:
            print("新しい名前に変更成功！")
            return

        if site_user.username != self.username_cache:

            raise forms.ValidationError("その名前のユーザーは既に登録されています")


class SiteUserLoginForm(forms.Form):

    username = UsernameField(label="ユーザ名", max_length=255, required=False,)

    password = forms.CharField(
        label="パスワード",
        strip=False,
        required=False,
        widget=forms.PasswordInput(render_value=True),
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean_username(self):

        username = self.cleaned_data["username"]

        if len(username) == 0:
            raise forms.ValidationError("名前を入力してください")

        return username

    def clean_password(self):

        password = self.cleaned_data["password"]

        if len(password) == 0:
            raise forms.ValidationError("パスワードを入力してください")

        return password

    def clean(self):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        try:
            site_user = get_user_model().objects.get(username=username)

        except ObjectDoesNotExist:
            raise forms.ValidationError("名前かパスワードが間違っています")

        if not site_user.check_password(password):
            raise forms.ValidationError("名前かパスワードが間違っています")

        self.user_cache = site_user

    def get_user_cache(self):

        return self.user_cache
