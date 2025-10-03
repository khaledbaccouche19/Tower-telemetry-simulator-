#!/usr/bin/env python3
import argparse
import json
import xml.etree.ElementTree as ET

# Define which sensors are considered "working" by status strings mapping
WORKING_STATUS = {
    'Contact Closure': {'Active', 'Inactive'},
    'Temperature': {'Normal'},
    'Analog': {'Normal'},
    'Output': {'Active', 'Inactive'},
}

IGNORED_NAMES = {'unnamed'}


def parse_xml_to_filtered_json(xml_path: str) -> dict:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def text(tag):
        el = root.find(tag)
        return el.text if el is not None else None

    unit = {
        'siteName': text('Unit_Sitename'),
        'serial': text('Unit_Serial'),
        'version': text('Unit_Version'),
        'build': text('Unit_Build'),
        'hardware': text('Unit_Hardware'),
        'timestamp': {
            'date': text('Unit_Date'),
            'time': text('Unit_Time'),
        },
        'location': {
            'latitude': text('Unit_Latitude'),
            'longitude': text('Unit_Longitude'),
        },
    }

    # Collect sensors grouped by EventSensor (ES)
    sensors = []
    for es in root.findall('EventSensor'):
        es_name_el = es.find('ES_Name')
        es_name = es_name_el.text if es_name_el is not None else None
        for s in es.findall('Sensor'):
            s_type = (s.findtext('Sensor_Type') or '').strip()
            s_name = (s.findtext('Sensor_Name') or '').strip()
            status_str = (s.findtext('Sensor_Status_String') or '').strip()
            enabled = (s.findtext('Sensor_Enabled') or '').strip()
            value_str = (s.findtext('Sensor_Value_String') or '').strip()

            # Skip unnamed or disabled sensors
            if s_name.lower() in IGNORED_NAMES:
                continue
            if enabled.upper() == 'OFF':
                continue

            # Keep only if status is in working set for that type (fallback: accept if non-empty)
            allowed = WORKING_STATUS.get(s_type, None)
            if allowed is not None and status_str not in allowed:
                continue

            sensors.append({
                'group': es_name,
                'type': s_type,
                'name': s_name,
                'status': status_str,
                'value': value_str,
            })

    return {
        'unit': unit,
        'sensors': sensors,
        'counts': {
            'totalSensors': len(sensors)
        }
    }


def main():
    ap = argparse.ArgumentParser(description='Convert SiteStatus.xml to filtered JSON')
    ap.add_argument('--in', dest='input_xml', default='SiteStatus.xml')
    ap.add_argument('--out', dest='output_json', default='siteboss_filtered.json')
    args = ap.parse_args()

    data = parse_xml_to_filtered_json(args.input_xml)
    with open(args.output_json, 'w') as f:
        json.dump(data, f, indent=2)
    print('Saved', args.output_json)

if __name__ == '__main__':
    main()
