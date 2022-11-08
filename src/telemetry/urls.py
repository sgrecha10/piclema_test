from django.urls import path

from . import views

urlpatterns = [
    path('tag_value/', views.TagValueView.as_view(), name='tag_value'),
]
