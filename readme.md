# INFOSCHILD

Program to control the OIO Infoschild (created for 36c3)
Opens an HTTP server on 0.0.0.0:80 to cast votes.

All LEDs will be in Infoschild.WHITE (#EEEEEE) at startup.
There are two parts of the Infoschild with a separate behaviour: 

- Spacestation: blinks twice, when a vote is cast
- Text: changes color from Infoschild.ORANGE to Infoschild.WHITE to Infoschild.GREEN depending on the last X votes

# Routes

- `/` - show current hope
- `/destruction` - vote for destruction (redirects to `/`)
- `/hope` - vote for hope (redirects to `/`)
- `/chaos` - ?

# setup

    sudo pip3 install aiohttp rpi_ws281x

# run

    sudo python3 ./run.py

# run at startup

    ./prepare-service.sh