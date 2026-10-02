from django.contrib.auth import (
    get_user_model,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .forms import AccountEditForm, LoginForm, RegistrationForm
from .models.languages import Languages
from .models.users_learning_languages import UsersLearningLanguages

SESSION_DURATION_SECONDS = 28 * 24 * 60 * 60


@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect("exercises:home")

    initial = {}

    if request.method == "GET":
        form = LoginForm(initial=initial)

    else:
        form = LoginForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data["identifier"].strip()
            password = form.cleaned_data["password"]
            user_model = get_user_model()
            user = (user_model.objects
                .filter(Q(email__iexact=identifier) | Q(nickname__iexact=identifier))
                .first())

            if user is not None and user.is_active and user.check_password(password):
                auth_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                request.session.set_expiry(SESSION_DURATION_SECONDS)
                next_url = request.POST.get("next") or request.GET.get("next")

                if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=request.get_host(), require_https=request.is_secure()):
                    return redirect(next_url)

                return redirect("exercises:home")

            form.add_error(None, "Invalid e-mail address, nickname or password.")

    return render(
        request,
        "accounts/login.html",
        {"form": form, "next": request.GET.get("next", "")}
    )


@ensure_csrf_cookie
def register_view(request):
    if request.user.is_authenticated:
        return redirect("exercises:home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
    else:
        form = RegistrationForm()

    if request.method == "POST" and form.is_valid():
        user = create_user_from_registration(form)
        auth_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        request.session.set_expiry(SESSION_DURATION_SECONDS)
        request.session['force_preferred_interface_language_once'] = True

        return redirect("exercises:home")

    return render(
        request,
        "accounts/registration.html",
        {
            "form": form,
            "interface_languages": Languages.objects.order_by("id"),
            "learning_languages": Languages.objects.order_by("id"),
            "selected_learning_languages": (
                request.POST.getlist("learning_languages")
                if request.method == "POST"
                else []
            ),
        },
    )


@transaction.atomic
def create_user_from_registration(form):
    user_model = get_user_model()
    user = user_model(
        first_name=form.cleaned_data["first_name"],
        last_name=form.cleaned_data["last_name"],
        email=form.cleaned_data["email"],
        telephone=form.cleaned_data.get("telephone"),
        nickname=form.cleaned_data["nickname"],
        preferred_interface_language_id=form.cleaned_data["preferred_interface_language_id"]
    )
    user.set_password(form.cleaned_data["password1"])
    user.save()
    learning_languages = form.cleaned_data["learning_languages"]
    UsersLearningLanguages.objects.bulk_create([
        UsersLearningLanguages(user=user, language=language)
        for language in learning_languages
    ])

    return user


@login_required
@require_POST
def set_initial_learning_language(request):
    language_id = request.POST.get('learning_language_id')

    try:
        language_id = int(language_id)
    except (TypeError, ValueError):
        return HttpResponseBadRequest('Invalid language.')

    learning_language = (Languages.objects
        .filter(id=language_id)
        .first())

    if learning_language is None:
        return HttpResponseBadRequest('Invalid language.')

    is_registered_learning_language = (UsersLearningLanguages.objects
        .filter(user=request.user, language_id=language_id)
        .exists())

    if not is_registered_learning_language:
        return HttpResponseBadRequest('Invalid language.')
    request.user.default_learning_language_id = learning_language.id
    request.user.save(update_fields=['default_learning_language_id'])
    request.session['force_learning_language_code_once'] = learning_language.code

    return redirect('exercises:home')

@login_required
@transaction.atomic
def edit_account_view(request):
    user = request.user
    current_learning_language_ids = list(UsersLearningLanguages.objects
        .filter(user=user)
        .values_list("language_id", flat=True))

    if request.method == "POST":
        form = AccountEditForm(request.POST, user=user)
        selected_learning_languages = (request.POST.getlist("learning_languages"))

    else:
        form = AccountEditForm(
            user=user,
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "telephone": (user.telephone or ""),
                "nickname": user.nickname,
                "preferred_interface_language_id": user.preferred_interface_language_id,
                "learning_languages": current_learning_language_ids
            }
        )

        selected_learning_languages = [
            str(language_id)
            for language_id in current_learning_language_ids
        ]

    if request.method == "POST" and form.is_valid():
        previous_interface_language_id = user.preferred_interface_language_id
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.email = form.cleaned_data["email"]
        user.telephone = form.cleaned_data["telephone"] or None
        user.nickname = form.cleaned_data["nickname"]
        user.preferred_interface_language_id = form.cleaned_data["preferred_interface_language_id"]
        learning_languages = list(form.cleaned_data["learning_languages"])
        selected_ids = {
            language.id
            for language in learning_languages
        }

        if user.default_learning_language_id not in selected_ids:
            if len(selected_ids) == 1:
                user.default_learning_language_id = next(iter(selected_ids))
            else:
                user.default_learning_language_id = None

        password_changed = False
        new_password = form.cleaned_data.get("password1")

        if new_password:
            user.set_password(new_password)
            password_changed = True

        update_fields = ["first_name", "last_name", "email", "telephone", "nickname", "preferred_interface_language_id",
            "default_learning_language_id"]

        if password_changed:
            update_fields.append("password")

        user.save(update_fields=update_fields)
        UsersLearningLanguages.objects.filter(user=user).delete()
        UsersLearningLanguages.objects.bulk_create([
                UsersLearningLanguages(user=user, language=language)
                for language in learning_languages
            ])

        if password_changed:
            update_session_auth_hash(request, user)

        if previous_interface_language_id != user.preferred_interface_language_id:
            request.session["force_preferred_interface_language_once"] = True

        request.session["account_changes_saved_once"] = True

        return redirect("accounts:edit_account")

    force_preferred_interface_language = request.session.pop("force_preferred_interface_language_once", False)
    account_changes_saved = request.session.pop("account_changes_saved_once", False)
    account_changes_error = (request.method == "POST" and bool(form.errors))

    return render(
        request,
        "accounts/account_edit.html",
        {
            "form": form,
            "interface_languages": Languages.objects.order_by("id"),
            "learning_languages": Languages.objects.order_by("id"),
            "selected_learning_languages": selected_learning_languages,
            "force_preferred_interface_language": force_preferred_interface_language,
            "account_changes_saved": account_changes_saved,
            "account_changes_error": account_changes_error
        }
    )

@require_POST
def logout_view(request):
    auth_logout(request)

    return redirect("accounts:login")