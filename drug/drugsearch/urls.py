from django.urls import path
from . import views

app_name = 'drugsearch' 

urlpatterns = [ 
    path('',views.home,name='home'),
    path('index_t', views.search_index, name='search_view'), 
]
