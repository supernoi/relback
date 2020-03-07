from django.contrib import admin
from django.urls import path

from coreRelback import views

app_name = 'coreRelback'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('creators/', views.creators, name='creators'),
    # Routes - Clients
    path('client/', views.clientRead, name='client'),
    path('client/create/', views.clientCreate, name='clientCreate'),
    path('client/update/<int:idClient>', views.clientUpdate, name='clientUpdate'),
    path('client/delete/<int:idClient>', views.clientDelete, name='clientDelete'),

    # Routes - Hosts
    path('host/', views.hostRead.as_view(), name='host'),
    path('host/create/', views.hostCreate.as_view(), name='hostCreate'),
    path('host/update/', views.hostUpdate.as_view(), name='hostUpdate'),
    path('host/delete/', views.hostDelete.as_view(), name='hostDelete'),

    # Routes - Databases
    path('database/', views.databaseRead, name='database'),
    path('database/create/', views.databaseCreate, name='databaseCreate'),
    # path('database/update/<int:idDatabase>/', views.databaseUpdate, name='databaseUpdate'),
    path('database/delete/<int:idDatabase>/', views.databaseDelete, name='databaseDelete'),

    # Routes - Policies
    path('policies/', views.policiesRead, name='policies'),
    path('policies/create/', views.policiesCreate, name='policiesCreate'),
    path('policies/update/<int:idPolicy>/', views.policiesUpdate, name='policiesUpdate'),
    path('policies/delete/<int:idPolicy>/', views.policiesDelete, name='policiesDelete'),

    # Routes - Reports
    path('reports/', views.reportRead, name='reportRead'),
    path('reports/readLogDetail/<int:idPolicy>/<int:dbKey>/<int:sessionKey>/', views.reportReadLogDetail, name='reportReadLogDetail'),
]
