from core.server_core import parse_request_django, handle_request

import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
	return HttpResponse("msimexper server, version 0.1.0\n\nSee API docs for available methods.")


@csrf_exempt
def main_handler(request, layer, ptype):
	req = parse_request_django(layer, ptype, request)
	res = handle_request(req)
	print('Response:', res.__dict__)

	http_body = ""
	if res.payload != None:
		http_body = json.dumps(res.payload, ensure_ascii=False)
	http_response = HttpResponse(http_body, status=res.code)
	return http_response