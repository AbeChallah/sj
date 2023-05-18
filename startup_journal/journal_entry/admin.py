from django.contrib import admin
# from django.contrib.admin import AdminSite
from .models import Entry

# class SJAdminSite(AdminSite):
#    title_header = 'StartupJournal Admin'
#    index_title = 'StartupJournal site admin'

# admin_site = SJAdminSite(name='StartupJournal')

# Register your models here.

# admin_site.register(Entry)
@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['text', 'date_added', 'owner', 'get_tags']
    list_filter = ['date_added', 'tags']
    # search_fields = ['text', 'tags'] # not working for some reason
    ordering = ['date_added']

    # This is how you can include tags in the admin list display
    def get_tags(self, entry):
        tags = []
        for tag in entry.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)
