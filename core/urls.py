from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("LingoFillWebApp/", include("exercises.urls")),
    path("LingoFillWebApp/accounts/", include("accounts.urls"))
]