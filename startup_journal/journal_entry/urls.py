from django.urls import path
from . import views

app_name = 'journal_entry'
urlpatterns = [
    # Landing page
    path('', views.index, name='index'),
    # Other pages
    path('entries/', views.entries, name='entries'),
    path('date/<str:entry_date>/', views.entries_by_date, name='entries_by_date'),
    path('tag/<slug:tag_slug>/', views.entries, name='entries_by_tag'),
    path('entry/<int:entry_id>/', views.entry, name='entry'),

    # Page for adding a new entry
    path('new_entry/', views.new_entry, name='new_entry'),
    # Page for editing an existing entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('search/', views.entry_search, name='entry_search')
]
