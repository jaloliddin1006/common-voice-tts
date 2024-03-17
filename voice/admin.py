from django.contrib import admin
from .models import Sentence, Voice, Comment, CheckVoice, SavedVoiceGroupId
# Register your models here.
from django.utils.html import format_html

@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body', 'is_read', 'created_at', 'updated_at')
    list_display_links = ('id', 'user', 'body')
    list_filter = ('is_read', 'created_at', 'updated_at')
    search_fields = ('body', 'user__username')
    list_editable = ('is_read',)
    
    
@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sentence', 'audio_tag', 'created_at')
    list_display_links = ('id', 'user', 'sentence')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('sentence__body', 'user__username')
        # list_display = ['audio_tag']

    def audio_tag(self, obj):
        return format_html('<audio controls src="{}"></audio>', obj.audio.url)

    audio_tag.short_description = 'Audio'

    
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