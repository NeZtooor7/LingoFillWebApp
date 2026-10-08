from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models.languages import Languages


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=254)
    telephone = forms.CharField(max_length=30, required=False)
    nickname = forms.CharField(max_length=150)
    preferred_interface_language_id = forms.IntegerField(required=True)
    learning_languages = forms.ModelMultipleChoiceField(queryset=Languages.objects.none(), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        languages = Languages.objects.order_by("name")
        self.fields["learning_languages"].queryset = languages
        self.fields["preferred_interface_language_id"].choices = [
            (language.id, language.original_name)
            for language in languages
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        user_model = get_user_model()

        if user_model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this e-mail address already exists.")

        return email

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"].strip().lower()
        user_model = get_user_model()

        if user_model.objects.filter(nickname__iexact=nickname).exists():
            raise forms.ValidationError("This nickname is already in use.")

        return nickname

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", "The passwords do not match.")

                return cleaned_data

            try:
                validate_password(password1)
            except ValidationError as error:
                self.add_error("password1", error)

        return cleaned_data


class AccountEditForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=254)
    telephone = forms.CharField(max_length=30, required=False)
    nickname = forms.CharField(max_length=150)
    preferred_interface_language_id = forms.IntegerField()
    learning_languages = forms.ModelMultipleChoiceField(queryset=Languages.objects.none(), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["learning_languages"].queryset = (Languages.objects.order_by("name"))

    def clean_preferred_interface_language_id(self):
        language_id = self.cleaned_data["preferred_interface_language_id"]

        if not Languages.objects.filter(id=language_id).exists():
            raise forms.ValidationError("Invalid interface language.")

        return language_id

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        user_model = get_user_model()
        already_exists = (user_model.objects
            .filter(email__iexact=email)
            .exclude(id=self.user.id)
            .exists())

        if already_exists:
            raise forms.ValidationError("An account with this e-mail address already exists.")

        return email

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"].strip().lower()
        user_model = get_user_model()
        already_exists = (user_model.objects
            .filter(nickname__iexact=nickname)
            .exclude(id=self.user.id)
            .exists())

        if already_exists:
            raise forms.ValidationError("This nickname is already in use.")

        return nickname

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not password1 and not password2:
            return cleaned_data

        if password1 != password2:
            self.add_error("password2", "The passwords do not match.")

            return cleaned_data

        try:
            validate_password(password1, self.user)
        except ValidationError as error:
            self.add_error("password1", error)

        return cleaned_data
