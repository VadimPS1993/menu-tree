from django.contrib import admin
from .models import Menu, MenuItem


@admin.register(Menu)
class Menu(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(MenuItem)
class MenuItem(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'url', 'named_url')  # Показываем эти поля в списке
    list_filter = ('menu',)  # Добавляем возможность фильтрации по меню
    search_fields = ('title',)  # Поле для поиска по названию пункта меню