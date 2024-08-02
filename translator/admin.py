# from django.contrib import admin
# from .models import Chat
# # Register your models here.
# admin.site.register(Chat)

# admin.py

from django.contrib import admin
from django.http import HttpResponse
from .models import Chat
import os

def download_translations(modeladmin, request, queryset):
    file_paths = []
    for chat in queryset:
        if chat.is_correct:
            file_paths.append(chat.correct_file_path)
        else:
            file_paths.append(chat.incorrect_file_path)

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=translations.txt'

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            response.write(file.read())

    return response

download_translations.short_description = 'Download selected translations'

class ChatAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'response', 'created_at', 'is_correct']
    actions = [download_translations]

admin.site.register(Chat, ChatAdmin)



