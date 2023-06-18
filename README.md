# GCR-Google-Calendar-RAT
Google Calendar RAT is a PoC of Command&amp;Control over Google Calendar Events
The script creates a 'Covert Channel' by exploiting the event descriptions in Google Calendar. The target will connect directly to Google."
It could be considered as a layer 7 application Covert Channel (but some friends would say it cannot :) very thanks to my mates "Tortellini" https://aptw.tf )

![image](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/8e4e1f83-8141-408d-8910-e8e92896b8e4)


# How to use it
- Setup a Google service account and obtain the credentials.json file, place the file in the same directory of the script
- Create a new Google calendar and share it with the new created service account
- Edit the script to point your calendar address
- Once executed on the target machine an event with a unique target ID is automatically created autoexecuting the "whoami" command
- Use the following syntax in the event description for the communication =>   CLEAR_COMMAND|BASE64_OUTPUT
  ### Examples:
  - "whoami|"
  - "net users|"
- The date is fixed on May 30th, 2023. You can create unlimited events using the unique ID as the event name.

# POC
![poc](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/b83e6f28-36bd-454d-9c04-87095a280b1a)



# Notes
I prefer to consider this project as a game rather than an experiment :)
Please do not use it for illegal purpose.
I take no responsibility for the use that will be made of it

IT IS JUST A POC, PLEASE DO NOT ASK ME HOW TO WEAPONIZE IT!
