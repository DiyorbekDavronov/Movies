from django.contrib import admin

from .models import Film, Categories


# pk/ film-id => PRIMARY KEY,
@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "image", "time_create", "time_update", "is_published"]
    list_display_links = ["pk", "title"]
    list_editable = ["is_published", "image"]
    list_filter = ["time_create", "time_update", "is_published"]
    search_fields = ["title", "description"]


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "slug"]
    list_display_links = ["pk", "name"]
