from django.http import JsonResponse
from .models import SubService

def get_sub_services(request):
    service_id = request.GET.get('service')
    sub_services = SubService.objects.filter(service_id=service_id).values('id', 'name')
    return JsonResponse({'sub_services': list(sub_services)})
