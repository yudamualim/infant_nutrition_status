"""
URL configuration for nutrition_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from napp import views
from napp.views import person_form

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.data_test),
    path('data-test', views.data_test),
    path('data-train', views.data_train),
    path('correlation', views.correlation),
    path('predict', views.predict),
    path('graph', views.graph),
    path('person-form', person_form, name='person_form'),
    path('success/', views.success_view, name='success'),
    path('index/person/', views.index_person, name='index_person'),  # Add a name to this path
    path('edit-person/<int:person_id>/', views.edit_person, name='edit_person'),
    path('delete-person/<int:person_id>/', views.delete_person, name='delete_person'),
]

