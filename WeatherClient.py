import time
import socket
import geocoder
import sys
import os
import urllib.request
from Obj import GeoLocation
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui, sip, QtWebKitWidgets
from Layout import client
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from pyqtlet import L, MapWidget

# click count
click = 0
mapClick = 0
fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_ip = '127.0.0.1'
udp_port = 8014

# global variable for user location
currLocation = GeoLocation.GeoLocation('', '', '', '', '', '')

weather_api_key = 'b3a64e07a9cb08c942f2d1711c1d47e6'  # for weather


# get current location
def getLocation():
    options = Options()
    options.set_preference("geo.prompt.testing", True)
    options.set_preference("geo.prompt.testing.allow", True)
    options.add_argument("--headless")

    timeout = 60
    driver = webdriver.Firefox(executable_path='geckodriver/geckodriver.exe', options=options)
    driver.get("https://whatmylocation.com/")
    WebDriverWait(driver, timeout)
    time.sleep(1)

    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
    longitude = [x.text for x in longitude]
    longitude = str(longitude[0])

    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
    latitude = [x.text for x in latitude]
    latitude = str(latitude[0])

    road = driver.find_elements_by_xpath('//*[@id="street"]/span')
    road = [x.text for x in road]
    road = str(road[0])

    province = driver.find_elements_by_xpath('//*[@id="county"]/span')
    province = [x.text for x in province]
    province = str(province[0])

    district = driver.find_elements_by_xpath('//*[@id="city"]/span')
    district = [x.text for x in district]
    district = str(district[0])

    country = driver.find_elements_by_xpath('//*[@id="country"]/span[1]')
    country = [x.text for x in country]
    country = str(country[0])

    ti = datetime.today()

    driver.quit()

    g = geocoder.ip('')
    geo = GeoLocation.GeoLocation(ip=g.ip, latitude=latitude, longitude=longitude,
                                  city=road + '\n ' + district + ', ' + province, country=country, time=ti)

    return geo


# get province
def allProvince():
    provinceList = []
    provinceFile = open('Province.txt', encoding="utf8")
    lines = provinceFile.readlines()
    provinceList.append("Click to choose place")
    for i in lines:
        pr = i.split(',')
        provinceList.append(pr[0].strip() + ', ' + pr[1].strip() + ', ' + pr[2].strip())
    return provinceList


# weather icon
def showIcon(iconName, size):
    if size == 0:
        url = 'http://openweathermap.org/img/wn/' + iconName + '.png'
    else:
        url = 'http://openweathermap.org/img/wn/' + iconName + '@2x.png'
    url_data = urllib.request.urlopen(url).read()
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(url_data)
    return pixmap


def hourlyForecast(hourly):
    # 0 dt, 1 temp, 2 icon, 3 desc, 4 wind, 5 cloud
    hourlyFore = QtWidgets.QHBoxLayout()
    for i in hourly:
        if i == '':
            continue
        else:
            hourlyDetails = i.split('_')  # list of hourly details
            mainCont = QtWidgets.QWidget()
            cont = QtWidgets.QVBoxLayout()
            font = QtGui.QFont()
            if hourlyDetails[0] == '00:00:00':
                font.setBold(True)
                font.setUnderline(True)
            else:
                font.setUnderline(True)

            lblTime = QtWidgets.QLabel('{}'.format(hourlyDetails[0]))
            lblTime.setFont(font)
            lblTemp = QtWidgets.QLabel('{} C'.format(hourlyDetails[1]))
            lblIcon = QtWidgets.QLabel()
            lblIcon.setStyleSheet("background-color: rgb(159, 159, 159);")
            lblIcon.setPixmap(showIcon(hourlyDetails[2], 0))
            lblDesc = QtWidgets.QLabel('{}'.format(hourlyDetails[3]))
            lblWindCloud = QtWidgets.QLabel('{} m/s - {} %'.format(hourlyDetails[4], hourlyDetails[5]))
            cont.addWidget(lblTime)
            cont.addWidget(lblTemp)
            cont.addWidget(lblIcon)
            cont.addWidget(lblDesc)
            cont.addWidget(lblWindCloud)
            mainCont.setLayout(cont)
            hourlyFore.addWidget(mainCont)

    return hourlyFore


