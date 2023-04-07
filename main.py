import telebot
import psycopg2
from telebot.types import*
from telebot.apihelper import ApiTelegramException

bot = telebot.TeleBot("5628656737:AAGqz06KVUBcdqNbCxQg3-t5nVMg7xy2_so")

CHAT_ID = '@pristbank' #replace your channel id
DATABASE_URL = "postgresql://postgres:0XSbBvU64j4G7EWusxWD@containers-us-west-163.railway.app:7257/railway"
def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    return conn
def insert_user_data(user_id, join_date, user_info):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO users (user_id, join_date, user_info) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, join_date, user_info))
    conn.commit()
    cursor.close()
    conn.close()


def is_subscribed(chat_id, user_id):
    try:
        response = bot.get_chat_member(chat_id, user_id)
        if response.status == 'left':
            return False
        else:
            return True

    except ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: chat not found':
            return False



@bot.message_handler(commands=['start'])
def send_welcome(message):

    if not is_subscribed(CHAT_ID,message.chat.id):
        # user is not subscribed. send message to the user
        bot.send_message(message.chat.id, 'Please subscribe to the channel')
    else:
        
        user_id = message.from_user.id
        join_date = message.date
        user_info = f"{message.from_user.first_name} {message.from_user.last_name}"
        if user_id not in insert_user_data(user_id):
            insert_user_data(user_id, join_date, user_info)
            bot.send_message(message.chat.id, 'User information has been stored in the database.')
        else:
            bot.send_message(message.chat.id, 'hi prist')

@bot.message_handler(commands=['help'])
def send_welcome(message):

    if not is_subscribed(CHAT_ID,message.chat.id):
        # user is not subscribed. send message to the user
        bot.send_message(message.chat.id, 'Please subscribe to the channel')
    else:
        bot.send_message(message.chat.id, 'help msg')

bot.polling()
