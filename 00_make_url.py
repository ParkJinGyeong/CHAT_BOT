import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

URL = f'https://api.telegram.org/bot{TOKEN}'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

method = 'getUpdates'

res = requests.get(f'{URL}/{method}')

res_dict = res.json()

user_input = res_dict['result'][-1]['message']['text']
user_id = res_dict['result'][-1]['message']['from']['id']


print(user_id, user_input)

#웹에서 값을 가지고 온 상태 
#사용자에게 메세지를 보내는 상태
SEND_MSG_URL = f'{URL}/sendMessage?chat_id={user_id}&text={user_input}'
for i in range(5):
    requests.get(SEND_MSG_URL)

#사용자가 한말을 메아리로 따라함 
