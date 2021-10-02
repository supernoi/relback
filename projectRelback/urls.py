from django.urls import include, path

urlpatterns = [
    path('', include('coreRelback.urls', namespace='coreRelback')),
]