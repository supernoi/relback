from django.urls import include, path

urlpatterns = [
    path("", include("coreRelback.urls", namespace="coreRelback")),
    path("api/", include("coreRelback.api.urls", namespace="api")),
    path("__reload__/", include("django_browser_reload.urls")),
]