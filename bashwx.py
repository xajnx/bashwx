#!/usr/bin/env python3

""" 
add current weather conditions, local ip and public IP 
to your bash login 

"""

import sys, os
import requests, socket
import errno

home = os.getenv("HOME")
#build the query with the api keys given to us from OW
app_id = '' #enter API key obtain from OpenWeatherMap.org
base_url = 'http://api.openweathermap.org/data/2.5/weather?'
headers = {'user-agent':'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'} #pretend we're a browser

try:  
    #first retrieve current location from wlan information
    loc_url = 'http://freegeoip.net/json/'
    loc_rqst = requests.get(loc_url)
    loc_resp = loc_rqst.json()
    lat = loc_resp['latitude']
    lon = loc_resp['longitude']
    ip = loc_resp['ip']
  
    #now retrieve weather data for our location
    params = {'lon':lon, 'lat':lat, 'appid':app_id, 'units':'imperial'}
    query = requests.get(base_url, params=params, headers=headers)
    conditions = query.json()['weather']
    temp = query.json()['main']
    wx_c = conditions[0]['description']
    wx_t = temp['temp']

    #get local IP
    loc_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    loc_ip.connect(('8.8.4.4', 0))
    locip = loc_ip.getsockname()[0]  
        
    #output to .bashrc
    out_file = (home+('/.bashrc'))
    rf = open(out_file, 'r')
    lines = rf.readlines()
    rf.close()

    f = open(out_file, 'w')
    f.writelines([item for item in lines[:-2]])

    w = "echo -e \"\e[0;37m[\e[0mLocal weather\e[0;37m]\e[0m: \e[0;37m\"" + str(wx_t) +  "\" F\e[0m with \e[0;37m\"" + str(wx_c) + "\"\e[0m\""
    i = "echo -e \"\e[0;37m[\e[0mYour public IP is\e[0;37m]\e[0m: \e[0;37m\"" + ip + "\"\e[0m \e[0;37m[\e[0mLocal IP\e[0;37m]\e[0m: \e[0;37m\"" + locip + "\"\e[0m\""

    out = [str(w), str(i)]
    f.writelines('\n'.join(out))
    f.close()
              
#handle connection errors
except requests.exceptions.ConnectionError:
    e = "echo [No network detected]: Unable to retrieve data\n"
    f.writelines(str(e[:-3]))
    f.close()
        