def dailyForecast(daily):
    # 0 dt, 1 icon, 2 minTemp, 3 maxTemp, 4 weatherDesc, 5 humidity, 6 wind_speed, 7 morTemp, 8 dayTemp,
    # 9 eveTemp, 10 nightTemp, 11 sunrise, 12 sunset, 13 clouds, 14 pressure
    boldFont = QtGui.QFont()
    boldFont.setBold(True)
    italicFont = QtGui.QFont()
    italicFont.setItalic(True)

    # 8 days forecast
    dailyForecast = QtWidgets.QVBoxLayout()
    for i in daily:
        if i == '':
            continue
        else:
            dailyDetails = i.split('_')  # list of daily details
            Frame = QtWidgets.QWidget()
            FrameBox = QtWidgets.QVBoxLayout()
            MainDe = QtWidgets.QWidget()
            MainDetails = QtWidgets.QHBoxLayout()
            # details info main
            lblDt = QtWidgets.QLabel('{}'.format(dailyDetails[0]))
            lblDt.setFrameShape(QtWidgets.QFrame.Box)
            lblDt.setFont(boldFont)
            lblIcon = QtWidgets.QLabel()
            lblIcon.setPixmap(showIcon(dailyDetails[1], 0))
            lblIcon.setStyleSheet("background-color: rgb(159, 159, 159);")
            lblMinMax = QtWidgets.QLabel('{}/{} C'.format(dailyDetails[2], dailyDetails[3]))
            lblDescription = QtWidgets.QLabel('{}'.format(dailyDetails[4]))
            lblDescription.setFont(italicFont)
            lblDescription.setAlignment(QtCore.Qt.AlignCenter)
            MainDetails.addWidget(lblDt)
            MainDetails.addWidget(lblIcon)
            MainDetails.addWidget(lblMinMax)
            MainDetails.addWidget(lblDescription)

            # subDetails
            subDe= QtWidgets.QWidget()
            subDetails = QtWidgets.QFormLayout()
            lblHumi = QtWidgets.QLabel('Humidity:')
            lblInfoHumi = QtWidgets.QLabel('{} %'.format(dailyDetails[5]))
            lblWindSpeed = QtWidgets.QLabel('Wind Speed:')
            lblInfoWindSpd = QtWidgets.QLabel('{} m/s'.format(dailyDetails[6]))
            lblSunrise = QtWidgets.QLabel('Sunrise at:')
            lblInfoSunrise = QtWidgets.QLabel('{} am'.format(dailyDetails[11]))
            lblSunset = QtWidgets.QLabel('Sunset at:')
            lblInfoSunset = QtWidgets.QLabel('{} pm'.format(dailyDetails[12]))
            lblCloud = QtWidgets.QLabel('Cloud:')
            lblInfoCloud = QtWidgets.QLabel('{} %'.format(dailyDetails[13]))
            lblPressure = QtWidgets.QLabel('Pressure:')
            lblInfoPressure = QtWidgets.QLabel('{} hPa'.format(dailyDetails[14]))
            subDetails.addRow(lblSunrise, lblInfoSunrise)
            subDetails.addRow(lblSunset, lblInfoSunset)
            subDetails.addRow(lblHumi, lblInfoHumi)
            subDetails.addRow(lblWindSpeed, lblInfoWindSpd)
            subDetails.addRow(lblCloud, lblInfoCloud)
            subDetails.addRow(lblPressure, lblInfoPressure)
            subDe.setLayout(subDetails)
            # day part temp box details
            dayPartTempBox = QtWidgets.QScrollArea()
            dayInfo = QtWidgets.QGridLayout()
            dayPartTempBox.setLayout(dayInfo)
            lblMor = QtWidgets.QLabel('Morning')
            lblTempMor = QtWidgets.QLabel('{} C'.format(dailyDetails[7]))
            lblNight = QtWidgets.QLabel('Night')
            lblTempNight = QtWidgets.QLabel('{} C'.format(dailyDetails[10]))
            lblAfter = QtWidgets.QLabel('Afternoon')
            lblTempAfter = QtWidgets.QLabel('{} C'.format(dailyDetails[8]))
            lblEve = QtWidgets.QLabel('Evening')
            lblTempEve = QtWidgets.QLabel('{} C'.format(dailyDetails[9]))
            dayInfo.addWidget(lblMor, 1, 0)
            dayInfo.addWidget(lblTempMor, 2, 0)
            dayInfo.addWidget(lblAfter, 1, 1)
            dayInfo.addWidget(lblTempAfter, 2, 1)
            dayInfo.addWidget(lblEve, 1, 2)
            dayInfo.addWidget(lblTempEve, 2, 2)
            dayInfo.addWidget(lblNight, 1, 3)
            dayInfo.addWidget(lblTempNight, 2, 3)

            dayInfo.addWidget(subDe, 0, 0, 1, 4)

            MainDe.setLayout(MainDetails)
            FrameBox.addWidget(MainDe)
            FrameBox.addWidget(dayPartTempBox)
            Frame.setLayout(FrameBox)
            dailyForecast.addWidget(Frame)
            dailyForecast.addWidget(QtWidgets.QLabel('---------------------------------------------'))

    return dailyForecast


