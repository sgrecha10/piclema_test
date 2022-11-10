import json
import random
import sys
import time

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from kafka import KafkaProducer

from telemetry.models import Device

VERSION = 'some_version'
MIN_VALUE = -120
MAX_VALUE = 120

# False для работы через request
IS_BROKER = True


class Command(BaseCommand):
    help = (
        'Data generator'
    )

    def handle(self, *args, **options):
        sys.stdout.write('Generator working..')

        devices = Device.objects.prefetch_related('tag_set').all()
        device_idx = [device.id for device in devices]

        kafka_params = settings.KAFKA
        bootstrap_server = '{}:{}'.format(kafka_params['HOST'], kafka_params['PORT'])
        producer = KafkaProducer(
            bootstrap_servers=[bootstrap_server],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        )

        def _data_generator() -> dict:
            device_id = random.choice(device_idx)
            tag_name_list = [tag.name for tag in devices.get(id=device_id).tag_set.all()]
            timestamp = time.time()

            data = {
                'timestamp': timestamp,
                'device_id': device_id,
                'version': VERSION,
            }
            for tag_name in tag_name_list:
                data.update({tag_name: random.randint(MIN_VALUE, MAX_VALUE)})

            # иногда добавляем некорректное устройство
            if int(timestamp) % 7 == 0:
                data['device_id'] = 0

            # иногда добавляем некорректный тег
            if int(timestamp) % 3 == 0:
                data.update({'tag_incorrect': 4})

            return data

        while True:
            if IS_BROKER:
                data = _data_generator()
                producer.send(kafka_params['TOPIC'], data)
            else:
                with requests.Session() as session:
                    data = _data_generator()
                    session.request(
                        method='POST',
                        url=settings.BASE_URL + reverse('tag_value'),
                        json=data,
                    )
            sys.stdout.write(str(data) + '\n')
