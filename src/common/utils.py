import fnc
import csv
from datetime import datetime


def get_summary_payload(raw):
    org = fnc.get('matches[0].org', raw)
    hostnames = fnc.get('matches[0].hostnames', raw) or []
    city = fnc.get('matches[0].location.city', raw)
    country_name = fnc.get('matches[0].location.country_name', raw)
    matches = fnc.get('matches', raw)
    ports = [str(fnc.get('port', match)) for match in matches]
    data = []
    for match in matches:
        vulns = fnc.get('vulns', match) or []
        for vuln in vulns:
            data.append(
                {'CVE-ID': vuln, **vulns[vuln]})
    return {
        'Organization': org,
        'Hostname': hostnames,
        'City': city,
        'Country': country_name,
        'Open ports': list(set(ports)),
        'Vulnerabilities': list({x['CVE-ID']: x for x in data}.values())
    }


def get_result_payload(raw):
    matches = fnc.get('matches', raw)
    data = []
    for match in matches:
        ip = fnc.get('ip_str', match)
        port = fnc.get('port', match)
        os = fnc.get('os', match)
        country = fnc.get('location.country_name', match)
        city = fnc.get('location.city', match)
        data.append((ip, port, os, country, city))
    return data


def get_export_payload(raw):
    matches = fnc.get('matches', raw)
    data = []
    for match in matches:
        ip = fnc.get('ip_str', match)
        port = fnc.get('port', match)
        os = fnc.get('os', match)
        country = fnc.get('location.country_name', match)
        city = fnc.get('location.city', match)
        data.append({"ip": ip, "port": port, "os": os,
                    "country": country, "city": city})
    return data


def dict_to_csv(data):
    dict = fnc.get('[0]', data)
    header = dict.keys()
    timestamp = int(datetime.now().timestamp())
    with open(f'data/result_{timestamp}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
