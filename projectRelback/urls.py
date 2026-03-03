from django.urls import include, path

urlpatterns = [
    path('', include('coreRelback.urls', namespace='coreRelback')),
    path("__reload__/", include("django_browser_reload.urls")),
]