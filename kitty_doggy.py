import random
import telebot
import requests

token = "token"
bot = telebot.TeleBot(token)

cat_index = random.randint(0, 150)
factIndex = random.randint(0, 435)

cat_facts = requests.get('https://catfact.ninja/facts?limit=250').json()
fact_list = cat_facts['data']
cat_list = [fact['fact'] for fact in fact_list]


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Send me a cat', 'Send me a dog')
    bot.send_message(message.chat.id, '🐈 / 🐕', reply_markup=keyboard)


@bot.message_handler(commands=['cat'])
def get_cat_img(message):
    contents = requests.get('https://aws.random.cat/meow').json()
    url = contents['file']
    bot.send_photo(message.chat.id, url, caption=cat_list[cat_index])


@bot.message_handler(commands=['dog'])
def get_dog_img(message):
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    dog_facts = requests.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?index=" + str(factIndex)).json()
    bot.send_photo(message.chat.id, url, caption=dog_facts[0]['fact'])


@bot.message_handler(content_types=['text'])
def send_kittydoggy(message):
    if message.text == 'Send me a cat':
        get_cat_img(message)
    elif message.text == 'Send me a dog':
        get_dog_img(message)


if __name__ == '__main__':
    bot.infinity_polling()
