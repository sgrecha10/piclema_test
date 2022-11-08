import json
from datetime import datetime

from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .models import Device, Tag, TagValue


@method_decorator(csrf_exempt, name='dispatch')
class TagValueView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        try:
            device_id = data.pop('device_id')
            device = Device.objects.prefetch_related('tag_set').get(id=device_id)
        except (Device.DoesNotExist, KeyError):
            # logging error
            return

        if not (timestamp := data.pop('timestamp', None)):
            # logging error
            return

        version = data.pop('version', None)

        prepared_data = {}
        for name_tag, source_value in data.items():
            try:
                tag = device.tag_set.get(name=name_tag)
            except Tag.DoesNotExist:
                # logging warning
                return

            value = int(source_value * tag.ratio)
            if not (tag.min_value <= value <= tag.max_value):
                # logging warning
                return

            prepared_data.update({
                'tag_id': tag.id,
                'value': value,
                'version': version,
                'timestamp': datetime.fromtimestamp(timestamp),
            })
            TagValue.objects.create(**prepared_data)

        return HttpResponse()
