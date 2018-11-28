"""
Description: URLs are defined in this module
"""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.notes_view, name='note'),
    path('<int:year>/<int:month>/<int:day>', views.notes_view, name='note'),
    path('settings', views.settings, name='settings'),
    path('search/', views.search_view, name='search'),
]

