from django.contrib import admin

from .models import Device, Tag, TagValue


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created', 'updated')
    readonly_fields = ('created', 'updated')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'device_name', 'ratio', 'min_value', 'max_value',
        'created', 'updated',
    )
    readonly_fields = ('created', 'updated')

    @admin.display(description=Tag.device.field.verbose_name)
    def device_name(self, obj):
        return obj.device.name

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.select_related('device')


@admin.register(TagValue)
class TagValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'value', 'version', 'timestamp')
    readonly_fields = list_display
