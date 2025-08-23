from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'venue', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('title', 'venue', 'description')
    ordering = ('-date',)
    date_hierarchy = 'date' 