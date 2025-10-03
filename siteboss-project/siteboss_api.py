#!/usr/bin/env python3
"""
SiteBoss API - Complete workflow for backend integration
Pulls XML data, converts to JSON, and prepares for API consumption
"""
import asyncio
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

# Define which sensors are considered "working" by status strings mapping
WORKING_STATUS = {
    'Contact Closure': {'Active', 'Inactive'},
    'Temperature': {'Normal'},
    'Analog': {'Normal'},
    'Output': {'Active', 'Inactive'},
}

IGNORED_NAMES = {'unnamed'}


async def pull_xml_data(host: str, username: str, password: str) -> str:
    """Pull XML data from SiteBoss device using Playwright"""
    base = f'http://{host}'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context()
        page = await ctx.new_page()

        print("🔌 Connecting to SiteBoss device...")
        
        # 1) Open login page
        await page.goto(f'{base}/UnitLogin.html', wait_until='domcontentloaded')
        
        # 2) AJAX login
        await page.evaluate(
            """
            async (cred)=>{
            const params = new URLSearchParams({username:cred.u, password:cred.p});
            await fetch('/index.html?commit=login', {
                method:'POST',
                headers:{'Content-Type':'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'},
                body:params
            });
            }
            """,
            {"u": username, "p": password}
        )
        
        # 3) Land on UI to cement session
        await page.goto(f'{base}/UnitMain.html', wait_until='domcontentloaded')
        
        # 4) Navigate directly to XML and read response text
        print("📥 Fetching XML data...")
        resp = await page.goto(f'{base}/SiteStatus.xml')
        xml_text = await resp.text()

        await browser.close()
        
        if xml_text.strip().startswith('<?xml'):
            print("✅ XML data retrieved successfully")
            return xml_text
        else:
            raise Exception("Failed to retrieve XML data - got HTML instead")


def parse_xml_to_json(xml_text: str) -> dict:
    """Convert XML text to filtered JSON format"""
    print("🔄 Converting XML to JSON...")
    
    root = ET.fromstring(xml_text)

    def text(tag):
        el = root.find(tag)
        return el.text if el is not None else None

    # Extract unit information
    unit = {
        'siteName': text('Unit_Sitename'),
        'serial': text('Unit_Serial'),
        'version': text('Unit_Version'),
        'build': text('Unit_Build'),
        'hardware': text('Unit_Hardware'),
        'timestamp': {
            'date': text('Unit_Date'),
            'time': text('Unit_Time'),
            'lastUpdated': datetime.now().isoformat()
        },
        'location': {
            'latitude': float(text('Unit_Latitude')) if text('Unit_Latitude') else None,
            'longitude': float(text('Unit_Longitude')) if text('Unit_Longitude') else None,
        },
        'uptime': text('Unit_Uptime')
    }

    # Collect sensors grouped by EventSensor (ES)
    sensors = []
    for es in root.findall('EventSensor'):
        es_name_el = es.find('ES_Name')
        es_name = es_name_el.text if es_name_el is not None else None
        es_state = es.findtext('ES_State', '').strip()
        
        for s in es.findall('Sensor'):
            s_type = (s.findtext('Sensor_Type') or '').strip()
            s_name = (s.findtext('Sensor_Name') or '').strip()
            status_str = (s.findtext('Sensor_Status_String') or '').strip()
            enabled = (s.findtext('Sensor_Enabled') or '').strip()
            value_str = (s.findtext('Sensor_Value_String') or '').strip()
            
            # Additional sensor details
            s_number = s.findtext('Sensor_Number', '')
            s_value = s.findtext('Sensor_Value', '')
            s_units = s.findtext('Sensor_Units', '')

            # Skip unnamed or disabled sensors
            if s_name.lower() in IGNORED_NAMES:
                continue
            if enabled.upper() == 'OFF':
                continue

            # Keep only if status is in working set for that type
            allowed = WORKING_STATUS.get(s_type, None)
            if allowed is not None and status_str not in allowed:
                continue

            # Determine alert status
            alert_level = "normal"
            if status_str in ['Active'] and s_type == 'Contact Closure':
                # For contact closures, Active might be an alert depending on sensor
                if any(word in s_name.lower() for word in ['door', 'alarm', 'smoke', 'motion', 'flood']):
                    alert_level = "warning" if 'door' in s_name.lower() else "critical"
            
            # Create unique ID by combining group, type, name, and number
            unique_id = f"{es_name}_{s_type}_{s_name}_{s_number}".replace(' ', '_').replace('-', '_')
            if not unique_id or unique_id == "None_None_None_":
                unique_id = f"{es_name}_{s_type}_{len(sensors)}"
            
            sensors.append({
                'id': unique_id,
                'group': es_name,
                'groupState': es_state,
                'type': s_type,
                'name': s_name,
                'number': s_number,
                'status': status_str,
                'value': value_str,
                'rawValue': s_value,
                'units': s_units,
                'enabled': enabled.upper() == 'ON',
                'alertLevel': alert_level
            })

    # Calculate summary statistics
    sensor_stats = {}
    alert_counts = {'normal': 0, 'warning': 0, 'critical': 0}
    
    for sensor in sensors:
        s_type = sensor['type']
        sensor_stats[s_type] = sensor_stats.get(s_type, 0) + 1
        alert_counts[sensor['alertLevel']] += 1

    return {
        'unit': unit,
        'sensors': sensors,
        'summary': {
            'totalSensors': len(sensors),
            'sensorsByType': sensor_stats,
            'alertCounts': alert_counts,
            'lastPull': datetime.now().isoformat()
        }
    }


async def main():
    parser = argparse.ArgumentParser(description='SiteBoss API - Pull and convert data for backend')
    parser.add_argument('--host', required=True, help='SiteBoss host or IP')
    parser.add_argument('--user', required=True, help='Username')
    parser.add_argument('--pass', dest='password', required=True, help='Password')
    parser.add_argument('--output', default='siteboss_api_data.json', help='Output JSON filename')
    parser.add_argument('--save-xml', action='store_true', help='Also save raw XML file')
    args = parser.parse_args()

    try:
        print("🚀 SiteBoss API Data Puller")
        print(f"   Target: {args.host}")
        print(f"   Output: {args.output}")
        
        # Step 1: Pull XML data
        xml_data = await pull_xml_data(args.host, args.user, args.password)
        
        # Step 2: Convert to JSON
        json_data = parse_xml_to_json(xml_data)
        
        # Step 3: Save JSON for API consumption
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"✅ JSON data saved to: {args.output}")
        
        # Step 4: Optionally save raw XML
        if args.save_xml:
            xml_filename = args.output.replace('.json', '.xml')
            with open(xml_filename, 'w', encoding='utf-8') as f:
                f.write(xml_data)
            print(f"📄 Raw XML saved to: {xml_filename}")
        
        # Step 5: Display summary
        unit = json_data['unit']
        summary = json_data['summary']
        
        print(f"\n📊 Data Summary:")
        print(f"   Site: {unit['siteName']} (Serial: {unit['serial']})")
        print(f"   Location: {unit['location']['latitude']}, {unit['location']['longitude']}")
        print(f"   Last Update: {unit['timestamp']['date']} {unit['timestamp']['time']}")
        print(f"   Total Sensors: {summary['totalSensors']}")
        print(f"   Alerts: {summary['alertCounts']['critical']} critical, {summary['alertCounts']['warning']} warnings")
        
        print(f"\n🔌 Backend Integration Ready!")
        print(f"   JSON endpoint data: {args.output}")
        print(f"   File size: {Path(args.output).stat().st_size:,} bytes")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    exit(asyncio.run(main()))
