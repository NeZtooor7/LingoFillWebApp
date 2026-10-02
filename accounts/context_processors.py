from .models.languages import Languages


def user_language_preferences(request):
    available_languages = list(Languages.objects.order_by("id"))
    preferred_language = None

    if request.user.is_authenticated:
        preferred_language = next((language
                for language in available_languages
                    if language.id == request.user.preferred_interface_language_id),
            None)

    if preferred_language is None:
        preferred_language = next((language
                for language in available_languages
                    if language.code == "en"),
            None)

    return {
        "available_interface_languages": available_languages,
        "preferred_interface_language": preferred_language,
        "preferred_interface_language_code": (preferred_language.code if preferred_language else "en")
    }