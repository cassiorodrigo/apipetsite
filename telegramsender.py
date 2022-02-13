import requests
import os
import json
chavebanhos = os.getenv('apitelbanhos')
# chavehotel =



class MensagemBanhos:
    def __init__(self, nome, databanho, orientacoes):
        self.nome = nome
        self.databanho = databanho
        self.orientacoes = orientacoes

class SendMessage(MensagemBanhos):
    def __init__(self, *args, **kwargs):
        for e in kwargs:
            print(e)
        super().__init__(*args, **kwargs)
        self.endpointtelegram = f'https://api.telegram.org/{chavebanhos}/sendMessage?'
        # self.endpointtelegram = f'https://api.telegram.org/{chavebanhos}/getUpdates'

        self.formdata = {
            "chat_id": '-1001506442700',
            "text": '',
            "parse_mode": 'html'
        }

    def enviar_pedido(self):
        self.formdata['text'] = 'testes para o novo envio de peido de banhos. Favor ignorar.'
        # return self.formdata
        # return requests.get(self.endpointtelegram, json=self.options)
        return requests.post(self.endpointtelegram, self.formdata)


if __name__ == "__main__":
    newmessage = SendMessage(nome='Teste', databanho='Hoje', orientacoes='shampoo')
    newmessage.formdata['text'] = 'testes para o novo envio de peido de banhos. Favor ignorar.'
    res = newmessage.enviar_pedido()
    print(res.text)