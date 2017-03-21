# bashwx -A.Nelson- aaron.nelson805@gmail.com
bashwx is a python3 script that will put the current weather conditions, public IP and local IP in your .bashrc file to be displayed when you login

For the script to run correctly you will need to obtain an API key from https://home.openweathermap.org/users/sign_up
and add it to "app_id = " value. The service is free. Following that, place bashwx in /usr/sbin/ and setup a chrontab to run
it hourly or half-hourly or whenever you want. I intitally wanted the script to run evry time that .bashrc was called but that will produce an error.

When you login to your shell the script will output the following:
[Local weather]: 81.68 F, with clear sky
[Your public IP is]: x.x.x.x [Local IP]: 192.168.x.x
-=skywalker@deathstar=-:[~/scripts/python/working]#

Additionally you can add the following lines to the bottm of your .bashrc to offer more info:

echo -e "Welcome to \e[0;37m[$(hostname)]\e[0m You are logged in as user \e[0;37m[$USER]\e[0m"
echo -e "[Local time]: \e[0;37m$(date)\e[0m."

All highlighting is white text so you may want to change that depending of your Term profile.

Hope you enjoy it!

