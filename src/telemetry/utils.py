import logging
from datetime import datetime

import pytz

from .models import Device, Tag, TagValue


def processing(data: dict) -> None:
    try:
        device_id = data.pop('device_id')
        device = Device.objects.prefetch_related('tag_set').get(id=device_id)
    except (Device.DoesNotExist, KeyError, AttributeError):
        logging.error('Device not exists')
        return

    if not (timestamp := data.pop('timestamp', None)):
        logging.error('Timestamp not exists')
        return

    version = data.pop('version', None)

    bulk_data = []
    for name_tag, source_value in data.items():
        try:
            tag = device.tag_set.get(name=name_tag)
        except Tag.DoesNotExist:
            logging.warning(f'Incorrect tag - {name_tag}')
            return

        value = int(source_value * tag.ratio)
        if not (tag.min_value <= value <= tag.max_value):
            logging.warning(f'Not a reference tag`s value - {value}')
            return

        bulk_data.append(
            TagValue(
                tag_id=tag.id,
                value=value,
                version=version,
                timestamp=datetime.fromtimestamp(timestamp, tz=pytz.UTC),
            )
        )

    TagValue.objects.bulk_create(bulk_data)
