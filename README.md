<p align="center">
  <img alt="GCR" src="https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/blob/main/images/logo.png?raw=true" height="200" /><br />
<a href="https://twitter.com/mrsaighnal"><img src="https://img.shields.io/twitter/follow/mrsaighnal?style=social" alt="twitter" style="text-align:center;display:block;"></a>
 
</p>
<p align="left">

# GCR - Google Calendar RAT
Google Calendar RAT is a PoC of Command&amp;Control (C2) over Google Calendar Events, This tool has been developed for those circumstances where it is difficult to create an entire red teaming infrastructure. To use GRC, only a Gmail account is required.
The script creates a 'Covert Channel' by exploiting the event descriptions in Google Calendar. The target will connect directly to Google."
It could be considered as a layer 7 application Covert Channel (but some friends would say it cannot be :) very thanks to my mates "Tortellini" https://aptw.tf )

![image](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/8e4e1f83-8141-408d-8910-e8e92896b8e4)

## POC
![poc](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/b83e6f28-36bd-454d-9c04-87095a280b1a)

## How it works
GCR attempt to connect to a valid shared Google Calendar link and after generating a unique ID check for any yet-to-be-executed commands.
If it is not able to find any command, it creates a new one (fixed to "whoami") as a proof of connection.
Every event is composed by two part:
1. The Title, which contains the unique ID, it means you can schedule multiple commands creating events having the same unique ID as name


![image](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/df999259-3b1b-419f-b555-204fc5dc2dbf)

3. The Description, which contains the command to execute and the base64 encoded output using the pipe symbol as separator "|"


![image](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/5f2630e2-5591-48d1-bae2-5695afa8a33e)

## Workflow Attack
![Disegno senza titolo (2)](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/99bec717-4e9a-4880-9a5a-b038666441b6)



## What a SOC analyst/Blue Teamer will see?
Focusing specifically on the network aspect, the only connections established will be to Google's servers, making the connection appear completely legitimate.
Let's check with process hacker:
![image](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/a2bf1f24-90a6-49ab-9a12-bcc7c999e2b3)
![image](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/66dbd7b5-4060-4829-9229-99bb0c5a19e5)


which results in this
![image](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/244e9acf-44a9-45b7-92f5-f61d911446a3)
![image](https://github.com/MrSaighnal/GCR-Google-Calendar-RAT/assets/47419260/14c875fc-c28f-45d6-94c1-64e3dd02606b)



## How to use it
- Setup a Google service account and obtain the credentials.json file, place the file in the same directory of the script
- Create a new Google calendar and share it with the new created service account
- Edit the script to point your calendar address
- Once executed on the target machine an event with a unique target ID is automatically created autoexecuting the "whoami" command
- Use the following syntax in the event description for the communication =>   CLEAR_COMMAND|BASE64_OUTPUT
  ### Examples:
  - "whoami|"
  - "net users|"
- The date is fixed on May 30th, 2023. You can create unlimited events using the unique ID as the event name.

## Disclaimer and notes
I prefer to consider this project as a game rather than an experiment :)
Please do not use it for illegal purpose.
I take no responsibility for the use that will be made of it

IT IS JUST A POC IN PYTHON, PLEASE DO NOT ASK ME HOW TO WEAPONIZE IT!

## Related articles

- [Google](https://services.google.com/fh/files/blogs/gcat_threathorizons_full_oct2023.pdf)

- [Microsoft](https://www.msn.com/en-us/news/technology/even-google-calendar-isnt-safe-from-hackers-any-more/ar-AA1juBQk)

- [Android Headlines](https://www.androidheadlines.com/2023/11/google-calendar-exploited-new-remote-access-trojan-rat.html)

- [BitDefender](https://www.bitdefender.com/blog/hotforsecurity/google-warns-of-google-calendar-rat-exploit-in-security-report/)

- [The Hacker News](https://thehackernews.com/2023/11/google-warns-of-hackers-absing-calendar.html)

- [Linkedin](https://www.linkedin.com/pulse/unmasking-google-calendar-rat-gcr-new-covert-cc-hqq0c/?trk=article-ssr-frontend-pulse_more-articles_related-content-card)

- [Security Affairs](https://securityaffairs.com/153700/hacking/google-calendar-rat-attacks.html)

- [Medium](https://chennylmf.medium.com/unveiling-the-cunning-a-demo-of-google-calendar-rat-exploiting-calendar-service-for-c2-operations-d6ee0b2f8011)

- [PC Magazine](https://www.pcmag.com/news/google-calendar-is-a-potential-tool-for-hackers-to-control-malware)

- [VPNOverview](https://vpnoverview.com/news/google-calendar-can-be-used-to-spread-malware-report-warns/)

- [SoftTonic](https://en.softonic.com/articles/not-even-google-calendar-is-free-from-hackers)

- [Cybersecurity News](https://cybersecuritynews.com/google-calendar-rat/)

- [Cyber Material](https://cybermaterial.com/threat-actors-exploit-google-calendar/)

- [DarkReading](https://www.darkreading.com/cloud/google-cloud-rat-calendar-events-command-and-control)

- [Vulners](https://vulners.com/thn/THN:59821E9D5171515534AD05F1337FF45D)

- [ExploitOne](https://www.exploitone.com/tutorials/this-google-calendar-technique-allows-to-hack-into-companies-without-getting-detected/)

- [Wired (italian)](https://www.wired.it/article/google-calendar-attacchi-informatici-malware/)

- [Punto Informatico (italian)](https://www.punto-informatico.it/google-calendar-nuovo-bersaglio-hacker/)

- [Il Software (italian)](https://www.ilsoftware.it/google-calendar-rat-hacker-sfruttano-calendar-per-i-loro-attacchi/)

- [Red Hot Cyber (italian)](https://www.redhotcyber.com/post/google-calendar-utilizzato-come-comand-control-per-la-gestione-dei-malware/)

## Similar (External) Projects

- [GC2-Sheet (by Lorenzo Grazian)](https://github.com/looCiprian/GC2-sheet)
