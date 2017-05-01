#!/usr/bin/env python3

import grequests, socket
from colorama import Fore, Back, Style
from colr import Colr as C
import os

#build the query with the api keys given to us from OW
api_key = ' ' #insert wunderground api key here
URLS = ['http://api.wunderground.com/api/7' + api_key + '/conditions/q/autoip.json',
        'http://api.wunderground.com/api/' + api_key + '/alerts/q/autoip.json',
        'http://api.wunderground.com/api/' + api_key + '/forecast/q/autoip.json',
        'http://api.wunderground.com/api/'+ api_key + '/astronomy/q/autoip.json',
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
    local = current_wx['display_location']['full'] #full geographical name
    wx_station = current_wx['station_id'] #station ID we're using
    weather = current_wx['weather'] #current conditions
    temp_f = current_wx['temp_f'] #temp in F
    feels = current_wx['feelslike_f'] #feels like
    heatindex = current_wx['heat_index_f'] #heat index
    windchill = current_wx['windchill_f'] #wind chill
    dewpoint = current_wx['dewpoint_f'] #dew point
    wind = current_wx['wind_string'] #wind data
    pressure = current_wx['pressure_mb'] #barometric pressure
    trend = current_wx['pressure_trend'] #pressure change (rising (+), falling(-))
    rain = current_wx['precip_today_in'] #daily precipitation
    h_rain = current_wx['precip_1hr_in'] #hourly precipitation
    time = current_wx['observation_time'] #observation time
    humid = current_wx['relative_humidity'] #realtive humidity
    visible = current_wx['visibility_mi'] #visibility (atmospheric haze levels)
    uv_index =current_wx['UV'] #uv index
    radiation = current_wx['solarradiation']
    forecast = wx_fcst['fcttext']
    wx_alrt = []
    alrt_msg = []
    
    with open(alerts_file, 'w') as af:
        if len(wx_alert) > 0:
            num_alert = len(wx_alert)
            for n in range(num_alert):
               alert = str(Fore.WHITE + Back.RED + alerts[wx_alert[n]['type']] + Fore.RESET + Back.RESET) #active weather alert/statement
               wx_alrt.insert(n, alert)
               message = str(Style.BRIGHT + wx_alert[n]['message'] + Style.RESET_ALL)
               alrt_msg.insert(n, message)      
               af.write(alert + '\n' + ''.join(message))
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
    sunrise = str(astro['sunrise']['hour'] + ':' + astro['sunrise']['minute'])
    sunset = str(astro['sunset']['hour'] + ':' + astro['sunset']['minute'])
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
        f.write(' Weather at [' + Fore.CYAN + Style.BRIGHT + local + Style.RESET_ALL + '] from station [' + Fore.CYAN + Style.BRIGHT + wx_station + Style.RESET_ALL + ']\n\n')
        f.write(' Today\'s Forecast: [' + Fore.CYAN + Style.BRIGHT + forecast + Style.RESET_ALL + ']\n')
        f.write(' Conditions: [' + Fore.CYAN + Style.BRIGHT + weather + Style.RESET_ALL + ']\n')
        f.write(' Winds: [' + Fore.CYAN + Style.BRIGHT + wind + Style.RESET_ALL + ']\n')
        f.write(' Temp: [' + Fore.CYAN + Style.BRIGHT + str(temp_f) + ' F' + Style.RESET_ALL + '] feels like: [' + Fore.CYAN + Style.BRIGHT + str(feels) + ' F' + Style.RESET_ALL + ']\n')
        f.write(' Heat Index: [' + Fore.CYAN + Style.BRIGHT + str(heatindex) + ' F' + Style.RESET_ALL + '] Wind Chill: [' + Fore.CYAN + Style.BRIGHT + str(windchill) + ' F' + Style.RESET_ALL + '] Dew Point: [' + Fore.CYAN + Style.BRIGHT + str(dewpoint) + ' F' + Style.RESET_ALL + ']\n')
        f.write(' Humidity: [' + Fore.CYAN + Style.BRIGHT + humid + Style.RESET_ALL + ']\n')
        f.write(' Barometric Pressure: [' + Fore.CYAN + Style.BRIGHT + str(pressure) + ' mB' + ' (' + trend + ')' + Style.RESET_ALL + ']\n')
        f.write(' Rain Gauge: [' + Fore.CYAN + Style.BRIGHT + str(h_rain) + ' in' + Style.RESET_ALL + ' hourly] ' + '[' + Fore.CYAN + Style.BRIGHT + str(rain) + ' in' + Style.RESET_ALL + ' daily]\n') 
        f.write(' Moon Phase: [' + Fore.CYAN + Style.BRIGHT + moon_phase + Fore.RESET + Style.RESET_ALL + '] illuminated [' + Fore.CYAN + Style.BRIGHT + str(illum) + '%' + Fore.RESET + Style.RESET_ALL + ']\n') 
        f.write(' Sunrise: [' + Fore.CYAN + Style.BRIGHT + sunrise + Style.RESET_ALL + '] Sunset: [' + Fore.CYAN + Style.BRIGHT + sunset + Style.RESET_ALL + ']\n')
        f.write(' UV Levels: [' + Fore.CYAN + Style.BRIGHT + str(uv_index) + ' mW/cm2' + Fore.RESET + '] Radiation Level [' + Fore.CYAN + str(radiation) + ' W/m2' + Fore.RESET + '] Visibility: [' + Fore.CYAN + str(visible) + ' Miles' + Style.RESET_ALL + ']\n')
        f.write(' Active alert: [' + (', '.join(wx_alrt)) + ']\n')
        f.write(' [' + Fore.CYAN + Style.BRIGHT + time + Style.RESET_ALL + ']\n\n')
        f.write(' Verse of the Day: [' + Fore.CYAN + Style.BRIGHT + "\"" + vod_text + "\" - " + vod_book + ' ' + vod_chap + ":" + vod_verse + Style.RESET_ALL + ']\n')
        

except (AttributeError, NameError):
    raise


    
 
