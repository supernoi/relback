from django.contrib import admin
from django.urls import path

from coreRelback import views

app_name = 'coreRelback'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('creators/', views.creators, name='creators'),

    # Routes - Clients
    path('client/', views.clientRead.as_view(), name='client'),
    path('client/create/', views.clientCreate.as_view(), name='clientCreate'),
    path('client/update/', views.clientUpdate.as_view(), name='clientUpdate'),
    path('client/delete/', views.clientDelete.as_view(), name='clientDelete'),

    # Routes - Hosts
    path('host/', views.hostRead.as_view(), name='host'),
    path('host/create/', views.hostCreate.as_view(), name='hostCreate'),
    path('host/update/', views.hostUpdate.as_view(), name='hostUpdate'),
    path('host/delete/', views.hostDelete.as_view(), name='hostDelete'),

    # Routes - Databases
    path('database/', views.databaseRead.as_view(), name='database'),
    path('database/create/', views.databaseCreate.as_view(), name='databaseCreate'),
    path('database/update/', views.databaseUpdate.as_view(), name='databaseUpdate'),
    path('database/delete/', views.databaseDelete.as_view(), name='databaseDelete'),

    # Routes - Policies
    path('policies/', views.policiesRead, name='policies'),
    path('policies/create/', views.policiesCreate, name='policiesCreate'),
    path('policies/update/<int:idPolicy>/', views.policiesUpdate, name='policiesUpdate'),
    path('policies/delete/<int:idPolicy>/', views.policiesDelete, name='policiesDelete'),

    # Routes - Reports
    path('reports/', views.reportRead, name='reportRead'),
    path('reports/readLogDetail/<int:idPolicy>/<int:dbKey>/<int:sessionKey>/', views.reportReadLogDetail, name='reportReadLogDetail'),

]
