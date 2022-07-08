"""
Created on Fri Apr 22 17:11:06 2022

@author: Fernando Sánchez
"""

from search import Scanner
import json

SHODAN_FILTERS = {'HOSTNAME': 'hostname', 'NET': 'net', 'IP': 'ip'}

"""
138.123.62.124
178.77.78.196
"""
# Report files
file_report_result = open("report_result.json", "w")
file_report_ip = open("report_ip.txt", "w")
file_report_summary = open("report_summary.txt", "w")


def get_ip(response):
    matches = response['matches']
    return list(map(lambda n: '{ip_str}:{port}'.format(**n), matches))


def get_report(response):
    data = {}
    ports = []
    vulns = []
    matches = response['matches']

    first_match = matches[0]
    if ('hostnames' in first_match):
        data['hostnames'] = ','.join(first_match['hostnames'])

    if ('location' in first_match and 'city' in first_match['location']):
        data['city'] = first_match['location']['city']

    if ('location' in first_match and 'country_name' in first_match['location']):
        data['country'] = first_match['location']['country_name']

    if ('org' in first_match):
        data['org'] = first_match['org']

    for match in matches:
        if ('port' in match):
            ports.append(str(match['port']))
        vulns = [*vulns, *match['vulns']] if 'vulns' in match else [*vulns]

    data['vulns'] = list(set(vulns))
    data['ports'] = list(set(ports))
    return data


try:
    # Text to search
    text = input('Search: ')
    choosen_filter = None
    while choosen_filter not in SHODAN_FILTERS.values():
        choosen_filter = input(
            f'Choose one of the followings ({",".join(SHODAN_FILTERS.values())}): ')
    filter_value = input(
        f'{SHODAN_FILTERS[choosen_filter.upper()].capitalize()}: ')
    query = f'{text} {choosen_filter}:{filter_value}'
    # Searching using scanner
    scanner = Scanner()
    print('Searching for results 🔍...')
    response = scanner.search(query)
    print('We have found {total} results!'.format(**response))
    # Parse response
    report = get_report(response)
    ip = get_ip(response)
    report_vulns = report['vulns']
    report_ports = report['ports']
    print(f'{len(report_vulns)} vulnerabilities found.')
    print(f'{len(report_ports)} open ports found.')
    print('Exporting data...')
    # Export data
    file_report_result.write(json.dumps(response))
    file_report_ip.write('\n'.join(ip))
    file_report_summary.write('Hostnames: {hostnames}\n'.format(**report))
    file_report_summary.write('City: {city}\n'.format(**report))
    file_report_summary.write('Country: {country}\n'.format(**report))
    file_report_summary.write('Organization: {org}\n'.format(**report))
    file_report_summary.write(
        f'Number of vulnerabilities: {len(report_vulns)}\n')
    file_report_summary.write(f'Number of open ports: {len(report_ports)}\n')
    file_report_summary.write(
        f'Vulnerabilities: {"    ".join(report_vulns)}\n')
    file_report_summary.write(f'Ports: {"    ".join(report_ports)}\n')
    print('See result report for more details 😁.')
except Exception as e:
    print(f'Error: {e}')

file_report_result.close()
file_report_ip.close()
file_report_summary.close()
