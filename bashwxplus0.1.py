#!/usr/bin/env python3

import grequests, socket
from colorama import Fore, Back, Style
from colr import Colr as C
import os

#build the query with the api keys given to us from OW
URLS = ['http://api.wunderground.com/api/705c1ebaea010d2e/conditions/q/autoip.json',
        'http://api.wunderground.com/api/705c1ebaea010d2e/alerts/q/autoip.json',
        'http://api.wunderground.com/api/705c1ebaea010d2e/forecast/q/autoip.json',
        'http://api.wunderground.com/api/705c1ebaea010d2e/astronomy/q/autoip.json',
        'http://httpbin.org/ip',
        'http://labs.bible.org/api/?passage=votd&type=json']

alerts = {'HUR': 'Hurricane Local Statement', 
          'TOR': 'Tornado Warning',
          'TOW': 'Tornado Watch',
          'WRN': 'Severe Thunderstorm Warning',
          'SEW': 'Severe Thunderstorm Watch',
          'WIN': 'Winter Weather Advisory',
          'FLO': 'Flood Warning',
          'WAT': 'Flood Watch/Statement',
          'WND': 'High Wind Advisory',
          'SVR': 'Severe Weather Statement',
          'HEA': 'Heat Advisory',
          'FOG': 'Dense Fog Advisory',
          'FIR': 'Fire Weather Advisory',
          'VOL': 'Volcanic Activity Statement',
          'HWW': 'Hurricane Wind Warning',
          'REC': 'Record Set',
          'REP': 'Public Reports',
          'PUB': 'Public Information Statement',
          ' ' : 'None'}

home_dir = os.environ['HOME']
work_dir = home_dir + '/bashwx/'
plus_file = work_dir + 'motdplus'
alerts_file = work_dir + '.alerts'

try:
    requests = (grequests.get(url) for url in URLS)
    responses = grequests.map(requests)
    data = [response.json() for response in responses]
    
    current_wx = data[0]['current_observation']
    wx_alert = data[1]['alerts']
    wx_fcst = data[2]['forecast']['txt_forecast']['forecastday'][0]
    astro = data[3]['moon_phase']
    p_ip = data[4]['origin']
    votd = data[5][0]
    
    #weather data
    loc = current_wx['observation_location']
    local = loc['city'] #full geographical name
    wx_station = current_wx['station_id'] #station ID we're using
    weather = current_wx['weather'] #current conditions
    temp_f = current_wx['temp_f'] #temp in F
    feels = current_wx['feelslike_f'] #feels like
    wind = current_wx['wind_string'] #wind data
    gust = current_wx['wind_gust_mph'] #wind gust
    pressure = current_wx['pressure_mb'] #barometric pressure
    trend = current_wx['pressure_trend'] #pressure change (rising (+), falling(-))
    rain = current_wx['precip_today_in'] #daily precipitation
    time = current_wx['observation_time'] #observation time
    humid = current_wx['relative_humidity'] #realtive humidity
    forecast = wx_fcst['fcttext']
    
    if len(wx_alert) > 0:
         alert = str(Fore.WHITE + Back.RED + wx_alert['type'] + Fore.RESET + Back.RESET) #active weather alert/statement
         message = str(Style.BRIGHT + wx_alert[1]['alerts']['message'] + Style.RESET_ALL)
         with open(alerts_file, 'w') as af:
             af.write(alert + '\n' + message)
    else:
         alert = (Fore.CYAN + Style.BRIGHT + 'No active weather alerts or statements' + Fore.RESET + Style.RESET_ALL)
      
    #local ip
    loc_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    loc_ip.connect(('8.8.4.4', 0))
    locip = loc_ip.getsockname()[0] 

    #votd
    vod_book = votd['bookname']
    vod_chap = votd['chapter']
    vod_verse = votd['verse']
    vod_text = votd['text']
    
    #astronomy
    moon_phase = astro['phaseofMoon']
    illum = astro['percentIlluminated']  
    
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
        f.write(' Weather at [' + Fore.CYAN + Style.BRIGHT + local + Style.RESET_ALL + Fore.RESET + '] from station [' + Fore.CYAN + Style.BRIGHT + wx_station + Style.RESET_ALL + Fore.RESET + ']\n\n')
        f.write(' Today\'s Forecast: [' + Fore.CYAN + Style.BRIGHT + forecast + Fore.RESET + Style.RESET_ALL + ']\n')
        f.write(' Conditions: [' + Fore.CYAN + Style.BRIGHT + weather + Style.RESET_ALL + Fore.RESET + ']\n')
        f.write(' Winds: [' + Fore.CYAN + Style.BRIGHT + wind + Style.RESET_ALL + Fore.RESET + '] gusting to [' + Fore.CYAN + Style.BRIGHT + str(gust) + 'MPH' + Fore.RESET + Style.RESET_ALL + ']\n')
        f.write(' Temp: [' + Fore.CYAN + Style.BRIGHT + str(temp_f) + Style.RESET_ALL + Fore.RESET + '] feels like: [' + Fore.CYAN + Style.BRIGHT + str(feels) + Style.RESET_ALL + Fore.RESET + ']\n')
        f.write(' Humidity: [' + Fore.CYAN + Style.BRIGHT + humid + Style.RESET_ALL + Fore.RESET + ']\n')
        f.write(' Barometric Pressure: [' + Fore.CYAN + Style.BRIGHT + str(pressure) + ' mB' + ' (' + trend + ')' + Fore.RESET + Style.RESET_ALL + ']\n')
        f.write(' Moon Phase: [' + Fore.CYAN + Style.BRIGHT + moon_phase + Fore.RESET + Style.RESET_ALL + '] illuminated [' + Fore.CYAN + Style.BRIGHT + str(illum) + '%' + Fore.RESET + Style.RESET_ALL + ']\n') 
        f.write(' Active alert: [' + alert + ']\n')
        f.write(' [' + Fore.CYAN + Style.BRIGHT + time + Fore.RESET + Style.RESET_ALL + ']\n\n')
        f.write(' Verse of the Day: [' + Fore.CYAN + Style.BRIGHT + "\"" + vod_text + "\" - " + vod_book + ' ' + vod_chap + ":" + vod_verse + Fore.RESET + Style.RESET_ALL + ']\n')
        

except (AttributeError, NameError):
    raise


    
 
