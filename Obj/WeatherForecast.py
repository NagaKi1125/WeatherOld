from datetime import datetime


class DailyForecast:

    def __init__(self, dt, sunrise, sunset, temp_day, temp_morn, temp_eve, temp_night, temp_min, temp_max, pressure,
                 humidity, wind_speed, weather_main, weather_desc, weather_icon, percent_clouds):
        self.dt = dt
        self.sunrise = sunrise
        self.sunset = sunset
        self.temp_day = temp_day
        self.temp_morn = temp_morn
        self.temp_eve = temp_eve
        self.temp_night = temp_night
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.weather_main = weather_main
        self.weather_desc = weather_desc
        self.weather_icon = weather_icon
        self.percent_clouds = percent_clouds

    def getDtInMilies(self):
        return self.dt

    def getDtInDate(self):
        return str(datetime.fromtimestamp(self.dt)).split(' ')[0]

    def getDtInTime(self):
        return str(datetime.fromtimestamp(self.dt)).split(' ')[1]

    def getDtFull(self):
        return datetime.fromtimestamp(self.dt)

    def getSunriseTime(self):
        return str(datetime.fromtimestamp(self.sunrise)).split(' ')[1]

    def getSunSetTime(self):
        return str(datetime.fromtimestamp(self.sunset)).split(' ')[1]

    def getTempAtMorning(self):
        return self.temp_morn

    def getTempAtDay(self):
        return self.temp_day

    def getTempAtEvening(self):
        return self.temp_eve

    def getTempAtNight(self):
        return self.temp_night

    def getTempMin(self):
        return self.temp_min

    def getTempMax(self):
        return self.temp_max

    def getPressure(self):
        return self.pressure

    def getHumidity(self):
        return self.humidity

    def getWindSpeed(self):
        return self.wind_speed

    def getMainWeather(self):
        return self.weather_main

    def getWeatherDescription(self):
        return self.weather_desc

    def getWeatherIcon(self):
        return self.weather_icon

    def getPercentClouds(self):
        return self.percent_clouds


class HourlyForecast:
    def __init__(self, dt, temp, wind_speed, weather_desc, weather_icon, percent_clouds):
        self.dt = dt
        self.temp = temp
        self.wind_speed = wind_speed
        self.weather_desc = weather_desc
        self.weather_icon = weather_icon
        self.percent_clouds = percent_clouds

    def getDtInMilies(self):
        return self.dt

    def getDtInDate(self):
        return str(datetime.fromtimestamp(self.dt)).split(' ')[0]

    def getDtInTime(self):
        return str(datetime.fromtimestamp(self.dt)).split(' ')[1]

    def getDtFull(self):
        return datetime.fromtimestamp(self.dt)

    def getTemp(self):
        return self.temp

    def getWindSpeed(self):
        return self.wind_speed

    def getWeatherDescription(self):
        return self.weather_desc

    def getWeatherIcon(self):
        return self.weather_icon

    def getPercentClouds(self):
        return self.percent_clouds


class CurrentWeather:
    def __init__(self, dt, sunrise, sunset, temp, feels_like, pressure,
                 humidity, visibility, wind_speed, weather_main, weather_desc, weather_icon, percent_clouds):
        self.dt = dt
        self.sunrise = sunrise
        self.sunset = sunset
        self.temp = temp
        self.feels_like = feels_like
        self.pressure = pressure
        self.humidity = humidity
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.weather_main = weather_main
        self.weather_desc = weather_desc
        self.weather_icon = weather_icon
        self.percent_clouds = percent_clouds

    def getDtInMilies(self):
        return self.dt

    def getDtInDate(self):
        return str(datetime.fromtimestamp(self.dt)).split(' ')[0]

    def getDtInTime(self):
        return str(datetime.fromtimestamp(self.dt)).split(' ')[1]

    def getDtFull(self):
        return datetime.fromtimestamp(self.dt)

    def getSunriseTime(self):
        return str(datetime.fromtimestamp(self.sunrise)).split(' ')[1]

    def getSunSetTime(self):
        return str(datetime.fromtimestamp(self.sunset)).split(' ')[1]

    def getTemp(self):
        return self.temp

    def getTempFeelsLike(self):
        return self.feels_like

    def getPressure(self):
        return self.pressure

    def getHumidity(self):
        return self.humidity

    def getVisibility(self):
        return self.visibility

    def getWindSpeed(self):
        return self.wind_speed

    def getMainWeather(self):
        return self.weather_main

    def getWeatherDescription(self):
        return self.weather_desc

    def getWeatherIcon(self):
        return self.weather_icon

    def getPercentClouds(self):
        return self.percent_clouds

