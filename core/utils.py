# # utils.py
# import datetime
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from django.conf import settings

# def create_google_calendar_event(appointment):
#     SCOPES = ['https://www.googleapis.com/auth/calendar']
#     credentials = service_account.Credentials.from_service_account_file(
#         settings.GOOGLE_CALENDAR_CREDENTIALS_JSON, scopes=SCOPES)
    
#     delegated_credentials = credentials.with_subject(appointment.doctor.user.email)
    
#     service = build('calendar', 'v3', credentials=delegated_credentials)
    
#     event = {
#         'summary': f'Appointment with {appointment.doctor.user.get_full_name()}',
#         'description': f'Speciality: {appointment.speciality}',
#         'start': {
#             'dateTime': f"{appointment.date}T{appointment.start_time.isoformat()}",
#             'timeZone': 'UTC',
#         },
#         'end': {
#             'dateTime': f"{appointment.date}T{appointment.end_time.isoformat()}",
#             'timeZone': 'UTC',
#         },
#         'attendees': [
#             {'email': appointment.patient.email},
#             {'email': appointment.doctor.user.email},
#         ],
#     }
    
#     service.events().insert(calendarId='primary', body=event).execute()
#     return True


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


# def insert_event(request):
#     credentials = Credentials(**request.session['credentials'])
    
#     service = build('calendar', 'v3', credentials=credentials)
    
#     event = {
#       'summary': 'Test Event',
#       'location': '800 Howard St., San Francisco, CA 94103',
#       'description': 'A chance to hear more about Google\'s developer products.',
#       'start': {
#         'dateTime': '2024-07-09T09:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#       },
#       'end': {
#         'dateTime': '2024-07-09T17:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#       },
#       'recurrence': [
#         'RRULE:FREQ=DAILY;COUNT=2'
#       ],
#       'attendees': [
#         {'email': 'lpage@example.com'},
#         {'email': 'sbrin@example.com'},
#       ],
#       'reminders': {
#         'useDefault': False,
#         'overrides': [
#           {'method': 'email', 'minutes': 24 * 60},
#           {'method': 'popup', 'minutes': 10},
#         ],
#       },
#     }
    
#     event = service.events().insert(calendarId='primary', body=event).execute()
#     return HttpResponse(f'Event created: {event.get("htmlLink")}')