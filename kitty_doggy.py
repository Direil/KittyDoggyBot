import random
import telebot
import requests

token = "Token"
bot = telebot.TeleBot(token)


# Generate a random index to choose a random pic
cat_index = random.randint(0, 150)
dog_index = random.randint(0, 435)
cat_fact_limit = 250

# Get a list of cat facts via catfact api
cat_facts = requests.get(f'https://catfact.ninja/facts?limit={cat_fact_limit}').json()
fact_list = cat_facts['data']
cat_list = [fact['fact'] for fact in fact_list]


# Creating a keyboard
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Send me a cat', 'Send me a dog')
    bot.send_message(message.chat.id, '🐈 / 🐕', reply_markup=keyboard)


# Accessing a cat img api
@bot.message_handler(commands=['cat'])
def get_cat_img(message):
    contents = requests.get('https://aws.random.cat/meow').json()
    url = contents['file']
    bot.send_photo(message.chat.id, url, caption=cat_list[cat_index])


# Accessing a dog img & fact api
@bot.message_handler(commands=['dog'])
def get_dog_img(message):
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    dog_facts = requests.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?index=" + str(dog_index)).json()
    bot.send_photo(message.chat.id, url, caption=dog_facts[0]['fact'])


# A message handler that activates get_dog_img and get_cat_img
@bot.message_handler(content_types=['text'])
def send_kittydoggy(message):
    if message.text == 'Send me a cat':
        get_cat_img(message)
    elif message.text == 'Send me a dog':
        get_dog_img(message)

if __name__ == '__main__':
    bot.infinity_polling()
