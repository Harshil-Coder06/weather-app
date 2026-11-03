import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

#creates the weather app object using Qwidget
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        #creates all the different objects in the weather app
        self.cityLabel = QLabel("Enter City Name", self)
        self.cityInput = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.tempLabel = QLabel(self)
        self.emojiLabel = QLabel(self)
        self.descriptionLabel = QLabel(self)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 400, 500)
        pixmap = QPixmap("WeatherAppBackground.png")
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.lower()
        self.initUI()

   # function responsible for the UI of the weather app
    def initUI(self):
        self.setStyleSheet("""
              QLabel, QPushButton{
              font-family: Comic Sans MS;
              }
              QLabel#city_label{
              font-size: 40px;
              font-style: italic;
              background-color: transparent;
              }
              QLineEdit#city_input{
              font-size: 40px;
              border: 5px solid black;
              background-color: white;
              }
              QPushButton#get_weather{
              font-size: 30px;
              border : 5px solid black;
              background-color: white;
              }
              QLabel#temp_label{
              font-size: 40px;
              background-color: transparent;
              }
              QLabel#emoji_Label{
              font-size: 100px;
              font-family: Segoe UI emoji;
              background-color: transparent;
              }
              QLabel#description_Label{
              font-size: 50px;
              background-color: transparent;
              }
              QWidget{
              background-color: lightblue;
              }
             
              """)




        #setting the window title of our weather app
        self.setWindowTitle("Weather App")
        self.setFixedSize(500,600)

        # creating the layout of our weather app
        vbox = QVBoxLayout()
        vbox.addWidget(self.cityLabel)
        vbox.addWidget(self.cityInput)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.tempLabel)
        vbox.addWidget(self.emojiLabel)
        vbox.addWidget(self.descriptionLabel)
        self.setLayout(vbox)


        # aligning our widgets to the center
        self.cityLabel.setAlignment(Qt.AlignCenter)
        self.cityInput.setAlignment(Qt.AlignCenter)
        self.tempLabel.setAlignment(Qt.AlignCenter)
        self.emojiLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setAlignment(Qt.AlignCenter)

        # assigning each object with a specific "class".
        self.cityLabel.setObjectName("city_label")
        self.cityInput.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather")
        self.tempLabel.setObjectName("temp_label")
        self.descriptionLabel.setObjectName("description_Label")
        self.emojiLabel.setObjectName("emoji_Label")

        self.get_weather_button.clicked.connect(self.get_weather)

    def resizeEvent(self, event):
        self.label.resize(self.width(), self.height())
        super().resizeEvent(event)




   #function for getting the weather
    def get_weather(self):
        api_key = "bc582c742fd4e18b7cef2783426226d3"
        city = self.cityInput.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            responses = requests.get(url)
            responses.raise_for_status()
            data = responses.json()

            if data["cod"] == 200:
                self.display_weather(data)
        #handling error codes using match cases
        except requests.exceptions.HTTPError:
            match responses.status_code:
             case 400:
                 self.display_error("bad request\nPlease Try Again")
             case 401:
                    self.display_error("Unauthorized\nInvalid API Key")
             case 403:
                 self.display_error("Forbidden\nAccess Denied")
             case 404:
                 self.display_error("Not Found\nCity Not Found")
             case 500:
                 self.display_error("Internal Server\nPlease Try Again Later")
             case 502:
                 self.display_error("Bad Gateway\nInvalid Response From The Server")
             case 503:
                 self.display_error("Service Unavailable\nPlease Check your input")
             case 504:
                 self.display_error("Gateway Timeout\nNo Response From The Server")
             case _:
                 self.display_error("Unknown Error")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck Your Internet Connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request Timed Out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects\nCheck The URL")
        except requests.exceptions.RequestException as req_error:
           self.display_error(f"Request Error:\n{req_error}")

    #function for displaying error in app
    def display_error(self, message):
        self.tempLabel.setStyleSheet("font-size: 30px;")
        self.tempLabel.setText(message)
        self.emojiLabel.clear()
        self.descriptionLabel.clear()



    #function for displaying weather as well as calculating different temperatures in F and C
    def display_weather(self, data):
       self.tempLabel.setStyleSheet("font-size: 40px;")
       temperature_k = data["main"]["temp"]
       temperature_f = (temperature_k * 9 / 5) - 459.67
       temperature_c = temperature_k - 273.15
       temperature_c = round(temperature_c,1)
       temperature_f = round(temperature_f, 1)
       weather_id = data["weather"][0]["id"]
       weather_description = data["weather"][0]["description"]
       weather_code = data["weather"][0]["icon"]
       self.tempLabel.setText(f"{temperature_f}\u00B0F {temperature_c}\u00B0C")
       self.emojiLabel.setText(self.get_weather_emoji(weather_id, weather_code))
       self.descriptionLabel.setText(f"{weather_description}")

    #function for displaying the right emoji based on the weather of the city
    @staticmethod
    def get_weather_emoji(weather_id, weather_code):
        if 200 <= weather_id <= 232:
            return "\u26C8\uFE0F"
        elif 300 <= weather_id <= 321:
            return "🌧️"
        elif 500 <= weather_id <= 531:
            return "\U0001F237\uFE0F"
        elif 600 <= weather_id <= 622:
            return "\U0001F328\uFE0F"
        elif 701 <= weather_id <= 741:
            return "\U0001F32B\uFE0F"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "\U0001F32C\uFE0F"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            if weather_code == "01d":
               return "☀️"
            elif weather_code == "01n":
               return"🌙"

        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""
        
# creates the weather app object
def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

main()























