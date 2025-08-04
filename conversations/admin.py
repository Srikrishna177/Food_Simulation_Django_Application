from django.contrib import admin
from .models import Conversation


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'foods', 'vegetarian', 'vegan', 'created_at')
    list_filter = ('vegetarian', 'vegan')
    ordering = ('-created_at',)