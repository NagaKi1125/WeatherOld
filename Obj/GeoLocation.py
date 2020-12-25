
class GeoLocation:
    def __init__(self, ip, latitude, longitude, city, country, time):
        self.ip = ip
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.country = country
        self.time = time

    def address(self):
        return 'Ip: '+self.ip+ '\nLatitude = '+self.latitude +'\nLongitude = '+self.longitude + '\nAddress: '+self.city+', '+self.country

    def ip(self):
        return self.ip

    def latitude(self):
        return self.latitude

    def longitude(self):
        return self.longitude

    def city(self):
        return self.city

    def country(self):
        return self.country

    def time(self):
        return self.time
