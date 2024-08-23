from dotenv import load_dotenv
load_dotenv()

import os
import telebot
import utils
import time
from langchain.embeddings import HuggingFaceEmbeddings

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

model_name = 'l3cube-pune/punjabi-sentence-similarity-sbert'
embeddings = HuggingFaceEmbeddings(model_name=model_name)

fruit_retriever = utils.get_retriever('../vectorstore/fruit/')
vegetable_retriever = utils.get_retriever('../vectorstore/vegetable/')
rabi_retriever = utils.get_retriever('../vectorstore/rabi/')
kharif_retriever = utils.get_retriever('../vectorstore/kharif/')

def get_answer(query):
    domain = utils.router(query)
    if "fruits" in domain:
        rag_chain = utils.create_rag_chain(fruit_retriever)
    elif "vegetable" in domain:
        rag_chain = utils.create_rag_chain(vegetable_retriever)
    elif "rabi" in domain:
        rag_chain = utils.create_rag_chain(rabi_retriever)
    else:
        rag_chain = utils.create_rag_chain(kharif_retriever)
    print(domain)
    time.sleep(1)
    print('-'*20)
    answer = rag_chain.invoke(query)
    print('query executed')
    return answer

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "ਪੁੱਛਗਿੱਛ ਸ਼ੁਰੂ ਕਰੋ")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    text = "ਜਵਾਬ ਤਿਆਰ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ, ਕਿਰਪਾ ਕਰਕੇ ਜਵਾਬ ਦੀ ਉਡੀਕ ਕਰੋ"
    sent_msg = bot.send_message(message.chat.id, text)
    bot.reply_to(message, get_answer(message.text))

print('#'*100)
print('started')
bot.infinity_polling()