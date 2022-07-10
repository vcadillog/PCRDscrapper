# PCRDscrapper

## Discord bot implementation to scrap arena online data from PCRD profiles.

How to use:

First create a discord bot and activate developer mode in advanced settings.
Then modify the profile file with your information like this:

```
USER = 111111111111111111 (COPY YOUR DISCORD USER ID)
MY_CHANNEL_ID = 000000000000000000 (COPY THE DISCORD CHANNEL ID)
TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxx.yyyyyy.zzzzzzzzzzzzzzzzzzzzzzzzzzz' (COPY THE DISCORD BOT TOKEN ID)
```

Install python 3 and requirements with the command in the code folder:

```
pip install -r requirements.txt
```
Setup your device proxy to 8080 (default or a custom port)
To set a proxy in a emulator follow the next guide:
https://github.com/FabulousCupcake/pcr-exporter/wiki/Proxy%3A-Bluestacks-4

Download and install mitmproxy root certificate and install it on your device or emulator.

Follow the next guide to download the certificate:
https://docs.mitmproxy.org/stable/concepts-certificates/

To install the certificate in an emulator follow the next guide: 
https://github.com/FabulousCupcake/pcr-exporter/wiki/Cert%3A-Bluestacks-4

After downloading and installing the certificate in your device run the script command:

```
mitmdump -s main.py -p 8080
```

Then log in the app and tap a profile.

This will display the data received in a proxy in the port 8080 or a custom port.

After the proxy replays the http request you should close the app.

The script will run this indefinetly till you log in again or the server disconnects, only the stated situations stop the script, when the code is restarted it will keep running as the previous state cause the http flow is stored in saved_flows.pickle file.

The script restarts itself (only on linux) after an error is found or no new data is received after a set period of time, should be modified if you are running on windows or do it manually.

Code based on the repository:
https://github.com/FabulousCupcake/pcr-exporter 
