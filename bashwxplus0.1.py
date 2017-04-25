#!/usr/bin/env python3

import grequests, socket
from colorama import Fore, Style
from colr import Colr as C
import os

#build the query with the api keys given to us from OW
api_id = '' ##insert your API key here to retrieve weather data
URLS = ['http://api.wunderground.com/api/'+api_id+'/conditions/q/autoip.json',
        'http://www.ourmanna.com/verses/api/get/?format=json',
        'http://quotes.rest/qod.json',
        'http://httpbin.org/ip']

home_dir = os.environ['HOME']
work_dir = home_dir + '/bashwx/'
plus_file = work_dir + 'motdplus'

try:
    requests = (grequests.get(url) for url in URLS)
    responses = grequests.map(requests)
    data = [response.json() for response in responses]
    
    current_wx = data[0]['current_observation']
    vod = data[1]['verse']['details']
    qod = data[2]['contents']['quotes'][0]
    p_ip = data[3]['origin']
    
    #weather data
    loc = current_wx['observation_location']
    local = loc['city'] #full geographical name
    wx_station = current_wx['station_id'] #station ID we're using
    weather = current_wx['weather'] #current conditions
    temp_f = current_wx['temp_f'] #temp in F
    feels = current_wx['feelslike_f'] #feels like
    wind = current_wx['wind_string'] #wind data
    pressure = current_wx['pressure_mb'] #barometric pressure
    trend = current_wx['pressure_trend'] #pressure change (rising (+), falling(-))
    rain = current_wx['precip_today_in'] #daily precipitation
    time = current_wx['observation_time'] #observation time
    humid = current_wx['relative_humidity'] #realtive humidity

    #verse of the day
    verse = vod['text']
    version = vod['version']
    ref = vod['reference']

    #quote of the day
    quote = qod['quote']
    author = qod['author']
   
    #local ip
    loc_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    loc_ip.connect(('8.8.4.4', 0))
    locip = loc_ip.getsockname()[0] 
    
    #motd 
    f = open('/etc/motd', 'r')
    motd = f.readlines()
    f.close()
    
    #username
    user = os.environ['LOGNAME']

    with open(plus_file, 'w') as f:
        f.write(str(C(' '.join(motd)).gradient(name='blue')))
        f.write(Style.BRIGHT + '\nWelcome [' + Fore.CYAN + user + Fore.RESET + ']\n\n' + Style.RESET_ALL)
        f.write(Style.BRIGHT  + 'Your ' + Fore.CYAN + 'Public IP ' + Fore.RESET + 'is [' + Fore.CYAN + p_ip + Fore.RESET + '] Your ' + Fore.CYAN + 'Local IP ' + Fore.RESET + 'is [' + Fore.CYAN + locip + Fore.RESET + ']\n\n' + Style.RESET_ALL)
        f.write(' Weather at [' + Fore.CYAN + Style.BRIGHT + local + Style.RESET_ALL + Fore.RESET + '] from station [' + Fore.CYAN + Style.BRIGHT + wx_station + Style.RESET_ALL + Fore.RESET + ']\n')
        f.write(' Conditions: [' + Fore.CYAN + Style.BRIGHT + weather + Style.RESET_ALL + Fore.RESET + ']\n')
        f.write(' Winds: [' + Fore.CYAN + Style.BRIGHT + wind + Style.RESET_ALL + Fore.RESET + ']\n')
        f.write(' Temp: [' + Fore.CYAN + Style.BRIGHT + str(temp_f) + Style.RESET_ALL + Fore.RESET + '] Feels like: [' + Fore.CYAN + Style.BRIGHT + str(feels) + Style.RESET_ALL + Fore.RESET + ']\n')
        f.write(' Humidity: [' + Fore.CYAN + Style.BRIGHT + humid + Style.RESET_ALL + Fore.RESET + ']\n')
        f.write(' Barometric Pressure: [' + Fore.CYAN + Style.BRIGHT + str(pressure) + ' mB' + ' (' + trend + ')' + Fore.RESET + Style.RESET_ALL + ']\n')
        f.write(' [' + Fore.CYAN + Style.BRIGHT + time + Fore.RESET + Style.RESET_ALL + ']\n\n')
        f.write('Daily Bible Verse: ' + Fore.CYAN + Style.BRIGHT + verse + Fore.RESET + ' - ' + ref + Fore.RESET + Style.RESET_ALL +' [' + Fore.CYAN + Style.BRIGHT+ version + Style.RESET_ALL + ']\n\n')
        f.write('Quote of the Day: ' + Fore.CYAN + Style.BRIGHT + quote + Fore.RESET + Style.RESET_ALL + ' - [' + Style.BRIGHT + Fore.CYAN + author + Fore.RESET + Style.RESET_ALL + ']\n')

except (AttributeError, NameError):
    raise


    
 
