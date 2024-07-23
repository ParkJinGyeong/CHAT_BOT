#만들고 싶은 기능을 하나씩 추가 
import random
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough 
from langchain


def random_number():
    return str(sorted(random.sample(range(1, 46), 6)))

def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/' #가져오고 싶은 주소 값 

    res = requests.get(KOSPI_URL) #요청에 의해 가져 옴 
    res_text = res.text

    selector = '#KOSPI_now'

    soup = BeautifulSoup(res_text, 'html.parser') #soup 형태로 변형 시킴 
    kospi = soup.select_one(selector).text

    return kospi

def openai(api_key, user_input):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {'role': 'system', 'content' : "요리 이름에 맞는 레시피를 작성해줘, 다만 출력이름에 #은 넣지마"},
            {'role': 'user', 'content': user_input},
        ]
        )
    return completion.choices[0].message.content

#1.load document 

def langchain(api_key, user_input):
    loader = WebBaseLoader(
        web_path = ('
                 'https://www.aitimes.kr/news/articleView.html?idxno=31272', 
                 'https://developer.apple.com/kr/wwdc24/'
                 )
    )
docs = loader.load()

#2.split 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

#3. store


#4. retrieve - 유사도가 높은 것들을 기반으로 
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")

rag_chain = (
    {"context": retriever | retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

return rag_chain.invoke(user_input)