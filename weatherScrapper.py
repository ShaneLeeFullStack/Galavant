import requests
import pyowm
import geocoder

# owm = pyowm.OWM('875ff6231ea55034e1523534070aecdc')
# mgr = owm.weather_manager()
# weather = mgr.weather_at_place('Tokyo,JP').weather
# temp_dict_kelvin = weather.temperature() # a dict in Kelvin units (default when no temperature units provided)
# max_temp = temp_dict_kelvin['temp_min']
# min_temp = temp_dict_kelvin['temp_max']
# temp_dict_fahrenheit = weather.temperature('fahrenheit') # a dict in Fahrenheit units
# temp_dict_celsius = weather.temperature('celsius') # guess?


def weatherInfo():
    # setup for geocoder
    g = geocoder.ip('me')
    # print(g.latlng)

    #setup for OpenWeatherMap
    owm = pyowm.OWM('875ff6231ea55034e1523534070aecdc')
    mgr = owm.weather_manager()

    #getting the city location
    my_city_id = 12345
    my_city_lat = g.latlng[0]
    my_city_lng = g.latlng[1]
    # print("my_city_lat: ", my_city_lat)
    # print("my_city_lng: ", my_city_lng)

    observation = mgr.weather_at_coords(my_city_lat, my_city_lng)
    weather = observation.weather

    temp_dict_kelvin = weather.temperature('fahrenheit')
    # TODO: find current temperature
    # cur_temp = temp_dict_kelvin['']
    max_temp = temp_dict_kelvin['temp_max']
    min_temp = temp_dict_kelvin['temp_min']

    # rain section
    # TODO Rain data not working
    # Pulling weather data for a specific location
    # rain_dict = mgr.weather_at_coords(my_city_lat, my_city_lng).weather.rain
    # rain_one = rain_dict['1h']
    # rain_thr = rain_dict['3h']

    # sunrise and sunset times
    sunrise_unix = weather.sunrise_time()
    sunrise_iso = weather.sunrise_time(timeformat='iso')
    sunrise_date = weather.sunrise_time(timeformat='date')
    sunset_unix = weather.sunset_time()
    sunset_iso = weather.sunset_time(timeformat='iso')
    sunset_date = weather.sunset_time(timeformat='date')

    w_status = weather.status
    w_det_status = weather.detailed_status

    # print("Max temp today: ", max_temp)
    # print("Min temp today: ", min_temp)
    # print("Status: ", w_status)
    # print("Detailed status: ", w_det_status)
    # print("Sunrise Unix: ", sunrise_unix)
    # print("Sunrise ISO: ", sunrise_iso)
    # print("Sunrise Date: ", sunrise_date)
    # print("Sunset Unix: ", sunset_unix)
    # print("Sunset ISO: ", sunset_iso)
    # print("Sunset Date: ", sunset_date)
    # print("Rain in the last hour: ", rain_one)
    # print("Rain in the last 3 hours: ", rain_thr)
    return ("Sunset is at: " + sunset_iso + " Sunrise is at: " + sunrise_iso + " Weather today is: " + w_det_status)

weatherInfo()