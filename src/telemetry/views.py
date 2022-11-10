import json

from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .utils import processing


@method_decorator(csrf_exempt, name='dispatch')
class TagValueView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            data = None

        processing(data)
        return HttpResponse()
