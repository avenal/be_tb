from django.core.management.base import BaseCommand, CommandError
from measures.models import Measure, Device, DeviceMeasure, Aggregation, Log, AggregationLog, DeviceRemoteAddr
import requests
import json
from datetime import datetime, timedelta
from pytz import timezone
import dateutil.parser

class Command(BaseCommand):
    help = "Get messages"

    def handle(self, *args, **options):
        payload = {
            "clientId": "",
            "userName": "",
            "password": "",
            "cleanSession": False,
        }
        r = requests.post("https://node02.myqtthub.com/login", data=json.dumps(payload))
        token = r.json()["tokenId"]
        payload = {
            "tokenId": token,
            "domainName": "",
            "stashName": "PublishedMessages",
            "downloadAs": "json",
            "downloadFrame": "1h",
        }
        cookies = {"tokenId":token}
        r = requests.post(
            "https://node02.myqtthub.com/stashed/download", data=json.dumps(payload), cookies=cookies
        )
        agg = Aggregation.objects.latest('created_at')
        log_processed = []
        for entry in r.json():
            date = dateutil.parser.parse(entry["date"])
            if date > (agg.created_at.replace(tzinfo=date.tzinfo) + timedelta(hours=2)):
                data = entry["payload"].split(",")
                device, created = Device.objects.get_or_create(client_id=entry["clientId"])
                if created:
                    device.mac_address = data[0]
                    device.latitude = data[1]
                    device.longitude = data[2]
                    device.save()

                deviceRemoteAddr = DeviceRemoteAddr(created_at=date, latest_ip=entry["remoteAddr"], device=device)
                deviceRemoteAddr.save()
                measure_created_date = datetime(int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7]),int(data[8]))
                measure = Measure(created_at=date, value=int(data[9]))
                measure.save()
                device_measure = DeviceMeasure(device=device, measure=measure)
                device_measure.save()
                log_processed.append(entry)
        log = Log(payload=r.text, processed=str(log_processed))
        log.save()
        aggregation = Aggregation(status="OK")
        aggregation.save()
        aggregation_log = AggregationLog(aggregation=aggregation, log=log)
        