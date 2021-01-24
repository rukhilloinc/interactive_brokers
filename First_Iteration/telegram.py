import requests

bot_chatID = '-423666062'
bot_token = '1584877881:AAFPCiemu5BZcn-UJVH-P3MKdo2j2YgBOBM'


def send_telegram(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


