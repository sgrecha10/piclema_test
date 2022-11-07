from django.contrib import admin
from .models import Device, Tag, TagValue


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created', 'updated')
    readonly_fields = ('created', 'updated')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'device', 'ratio', 'min_value', 'max_value',
        'created', 'updated',
    )
    readonly_fields = ('created', 'updated')


@admin.register(TagValue)
class TagValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'value', 'created')
    readonly_fields = ('created',)
