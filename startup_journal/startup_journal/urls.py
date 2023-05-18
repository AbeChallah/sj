from django.contrib import admin
# from journal_entry.admin import admin_site
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/', admin_site.urls),
    path('users/', include('users.urls')),
    path('', include('journal_entry.urls', namespace='journal_entry')),
]
