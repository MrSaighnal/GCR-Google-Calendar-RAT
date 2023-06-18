# GCR-Google-Calendar-RAT
Google Calendar RAT is a PoC of Command&amp;Control over Google Calendar Events

# How to use it
- Setup a Google service account and obtain the credentials.json file
- Create a new Google calendar and share it with the new created service account
- Once executed on the target machine an event with a unique target ID is automatically created autoexecuting the "whoami" command
- Use the following syntax in the event description for the communication =>   CLEAR_COMMAND|BASE64_OUTPUT
  ### Examples:
  - "whoami|"
  - "net users|"
