from django.contrib import admin
from .models import Sentence, Voice, Comment, CheckVoice, SavedVoiceGroupId
# Register your models here.


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body', 'is_read', 'created_at', 'updated_at')
    list_display_links = ('id', 'user', 'body')
    list_filter = ('is_read', 'created_at', 'updated_at')
    search_fields = ('body', 'user__username')
    list_editable = ('is_read',)
    
    
@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sentence', 'file', 'created_at', 'updated_at')
    list_display_links = ('id', 'user', 'sentence')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('sentence__body', 'user__username')
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sentence', 'body', 'created_at', 'updated_at')
    list_display_links = ('id', 'user', 'sentence')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('body', 'user__username')
    
    
@admin.register(CheckVoice)
class CheckVoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'voice', 'is_checked', 'created_at', 'updated_at')
    list_display_links = ('id', 'user', 'voice')
    list_filter = ('is_checked', 'created_at', 'updated_at')
    search_fields = ('voice__sentence__body', 'user__username')
    list_editable = ('is_checked',)
    
    
@admin.register(SavedVoiceGroupId)
class SavedVoiceGroupIdAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'created_at', 'updated_at')
    list_display_links = ('id', 'user')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('group', 'user__username')