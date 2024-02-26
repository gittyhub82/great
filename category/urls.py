from django.urls import path


from . import views
# rhe namespace for the category links
app_name = 'category'


urlpatterns = [
    path('', views.index, name='index')
]