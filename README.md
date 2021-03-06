# bashwx/bashwxplus0.1 -A.Nelson- 
bashwx is a python3 script that will put the current weather conditions, public IP and local IP in your .bashrc file to be displayed when you login

For the script to run correctly you will need to obtain an API key from https://home.openweathermap.org/users/sign_up
and add it to "app_id = " value. The service is free. Following that, place bashwx in /usr/sbin/ and setup a chrontab to run
it hourly or half-hourly or whenever you want. I intitally wanted the script to run evry time that .bashrc was called but that will produce an error.

When you login to your shell the script will output the following:<br>
[Local weather]: 81.68 F, with clear sky<br>
[Your public IP is]: x.x.x.x [Local IP]: 192.168.x.x<br>
-=skywalker@deathstar=-:[~/scripts/python/working]#<br>

Additionally you can add the following lines to the bottm of your .bashrc to offer more info:

echo -e "Welcome to \e[0;37m[$(hostname)]\e[0m You are logged in as user \e[0;37m[$USER]\e[0m"<br>
echo -e "[Local time]: \e[0;37m$(date)\e[0m."<br>

All highlighting is white text so you may want to change that depending of your Term profile.

Hope you enjoy it!

**bashwxplus**

bashwxplus offers more data than bashwx. It will display your MOTD in a rainbow color format and much more weather data as well as astronomy. Instead of using openweathermap.org's api I opted for weatherunderground which offers more weather related data for the same amount of api calls. It is also free unless you plan on running over your call limit. You can sign up for an API key here: https://www.wunderground.com/weather/api/ 

to use **bashwxplus** you will have to run the script as with bashwx but in your .bashrc file you want to add the following lines to the bottom of the file.

cat ~/bashwx/motdplus<br>
echo<br>
if [ -s ~/bashwx/.alerts ]; then<br>
  echo ' To view active weather alerts type ''cat ~/bashwx/.alerts'<br>
fi<br>

setup a cron job to run every fifteen minutes:

$> crontab -e<br>
0/15 * * * * ~/bashwx/bashwxplus0.1.py<br>

the output will appear as follows:

**MOTD HERE** 

Welcome [skywalker]<br>
<br>
 Your Public IP is [x.x.x.x] Your Local IP is [192.168.2.5]<br>
<br>
 Weather at [City, ST] from station [STATIONID]<br>
<br>
 Today's Forecast: [Sunny. High near 85F. Winds S at 10 to 15 mph.]<br>
 Conditions: [Partly Cloudy]<br>
 Winds: [Calm]<br>
 Temp: [62.1 F] feels like: [62.1 F]<br>
 Heat Index: [NA F] Wind Chill: [NA F] Dew Point: [58 F]<br>
 Humidity: [86%]<br>
 Barometric Pressure: [1016 mB (+)]<br>
 Rain Gauge: [0.00 in hourly] [0.00 in daily]<br>
 Moon Phase: [Waxing Crescent] illuminated [44%]<br>
 Sunrise: [6:32] Sunset: [20:02]<br>
 UV Levels: [1.0 mW/cm2] Radiation Level [148 W/m2] Visibility: [10.0 Miles]<br>
 Active alert: [Flood Warning]<br>
 [Last Updated on May 2, 8:14 AM CDT]<br>
<br>
 Verse of the Day: ["You also are among them, called to belong to Jesus Christ." - Romans 1:6]<br>
<br>
 To view active weather alerts type "cat /home/user/bashwx/.alerts"<br>
skywalker@endor:~$ <br>

