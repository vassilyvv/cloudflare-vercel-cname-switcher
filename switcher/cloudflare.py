import os

import CloudFlare

CLOUDFLARE_API_KEY = os.environ["CLOUDFLARE_API_KEY"]
CLOUDFLARE_ZONE = os.environ["CLOUDFLARE_ZONE_ID"]

cf = CloudFlare.CloudFlare(token=CLOUDFLARE_API_KEY)


def add_or_update_record(cname, content):
    dns_records = cf.zones.dns_records.get(CLOUDFLARE_ZONE)
    dns_record_data = {
        'name': cname,
        'type': 'CNAME',
        'content': content,
        'proxied': True
    }
    try:
        dns_record = [dr for dr in dns_records if dr['name'] == f"{cname}.very.supply"][0]
        cf.zones.dns_records.put(CLOUDFLARE_ZONE, dns_record['id'], data=dns_record_data)
    except IndexError as dns_record_not_exist_error:
        cf.zones.dns_records.post(CLOUDFLARE_ZONE, data=dns_record_data)


def delete_record(cname):
    dns_records = cf.zones.dns_records.get(CLOUDFLARE_ZONE)
    try:
        dns_record = [dr for dr in dns_records if dr['name'] == f"{cname}.very.supply"][0]
        cf.zones.dns_records.delete(CLOUDFLARE_ZONE, dns_record['id'])
    except IndexError as dns_record_not_exist_error:
        pass
