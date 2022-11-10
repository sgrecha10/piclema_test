import json
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer

from telemetry.utils import processing


class Command(BaseCommand):
    help = (
        'Kafka consumer'
    )

    def handle(self, *args, **options):
        sys.stdout.write('Consumer started..')
        
        kafka_params = settings.KAFKA
        bootstrap_server = '{}:{}'.format(kafka_params['HOST'], kafka_params['PORT'])
        consumer = KafkaConsumer(
            kafka_params['TOPIC'],
            bootstrap_servers=[bootstrap_server],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        )

        for message in consumer:
            # sys.stdout.write(str(message.value) + '\n')
            processing(message.value)
