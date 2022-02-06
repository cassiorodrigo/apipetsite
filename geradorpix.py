import binascii
import qrcode
from io import BytesIO


class Pagamento:

    def __init__(self, chavepix_recebedor, valor, nome_merchant, cidade, cep, mensagem):
        """
        :param chavepix_recebedor: qualquer chave. deve ser a chave do recebedor
        :param valor: no formato decimal ex.: 1.93
        :param nome_merchant: string com o nome do merchant
        :param nome_merchant: string com o nome do merchant
        As listas são uma sequencia do ID, TAMANHO ESPERADO e VALOR (PODENDO, O VALOR ser mais de um parametro - I'm
        looking at you, MERCHANT_CATEGORY_INFORMATION
        [ID, LEN, VALUE]

        """
        self.format_indicator = '01'
        self.merchant_account_info = 'BR.GOV.BCB.PIX'
        self.merchan_cathegory_code = '0000'
        self.currency = '986'
        self.country_code = 'BR'
        self.merchant = nome_merchant
        self.cidade = cidade
        self.CEP = cep
        self.chavepix = chavepix_recebedor
        self.mensagem = "05" + self.calculate_size(mensagem) + mensagem
        self.PAYLOAD_FORMAT_INDICATOR = ['00', self.calculate_size(self.format_indicator),
                                         self.format_indicator]

        self.MERCHANT_ACCOUNT_INFORMATION = ['26', str(int(self.calculate_size(self.merchant_account_info)) +\
                                                           int(self.calculate_size(self.chavepix))+8),
                                             '00', self.calculate_size(self.merchant_account_info),
                                             self.merchant_account_info,
                                             '01',
                                             self.calculate_size(self.chavepix),
                                             self.chavepix]
        self.MERCHANT_CATEGORY_CODE = ['52',
                                       self.calculate_size(self.merchan_cathegory_code),
                                       self.merchan_cathegory_code]

        self.TRANSACTION_CURRENCY = ['53',
                                     self.calculate_size(self.currency),
                                     self.currency]

        self.VALOR = ['54',
                      self.calculate_size(
                          self.padronizar_valor(valor)
                      ),
                      self.padronizar_valor(valor)]  # valor no formato decimal. Ex.: 1.93 com 4 bytes (tem que ter duas casas decimais separadas por ponto
        self.COUNTRY_CODE = ['58', self.calculate_size(self.country_code), self.country_code]
        self.CEP = ['61', self.calculate_size(self.CEP), self.CEP]
        self.MERCHANT_NAME = ['59', self.calculate_size(self.merchant), self.merchant]
        self.MERCHANT_CITY = ['60', self.calculate_size(self.cidade), self.cidade]
        self.ADITIONAL_DATA_FIELD_TEMPLATE = ['62',
                                              self.calculate_size(self.mensagem), self.mensagem]
                                              #'05'+ self.calculate_size(self.mensagem) + self.mensagem]
        self.bqrcode = None

    def generate_payload(self):
        list_of_attributes = \
            self.PAYLOAD_FORMAT_INDICATOR + \
            self.MERCHANT_ACCOUNT_INFORMATION + \
            self.MERCHANT_CATEGORY_CODE + \
            self.TRANSACTION_CURRENCY + \
            self.VALOR + \
            self.COUNTRY_CODE + \
            self.MERCHANT_NAME + \
            self.MERCHANT_CITY + \
            self.CEP + \
            self.ADITIONAL_DATA_FIELD_TEMPLATE

        return ''.join(list_of_attributes)+"6304"

    def calculate_size(self, dado_para_calcular: str):
        tamanho = str(len(dado_para_calcular)).rjust(2, '0')
        return tamanho

    def padronizar_valor(self, valor: float):
        return f"{float(valor):.2f}"

    def calcular_crc16(self):
        payload = self.generate_payload()
        # payload = """00020126580014BR.GOV.BCB.PIX013611c358f9-a42d-434f-b791-f176de78f21552040000530398654041.005802BR5925CASSIO RODRIGO D ANTONIO 6009SAO PAULO61080540900062240520zdnNJxFvCvHr7nw6trlz6304"""
        return f'{payload}{binascii.crc_hqx(bytes(payload, "UTF-8"), 0xffff):X}'


class QRPix(Pagamento):
    def __init__(self, chavepix_recebedor, valor, nome_merchant, cidade, cep, mensagem):
        super().__init__(chavepix_recebedor, valor, nome_merchant, cidade, cep, mensagem)

    def salvar_qrcode(self):
        stringdoqr = self.calcular_crc16()
        self.bqrcode = qrcode.make(stringdoqr)
        self.bqrcode.save("qrpix2.png")
        return stringdoqr

    def __bytes__(self):
        self.salvar_qrcode()
        buffer = BytesIO()
        self.bqrcode.save(buffer, format='png')
        reader = buffer.getvalue()
        return reader


if __name__ == "__main__":
    npix = QRPix('11c358f9-a42d-434f-b791-f176de78f215', 11.00, 'CASSIO RODRIGO D ANTONIO ', 'SAO PAULO', "05409000", 'Asercolocadodepois').salvar_qrcode()
    # npix = QRPix('11c358f9-a42d-434f-b791-f176de78f215', 1.0, 'CASSIO RODRIGO D ANTONIO ', 'SAO PAULO', "05409000", "zdnNJxFvCvHr7nw6trlz").salvar_qrcode()
    print(npix)
    # expected = "00020126580014BR.GOV.BCB.PIX013611c358f9-a42d-434f-b791-f176de78f21552040000530398654041.005802BR5925CASSIO RODRIGO D ANTONIO 6009SAO PAULO61080540900062240520zdnNJxFvCvHr7nw6trlz63043ABB"
    # assert npix == expected
    # print('Yes, equals')
    # print(bytes(npix))