def mapView(lat, lon, zoom):
    mapWidget = MapWidget()
    mapLayout = QtWidgets.QVBoxLayout()
    mapLayout.addWidget(mapWidget)
    mapWidget.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
    map = L.map(mapWidget)
    map.setView([lat, lon], zoom)
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map)
    marker = L.marker([lat, lon])
    marker.bindPopup('You are here now!!')
    map.addLayer(marker)

    return mapLayout


def temperatureMapView():
    # Add layout
    layout = QtWidgets.QVBoxLayout()
    # Create QWebView
    view = QtWebKitWidgets.QWebView()

    # load .html file
    view.load(QtCore.QUrl.fromLocalFile(os.path.abspath('owmLeaflet/index.html')))

    layout.addWidget(view)

    return layout


class Client(QtWidgets.QFrame, client.Ui_mainLayout):
    def __init__(self, *args, **kwargs):
        global currLocation
        super(Client, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.hourlyForecast = QtWidgets.QHBoxLayout()
        self.dailyForecast = QtWidgets.QVBoxLayout()
        # get current location
        currLocation = getLocation()

        # get province list
        provList = allProvince()
        # if send a or c no need lat long
        self.socketWork('a', '', '')
        self.socketWork('b', currLocation.latitude, currLocation.longitude)

        # Gui
        # map stack
        self.mapStack = QtWidgets.QStackedLayout()
        # map
        self.mapLayout = QtWidgets.QWidget()
        self.mapLayout.setLayout(mapView(currLocation.latitude, currLocation.longitude, 11))
        self.mapTempLayout = QtWidgets.QWidget()
        self.mapTempLayout.setLayout(temperatureMapView())
        self.mapStack.addWidget(self.mapLayout)
        self.mapStack.addWidget(self.mapTempLayout)
        self.mapFrame.setLayout(self.mapStack)
        self.mapStack.setCurrentIndex(0)

        self.lblInfoAddress.setText(currLocation.city + ', ' + currLocation.country)
        self.lblInfoLat.setText(currLocation.latitude)
        self.lblInfoLong.setText(currLocation.longitude)
        self.lblIpAddress.setText("Your public IP address: " + currLocation.ip)
        self.lblUsername.setText("NagaKi: Vu Hoang")

        date = str(currLocation.time).split(' ')
        self.lblInfoDate.setText(str(date[0]))
        self.lblInfoTime.setText(str(date[1]))

        self.provList.addItems(provList)
        self.btnSearch.clicked.connect(self.searchOnClick)

        # hide some value
        self.lblCloud.setVisible(False)
        self.lblInfoCloud.setVisible(False)
        self.lblHumi.setVisible(False)
        self.lblInfoHumi.setVisible(False)
        self.lblSunrise.setVisible(False)
        self.lblInfoSunRise.setVisible(False)
        self.lblSunset.setVisible(False)
        self.lblInfoSunset.setVisible(False)
        self.lblVisi.setVisible(False)
        self.lblInfoVisi.setVisible(False)
        self.lblWind.setVisible(False)
        self.lblInfoWind.setVisible(False)
        self.lblPressure.setVisible(False)
        self.lblInfoPressure.setVisible(False)

        self.btnWeatherDetails.clicked.connect(self.clickVisible)
        self.btnHome.clicked.connect(lambda: self.socketWork('c', '', ''))

        # mapView
        self.btnNormalView.setEnabled(False)
        self.btnNormalView.clicked.connect(lambda: self.setMapView(1))
        self.btnTempMap.clicked.connect(lambda: self.setMapView(2))

    def setMapView(self, key):
        if key == 1:
            self.btnTempMap.setEnabled(True)
            self.btnNormalView.setEnabled(False)
            self.btnSearch.setEnabled(True)
            self.btnHome.setEnabled(True)
            self.mapStack.setCurrentIndex(0)
        else:
            self.btnTempMap.setEnabled(False)
            self.btnNormalView.setEnabled(True)
            self.btnSearch.setEnabled(False)
            self.btnHome.setEnabled(False)
            self.mapStack.setCurrentIndex(1)

    def socketWork(self, key, lat, long):
        global currLocation
        if key == 'a':
            # socket start - send "a" to say connect
            mess = "a_"
            fd.sendto(mess.encode(), (udp_ip, udp_port))

        # b also use for get data
        elif key == 'b':
            # then send "b" for current weather request
            mess = "b_" + lat.strip() + ',' + long.strip()
            fd.sendto(mess.encode(), (udp_ip, udp_port))
            r = fd.recvfrom(10000)
            text = r[0].decode().split('--split--')
            weather = text[0].split('_')
            self.lblInfoWeather.setText('{}'.format(weather[0]))
            self.lblInfoTemp.setText('{} C'.format(weather[1]))
            self.lblInfoHumi.setText('{} %'.format(weather[2]))
            self.lblInfoVisi.setText('{} m'.format(weather[3]))
            self.lblInfoWind.setText('{} m/s'.format(weather[4]))
            self.lblIcon.setPixmap(showIcon(weather[5], 2))
            self.lblInfoSunRise.setText('{} am'.format(weather[6]))
            self.lblInfoSunset.setText('{} pm'.format(weather[7]))
            self.lblInfoFeelTemp.setText('{} C'.format(weather[8]))
            self.lblInfoCloud.setText('{} %'.format(weather[9]))
            self.lblInfoPressure.setText('{} hPa'.format(weather[10]))

            # 8 days forecast
            daily = text[1].split('+')  # list of daily object
            self.dailyForecast = QtWidgets.QVBoxLayout()
            self.dailyForecast = dailyForecast(daily)
            self.scrollAreaForecast.setLayout(self.dailyForecast)

            # hourly forecast
            hourly = text[2].split('+')
            self.hourlyForecast = QtWidgets.QHBoxLayout()
            self.hourlyForecast = hourlyForecast(hourly)
            self.scrollAreaHourly.setLayout(self.hourlyForecast)

        # c for return back
        elif key == 'c':

            mess = "b_" + currLocation.latitude + ',' + currLocation.longitude
            fd.sendto(mess.encode(), (udp_ip, udp_port))
            r = fd.recvfrom(10000)
            text = r[0].decode().split('--split--')
            weather = text[0].split('_')
            self.lblInfoWeather.setText('{}'.format(weather[0]))
            self.lblInfoTemp.setText('{} C'.format(weather[1]))
            self.lblInfoHumi.setText('{} %'.format(weather[2]))
            self.lblInfoVisi.setText('{} m'.format(weather[3]))
            self.lblInfoWind.setText('{} m/s'.format(weather[4]))
            self.lblIcon.setPixmap(showIcon(weather[5], 2))
            self.lblInfoSunRise.setText('{} am'.format(weather[6]))
            self.lblInfoSunset.setText('{} pm'.format(weather[7]))
            self.lblInfoFeelTemp.setText('{} C'.format(weather[8]))
            self.lblInfoCloud.setText('{} %'.format(weather[9]))
            self.lblInfoPressure.setText('{} hPa'.format(weather[10]))

            self.lblInfoAddress.setText(currLocation.city + ', ' + currLocation.country)
            self.lblInfoLat.setText(currLocation.latitude)
            self.lblInfoLong.setText(currLocation.longitude)

            self.mapLayout = mapView(currLocation.latitude, currLocation.longitude, 11)

            # 8 days forecast
            #  remove first
            daily = text[1].split('+')  # list of daily object
            self.deleteLayout(self.dailyForecast)
            self.dailyForecast = QtWidgets.QVBoxLayout()
            self.dailyForecast = dailyForecast(daily)
            self.scrollAreaForecast.setLayout(self.dailyForecast)

            # hourly forecast
            hourly = text[2].split('+')
            self.deleteLayout(self.hourlyForecast)
            self.hourlyForecast = QtWidgets.QHBoxLayout()
            self.hourlyForecast = hourlyForecast(hourly)
            self.scrollAreaHourly.setLayout(self.hourlyForecast)

        # d for search place
        elif key == 'd':
            mess = "b_" + lat.strip() + ',' + long.strip()
            fd.sendto(mess.encode(), (udp_ip, udp_port))
            r = fd.recvfrom(10000)
            text = r[0].decode().split('--split--')
            weather = text[0].split('_')
            self.lblInfoWeather.setText('{}'.format(weather[0]))
            self.lblInfoTemp.setText('{} C'.format(weather[1]))
            self.lblInfoHumi.setText('{} %'.format(weather[2]))
            self.lblInfoVisi.setText('{} m'.format(weather[3]))
            self.lblInfoWind.setText('{} m/s'.format(weather[4]))
            self.lblIcon.setPixmap(showIcon(weather[5], 2))
            self.lblInfoSunRise.setText('{} am'.format(weather[6]))
            self.lblInfoSunset.setText('{} pm'.format(weather[7]))
            self.lblInfoFeelTemp.setText('{} C'.format(weather[8]))
            self.lblInfoCloud.setText('{} %'.format(weather[9]))
            self.lblInfoPressure.setText('{} hPa'.format(weather[10]))

            self.mapLayout = mapView(lat, long, 11)

            # 8 days forecast
            #  remove first
            daily = text[1].split('+')  # list of daily object
            self.deleteLayout(self.dailyForecast)
            self.dailyForecast = QtWidgets.QVBoxLayout()
            self.dailyForecast = dailyForecast(daily)
            self.scrollAreaForecast.setLayout(self.dailyForecast)

            # hourly forecast
            hourly = text[2].split('+')
            self.deleteLayout(self.hourlyForecast)
            self.hourlyForecast = QtWidgets.QHBoxLayout()
            self.hourlyForecast = hourlyForecast(hourly)
            self.scrollAreaHourly.setLayout(self.hourlyForecast)

    def deleteLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(layout)

    def searchOnClick(self):
        # print(self.provList.currentText())
        text = self.provList.currentText().split(',')
        self.lblInfoAddress.setText(text[0])
        self.lblInfoLat.setText(text[1])
        self.lblInfoLong.setText(text[2])
        self.mapLayout = mapView(text[1], text[2], 11)

        self.socketWork('d', text[1], text[2])

    def clickVisible(self):
        global click
        click += 1
        if click % 2 == 1:
            self.btnWeatherDetails.setText("Show Less")
            self.lblCloud.setVisible(True)
            self.lblInfoCloud.setVisible(True)
            self.lblHumi.setVisible(True)
            self.lblInfoHumi.setVisible(True)
            self.lblSunrise.setVisible(True)
            self.lblInfoSunRise.setVisible(True)
            self.lblSunset.setVisible(True)
            self.lblInfoSunset.setVisible(True)
            self.lblVisi.setVisible(True)
            self.lblInfoVisi.setVisible(True)
            self.lblWind.setVisible(True)
            self.lblInfoWind.setVisible(True)
            self.lblPressure.setVisible(True)
            self.lblInfoPressure.setVisible(True)
        else:
            self.btnWeatherDetails.setText("Details")
            self.lblCloud.setVisible(False)
            self.lblInfoCloud.setVisible(False)
            self.lblHumi.setVisible(False)
            self.lblInfoHumi.setVisible(False)
            self.lblSunrise.setVisible(False)
            self.lblInfoSunRise.setVisible(False)
            self.lblSunset.setVisible(False)
            self.lblInfoSunset.setVisible(False)
            self.lblVisi.setVisible(False)
            self.lblInfoVisi.setVisible(False)
            self.lblWind.setVisible(False)
            self.lblInfoWind.setVisible(False)
            self.lblPressure.setVisible(False)
            self.lblInfoPressure.setVisible(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = Client()
    widget.show()
    try:
        sys.exit(app.exec_())
    except (SystemError, SystemExit):
        fd.sendto('exit'.encode(), (udp_ip, udp_port))
        app.exit()
