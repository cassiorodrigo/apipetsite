import requests
import os
import json
chavebanhos = os.getenv('apitelbanhos')
chaveavisa = os.getenv('apiforms')
# chavehotel =


class SendMessage:
    def __init__(self, *args, **kwargs):
        self.texto = str()
        # tipodemenssagem = kwargs.setdefault('chave', chaveavisa)
        tipodemenssagem = kwargs.get("tipo")
        if 'banhos' in tipodemenssagem:
            telegramchave = chavebanhos
            self.chatid = "-1001506442700"
        elif "hotel" or "creche" in tipodemenssagem:
            telegramchave = chaveavisa
            self.chatid = '-1001549922949'

        self.endpointtelegram = f'https://api.telegram.org/{telegramchave}/sendMessage?'

        self.formdata = {
            "chat_id": self.chatid,
            "text": self.texto,
            "parse_mode": 'html'
        }

    def enviar_mensagem(self):
        return requests.post(self.endpointtelegram, self.formdata)


# class MensagemBanhos(SendMessage):
#     def __init__(self, *args, **kwargs):
#         nome, databanho, orientacoes = kwargs['nome'], kwargs['databanho'], kwargs['orientacoes']
#         super(MensagemBanhos, self).__init__(*args, **kwargs)
#         self.nome = nome
#         self.databanho = databanho
#         self.orientacoes = orientacoes


class FormSent(SendMessage):
    def __init__(self, *args, **kwargs):
        super(FormSent, self).__init__(*args, **kwargs)
        """
        kwargs: need to pass the 
        username,
        type of form to be sent(creche or hotel), 
        list of dogs in
        type (either banhos or presencas)
        """
        self.usuario, self.tipo, self.dogsin = kwargs.get('username'), kwargs.get('tipo'), kwargs.get('dogsin')
        self.listadecaes = "\n".join(kwargs.get('dogsin'))
        self.texto = self.monta_mensagem()

    def monta_mensagem(self):
        formulario = f"""
Formulário de Presenças de <strong> {self.tipo} </strong>:
Número de cães presentes: {len(self.listadecaes)}
Cães Presentes:

{self.listadecaes} 

Preenchido por <strong> {self.usuario} </strong>
        """
        # self.texto = formulario
        self.formdata['text'] = formulario
        return formulario


class PedidoBanhos(SendMessage):
    def __init__(self, *args, **kwargs):
        super(PedidoBanhos, self).__init__(*args, **kwargs)
        """
        :param args:
        :param kwargs:
        super class needs at least tipodemensagem to be initialized.
        also, text has to be defined befor sending the text.
        """
        self.tipo = kwargs.get('tipo')
        self.dog = kwargs.get('dog')
        self.buscacao = kwargs.get('buscacao')
        self.databanho = kwargs.get('databanho')
        self.perfumes = kwargs.get('perfumes')
        self.instrucoes = kwargs.get('instrucoes')
        self.tutor = kwargs.get('tutor')
        self.texto = f"""
        Banho pedido por {self.tutor}
        
        Para o cao: {self.dog}
        
        Data Banho: {self.databanho}
        
        Hora para Buscar: {self.buscacao}
        
        Perfumes: {self.perfumes}
        
        Instruções: {self.instrucoes}
        
        """

        self.formdata['text'] = self.texto



# if __name__ == "__main__":
#     newmessage = SendMessage(nome='Teste', databanho='Hoje', orientacoes='shampoo')
#     newmessage.formdata['text'] = 'testes para o novo envio de peido de banhos. Favor ignorar.'
#     res = newmessage.enviar_pedido()
#     print(res.text)