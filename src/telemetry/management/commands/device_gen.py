import random
import time

from django.core.management.base import BaseCommand

from telemetry.models import Device, Tag

VERSION = 'some_version'
MIN_VALUE = -120
MAX_VALUE = 120


class Command(BaseCommand):
    help = (
        'Генератор данных, эмуляция работы устройства.'
    )

    def handle(self, *args, **options):
        device_idx = list(Device.objects.values_list('id', flat=True))

        while True:
            device_id = random.choice(device_idx + [0])  # + несуществующее устройство
            tag_name_list = Tag.objects.filter(device_id=device_id).values_list('name', flat=True)
            timestamp = time.time()
            data = {
                'timestamp': timestamp,
                'device_id': device_id,
                'version': VERSION,
            }
            for tag_name in tag_name_list:
                data.update({tag_name: random.randint(MIN_VALUE, MAX_VALUE)})

            # иногда добавляем некорректный тег
            if int(timestamp) % 3 == 0:
                data.update({'tag_incorrect': '4'})

            print(data)
