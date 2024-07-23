import os
from fastapi import FastAPI, Request
from utils import random_number, kospi, openai, langchain 
from dotenv import load_dotenv
import requests
import random

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = FastAPI()

@app.post('/') 

#도메인의 최상단을 뜻함 

#서버는 이 요청을 받아서(read_root 함수가 실행), 
#요청 내용을 출력하고 {'hello': 'world'}라는 응답을 보냄
#request: 사용자가 보낸 요청의 세부 정보를 담고 있는 객체.
#Request: FastAPI에서 제공하는 클래스 타입으로, request 변수가 이 타입을 따르게 됨


async def read_root(request: Request):

    body = await request.json() #사용자가 입력한 것을 body로 받아왔다 
    
 
    #우리는 두가지를 뽑음
    user_id = body['message']['from']['id']
    user_input = body['message']['text']
    print(user_id, user_input)
#사용자가 어떤 데이터를 입력했어 ? 
    if user_input[0] == '/':
        #우리가 만든 기능 추가
        if user_input == '/lotto':
            text = random_number()
        elif user_input == '/kospi':
            text = kospi()
        else:
            text = '지원하지 않습니다.'
    else:
        #open API 활용
        #text = openai(OPENAI_API_KEY, user_input)
        text= langchain(OPENAI_API_KEY, user_input)
    req_url = f'{URL}/sendMessage?chat_id={user_id}&text={text}'
    requests.get(req_url)

    return{'hello':'world'}
