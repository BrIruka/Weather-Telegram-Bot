import requests
import json
from telebot import TeleBot, types

# Зареєструйте бота з @BotFather
bot = TeleBot('YOU_BOT_TOKEN')
openweathermap = "YOU_OPENWEATHER_TOKEN"

# Отримайте погоду з OpenWeatherMap
def get_weather(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + "&appid=" + openweathermap + "&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        raise Exception('Error getting weather data')

# Обробник повідомлень
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт! Я бот-погода. Я можу розповісти вам про погоду в будь-якому місті Світу. Просто введіть назву міста, щоб дізнатися про погоду.')

@bot.message_handler(content_types=['text'])
def get_weather_for_city(message):
    city = message.text
    weather_data = get_weather(city)
    if weather_data:
        # Отримати погоду
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        weather_description = weather_data['weather'][0]['description']
        # Створити повідомлення
        response_message = f'Погода в місті {city}: \n\n* Температура: {temperature}°C \n* Відчуття: {feels_like}°C \n* Вологість: {humidity}% \n* Атмосферний тиск: {pressure} hPa \n* Швидкість вітру: {wind_speed} м/с \n* Опис погоди: {weather_description}'
        bot.send_message(message.chat.id, response_message)
    else:
        bot.send_message(message.chat.id, 'Не можу знайти погоду для цього міста.')

# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
