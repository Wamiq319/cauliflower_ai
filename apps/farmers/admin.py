from django.contrib import admin
from .models import Analysis, Case, CaseSuggestion

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'crop_name', 'disease_name', 'analysis_date']
    list_filter = ['crop_name', 'disease_name', 'analysis_date']
    search_fields = ['farmer__username', 'farmer__email', 'crop_name', 'disease_name']
    readonly_fields = ['analysis_date']
    date_hierarchy = 'analysis_date'

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'farmer', 'analysis', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['farmer__username', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

@admin.register(CaseSuggestion)
class CaseSuggestionAdmin(admin.ModelAdmin):
    list_display = ['case', 'doctor', 'title', 'priority', 'created_at']
    list_filter = ['priority', 'created_at']
    search_fields = ['case__title', 'doctor__username', 'title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at' 