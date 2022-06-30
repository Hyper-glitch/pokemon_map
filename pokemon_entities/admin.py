from django.contrib import admin

from .models import Pokemon


@admin.register(Pokemon)
class BookInstanceAdmin(admin.ModelAdmin):
    pass
