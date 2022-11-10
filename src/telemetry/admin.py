from django.contrib import admin

from .models import Device, Tag, TagValue


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'user', 'last_timestamp', 'last_version',
        'created', 'updated',
    )
    readonly_fields = (
        'last_timestamp', 'last_version', 'created', 'updated',
    )

    def _get_last_tag_value(self, obj) -> TagValue:
        tag_ids = list(obj.tag_set.values_list('id', flat=True))
        return TagValue.objects.filter(
            tag_id__in=tag_ids,
        ).last()

    def last_timestamp(self, obj):
        return self._get_last_tag_value(obj).timestamp.timestamp()

    def last_version(self, obj):
        return self._get_last_tag_value(obj).version


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
