from django.shortcuts import render
from django.utils import timezone
from .models import reportData
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import redis

r = redis.Redis(host='127.0.0.1', port=6379, password='',db=0, decode_responses=True)

def report_list(request):
    reportDati = reportData.objects.filter().order_by("-report_date")
    context = {"dati": reportDati}
    return render(request, "home.html", context)

def report_staff(request):
    total_produced_energy_in_watt = 0
    total_consumed_energy_in_watt = 0

    reportTotale = reportData.objects.filter().order_by("-report_date")

    for r in reportTotale:
        total_produced_energy_in_watt = total_produced_energy_in_watt + r.produced_energy_in_watt
        total_consumed_energy_in_watt = total_consumed_energy_in_watt + r.consumed_energy_in_watt
    context = {
        "total_produced": total_produced_energy_in_watt,
        "total_consumed": total_consumed_energy_in_watt
    }

    return render(request, "total.html", context)

@csrf_exempt
def newReport(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        report = reportData()
        report.report_date = timezone.now()
        report.consumed_energy_in_watt = received_json_data['consumed_energy_in_watt']
        report.produced_energy_in_watt = received_json_data['produced_energy_in_watt']
        report.writeOnChain()
        report.publish()
        return StreamingHttpResponse('Json Data is correctly transimmitted to web app')
    else:
        return StreamingHttpResponse('Endpoint Page')


@receiver(user_logged_in)
def get_ip_address(sender, user, request, **kwargs):
    different_IP = False
    if user.is_staff:
        user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip_address:
            ip = user_ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        username = request.user.username
        check_user = r.get(username)

        if check_user == None :
            r.set(username,ip)
            different_IP = False
        else:
            ip_user = r.get(username)
            if ip_user == ip:
                different_IP = False
            else:
                #Mostro il messaggio in HTML
                different_IP = True
                #Setto il nuovo IP come IP per l'utente
                r.set(username,ip)
    if different_IP == True:
        print("Administrator user " + username + " logged in with new IP: " + ip + " different to the old IP: " + ip_user)
