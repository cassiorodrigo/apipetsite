import unittest
import requests
from unittest.mock import create_autospec
from unittest import mock
import main
from geradorpix import Pagamento
from Writer import Writer
import logging
result = '[{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"4",' \
              '"EMAIL":"beladsobrosa@hotmail.com","ENDERECO":"Rua Ayrton Senna número 303 apto 605 torre I. ' \
              'Itapoã Vila Velha ","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"25/12/2020","NOME_CAO":"Atena",' \
              '"RACA":"American Bully","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"998350601","TUTOR":"Isabela ' \
              'e Christian ","VET":"Dra Lays Zuqui","_ID":100},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"",' \
              '"DIAS_POR_SEMANA":"2","EMAIL":"liviavolpiss@gmail.com","ENDERECO":"Av Estudante José Júlio de ' \
              'Souza 1300","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"20/11/2014","NOME_CAO":"Balu","RACA":"",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"27981358000","TUTOR":"Lívia e Fábio Pezzin",' \
              '"VET":"Lifepet","_ID":8},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"Ele tem dermatite atópica. Usa ' \
              'omega 3 e faz alimentação natural. A medicação eu dou em casa pela manhã. ",' \
              '"DIAS_POR_SEMANA":"2","EMAIL":"ullychagasbernabe@gmail.com ","ENDERECO":"Aniceto Frizzera ' \
              'Filho, n 75, apto 1104 Ed Monet, Itaparica ","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"30/01/2021",' \
              '"NOME_CAO":"Boris ","RACA":"Buldogue Francês ","SAIDA_HOTEL":"","TEL_TUTOR":"",' \
              '"TEL_VET":"31997771971 (mamãe) ","TUTOR":"Ully Chagas Bernabé e Diego de Andrade Silva ",' \
              '"VET":"Consulveter- BH ","_ID":130},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"Cuidado ao subir ou ' \
              'descer de lugares altos. ","DIAS_POR_SEMANA":"3","EMAIL":"Camila.anholetti@gmail.com",' \
              '"ENDERECO":"Av. João Mendes, 1528, Praia de Itaparica\nVila Velha, ES\nAP 1105",' \
              '"ENTRADA_HOTEL":"","NASCIMENTO_CAO":"12/10/2010","NOME_CAO":"Boris - Labrador",' \
              '"RACA":"Labrador","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"3058-1114","TUTOR":"Camila ' \
              'Meirelles Anholetti","VET":"SOS Hospital","_ID":155},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"caso de Convulsões ","DIAS_POR_SEMANA":"1",' \
              '"EMAIL":"camillapisa@hotmail.com","ENDERECO":"Rua Itaoca, 20, ed Verona ap 203, ' \
              'praia de Itaparica, Vila Velha ","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"05/07/2013",' \
              '"NOME_CAO":"Braian Magnago ","RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"27 ' \
              '99772-3438","TUTOR":"Camilla pisa magnago","VET":"Dar Franciely Sezini ","_ID":36},' \
              '{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"Não come ração pura","DIAS_POR_SEMANA":"3",' \
              '"EMAIL":"carolinecucco@gmail.com","ENDERECO":"Av. Hugo Musso, n. 2370, apt. 1703, ' \
              'Ed. Mediterranean tower, Itapua","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"01/01/2018",' \
              '"NOME_CAO":"Bruce Wayne","RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"99625-5529",' \
              '"TUTOR":"Caroline Cucco","VET":"Plano de saúde Lifepet","_ID":19},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"3","EMAIL":"laisa.admufes@gmail.com","ENDERECO":"Av ' \
              'João Mendes, 1528","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"14/03/2018","NOME_CAO":"Céu",' \
              '"RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"30581114","TUTOR":"Laisa e Pamela",' \
              '"VET":"SOS","_ID":12},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"2",' \
              '"EMAIL":"Kamillasilvac@hotmail.com ","ENDERECO":"Av estudante José Júlio de Souza n 2800 Ed ' \
              'Armando negreiros apart 1402 Itaparica Vila Velha ","ENTRADA_HOTEL":"08/10/2021",' \
              '"NASCIMENTO_CAO":"06/08/2020","NOME_CAO":"Dom Perignon ","RACA":"Border colie ",' \
              '"SAIDA_HOTEL":"13/10/2021","TEL_TUTOR":"","TEL_VET":"027998350601","TUTOR":"Kamilla Carneiro ' \
              'benjamim ","VET":"De lays ","_ID":167},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"No momento sem ' \
              'cuidados especiais","DIAS_POR_SEMANA":"2","EMAIL":"mil1309@hotmail.com","ENDERECO":"Av Estud ' \
              'José Júlio de Souza 1590 apto 1204","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"14/04/2006",' \
              '"NOME_CAO":"Dupla BB Beethoven Benjamin","RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"",' \
              '"TEL_VET":"996082686","TUTOR":"Milleni","VET":"Fernanda","_ID":15},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"Alergia a cheiros fortes","DIAS_POR_SEMANA":"3",' \
              '"EMAIL":"mariza.duarte@hotmail.com","ENDERECO":"Av Est José Júlio de Souza, 1600, ' \
              'Praia de Itaparica","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"18/12/2017","NOME_CAO":"Gaya",' \
              '"RACA":"American Bully ","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"(27) 99835-0601",' \
              '"TUTOR":"Mariza e Isaías ","VET":"Dra Lays Neves Zuqui ","_ID":117},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"2","EMAIL":"jessica_nt1@hotmail.com",' \
              '"ENDERECO":"Rua Rio Grande Do Norte 55, apto 304, Praia da Costa Vila Velha ",' \
              '"ENTRADA_HOTEL":"","NASCIMENTO_CAO":"23/10/2017","NOME_CAO":"Ipa","RACA":"Buldogue francês ",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"27999666646","TEL_VET":"997570136","TUTOR":"Jessica Nunes ' \
              'Teixeira de Souza","VET":"Lilian Deise/ Clínica São Lazaro","_ID":174},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"Sempre verificar se ele esta bebendo água ele ja teve pedra nos rins",' \
              '"DIAS_POR_SEMANA":"2","EMAIL":"Suelen Cavalieri Bittencourt e carlos Roberto menegatti",' \
              '"ENDERECO":"Rua itabaiana, 133, cep 29102290, apt 1006, praia de itaparica",' \
              '"ENTRADA_HOTEL":"","NASCIMENTO_CAO":"10-12-2013","NOME_CAO":"Johnnie","RACA":"",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"+55 27 99933-1819","TUTOR":"Suelen cavalieri ' \
              'bittencourt","VET":"Poliana","_ID":14},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"",' \
              '"DIAS_POR_SEMANA":"2","EMAIL":"rcb.edu@gmail.com","ENDERECO":"Avenida dos Estados, ' \
              '114 apt 202","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"04/03/2020","NOME_CAO":"Laika","RACA":"Pug",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"30252191","TUTOR":"Eduardo e Carol ","VET":"Pet ' \
              'life","_ID":121},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"2",' \
              '"EMAIL":"naataalia.ribeiro@gmail.com","ENDERECO":"Rua José Félix Cheim, 101, Ed Plátano apto ' \
              '504, Praia de Itaparica - Vila Velha","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"25/03/2021",' \
              '"NOME_CAO":"Lola","RACA":"Bulldog Francês","SAIDA_HOTEL":"","TEL_TUTOR":"",' \
              '"TEL_VET":"996481387","TUTOR":"Natália Ribeiro Campos","VET":"Dra Aparecida Dauzacker",' \
              '"_ID":133},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"1",' \
              '"EMAIL":"karla_baptistaaguiar@hotmail.com","ENDERECO":"Av. Hugo musso 929 cedro de Líbano 603 ' \
              'praia da Costa ","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"27/01/2021","NOME_CAO":"Luke",' \
              '"RACA":"Spitz alemão ","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"995700300","TUTOR":"Karla ' \
              'Baptista ","VET":"Leisiani Uliana Pin / SOS hospital veterinário ","_ID":124},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"3","EMAIL":"hemylerocha@hotmail.com",' \
              '"ENDERECO":"Rua Humberto Serrano, 555, apto. 401 Praia da Costa","ENTRADA_HOTEL":"20/04/2021",' \
              '"NASCIMENTO_CAO":"27/11/2019","NOME_CAO":"Lulu","RACA":"","SAIDA_HOTEL":"26/04/2021",' \
              '"TEL_TUTOR":"","TEL_VET":"27999099630","TUTOR":"Hemyle e Hugo","VET":"Happy Dog / Dr. Renato ' \
              'Carvalho","_ID":22},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"3",' \
              '"EMAIL":"Nicole.cguirlin@gmail.com","ENDERECO":"Avenida Hugo Musso, 2370. apt 1003. Itapoã, ' \
              'Vila Velha.","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"07/07/2020","NOME_CAO":"Meg Beagle",' \
              '"RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"27 99952-2113","TUTOR":"Nicole Cerutti ' \
              'Guirlinzone","VET":"Caroline Ribeiro / Pet Kingdom","_ID":4},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"2","EMAIL":"ana_claralima@hotmail.com",' \
              '"ENDERECO":"Rua José Celso Cláudio, 235, Ed Praia das Conchas, apto 606, Praia das Gaivotas, ' \
              'Vila Velha ES","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"Meg 20/12/2014 e Tobi 31/07/2018",' \
              '"NOME_CAO":"Meg e Tobi","RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"99297-4027",' \
              '"TUTOR":"Ana Clara de Oliveira Lima","VET":"Pet Point","_ID":6},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"Alergia a corante","DIAS_POR_SEMANA":"3",' \
              '"EMAIL":"paulinhacavicchia@gmail.com/benecavicchia@gmail.com","ENDERECO":"Rua Santa Catarina ' \
              '70/102","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"27/09/2013","NOME_CAO":"Nina","RACA":"",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"Nao lembro","TUTOR":"Paula/Bene","VET":"Raquel ' \
              'Grand pet","_ID":17},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"2",' \
              '"EMAIL":"pricilabrito@hotmail.com","ENDERECO":"Av estudante José Júlio de Souza,  2800 apt 302 ' \
              '","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"Resgata aproximadamente 5meses","NOME_CAO":"Nina (' \
              'Caramelo)","RACA":"Goldem filhote","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"30581114",' \
              '"TUTOR":"Pricila Silva brito ","VET":"Sos hospital veterinario  praia da costa ","_ID":116},' \
              '{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"Não","DIAS_POR_SEMANA":"2",' \
              '"EMAIL":"kregaurich@hotmail.com","ENDERECO":"Rua Coronel Joaquim de Freitas, 247 - Jaburuna - ' \
              'Vila Velha","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"10/04/2020","NOME_CAO":"Olívia","RACA":"",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"3389-2319. ","TUTOR":"KATIA REGINA AURICH",' \
              '"VET":"Clinicão - Laura","_ID":35},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"",' \
              '"DIAS_POR_SEMANA":"2","EMAIL":"sarapinheiro@outlook.com","ENDERECO":"Rua Itapemirim, ' \
              '155. Apt 1805","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"23/02/2019","NOME_CAO":"Ozzy","RACA":"",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"(027) 99962-5060","TUTOR":"Sara Pinheiro",' \
              '"VET":"Guilherme Bretas","_ID":16},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"Pipoca e uma cachorro ' \
              'atópica, do nada pode ter alergias… sempre tire a coleira dela, pra evitar alergias… ☺️",' \
              '"DIAS_POR_SEMANA":"2","EMAIL":"anacfavato@gmail.com","ENDERECO":"AVENIDA PRESIDENTE FLORENTINO ' \
              'ÁVIDOS, n 300- apartamento 1901 A- Centro - Vitória/ ÉS 29.018-190","ENTRADA_HOTEL":"",' \
              '"NASCIMENTO_CAO":"03/04/2020","NOME_CAO":"PIPOCA FAVATO BARCELLOS","RACA":"Bulldog Francês ",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"27- 99262-3484","TUTOR":"ANA CRISTINA FAVATO E ' \
              'GUSTAVO BARCELLOS","VET":"Laysa Raimundo Valadares","_ID":122},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"2","EMAIL":"carolmarianelli@icloud.com",' \
              '"ENDERECO":"Rua Antônio Régis dos Santos n 06 apto 1304","ENTRADA_HOTEL":"",' \
              '"NASCIMENTO_CAO":"03/2013","NOME_CAO":"Petit","RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"",' \
              '"TEL_VET":"33494619","TUTOR":"Carolina Marianelli","VET":"Dr Paulo / Pet Point","_ID":18},' \
              '{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"","DIAS_POR_SEMANA":"3",' \
              '"EMAIL":"ingridtassar@gmail.com","ENDERECO":"Rua Itaquari, 295, apto 1401, Itapuã, ' \
              'Vila Velha/ES. CEP: 29101-850.","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"21/04/2017",' \
              '"NOME_CAO":"Raul","RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"27 981239217",' \
              '"TUTOR":"Ingrid Tassar","VET":"Kamila Souza/FFPET CENTER","_ID":11},{"ATIVO":"TRUE",' \
              '"CUIDADOS_ESPECIAIS":"Cuidados com não causar nenhum tipo de aperto na garganta do Ruff (' \
              'estenose de traqueia)","DIAS_POR_SEMANA":"3","EMAIL":"tamaraabraham34@gmail.com",' \
              '"ENDERECO":"Rua Deolindo Perim, num 373 apt 202","ENTRADA_HOTEL":"",' \
              '"NASCIMENTO_CAO":"10/01/2021","NOME_CAO":"Ruff","RACA":"Golden","SAIDA_HOTEL":"",' \
              '"TEL_TUTOR":"","TEL_VET":"27 998719130","TUTOR":"Tamara B Abraham","VET":"Pet imperio",' \
              '"_ID":144},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"Cuidado com os olhos pois é muito alérgico. ' \
              'Não passar perfume.\nE não deixar comer farinha branca.","DIAS_POR_SEMANA":"3",' \
              '"EMAIL":"bajopimentel@hotmail.com","ENDERECO":"Rua São Paulo número 1270 apt 201 Praia da ' \
              'Costa","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"14/04/2015","NOME_CAO":"Tiberio","RACA":"",' \
              '"SAIDA_HOTEL":"","TEL_TUTOR":"","TEL_VET":"27 99999-3454","TUTOR":"Camila e Thiago",' \
              '"VET":"Dr Vinicius Ribeiro","_ID":24},{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":"Apenas com a ' \
              'comida funcional dele que vai separadamente, esquentar e colocar um pouco de ração no meio.",' \
              '"DIAS_POR_SEMANA":"5","EMAIL":"taffoaraujo@hotmail.com","ENDERECO":"Av. José Martins Rato 156 ' \
              'apt 303 Jardim Camburi","ENTRADA_HOTEL":"","NASCIMENTO_CAO":"17/08/2019 data do resgate - já ' \
              'deveria ter uns 6 meses","NOME_CAO":"Tyron","RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"",' \
              '"TEL_VET":"3319-1622","TUTOR":"Flávio Márcio Araújo","VET":"Raiza Fernanda","_ID":13},' \
              '{"ATIVO":"TRUE","CUIDADOS_ESPECIAIS":" Evitar Ovo, e frango nos petiscos , pois o veterinário ' \
              'está avaliando uma possível alergia.  Não deixá-la molhada  muito tempo, dar bastante água , ' \
              'pois ela sente muita sede. ","DIAS_POR_SEMANA":"4","EMAIL":"and_diass@hotmail.com",' \
              '"ENDERECO":"Rua Fortaleza, 1520, apto 1504 - Itapoa - Vila Velha -ES","ENTRADA_HOTEL":"",' \
              '"NASCIMENTO_CAO":"20/06/2020","NOME_CAO":"Zoe","RACA":"","SAIDA_HOTEL":"","TEL_TUTOR":"",' \
              '"TEL_VET":" (27 99) 9622-5060","TUTOR":"José Vicente Lorenzon  e Andréa Bastos Dias Lorenzon",' \
              '"VET":"Guilherme Brêtas ","_ID":25}] '


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.writer = Writer()
        self.creche = 'http://127.0.0.1:5000/creche'
        self.login = 'http://127.0.0.1:5000/login'
        self.cadastrar_funcionario = 'http://127.0.0.1:5000/cadastrar-funcionario'
        self.daycare = 'http://127.0.0.1:5000/daycare'
        self.banhos = 'http://127.0.0.1:5000/banhos'
        self.hotel = 'http://127.0.0.1:5000/hotel'
        self.testes = 'http://127.0.0.1:5000/testes'
        self.pg = pg = Pagamento(chavepix_recebedor="123e4567-e12b-12d1-a456-426655440000",
                                 valor=0.00,
                                 nome_merchant="Fulano de Tal",
                                 cidade="BRASILIA",
                                 cep='',
                                 mensagem="***")
        self.realpix = Pagamento(
            chavepix_recebedor="11c358f9-a42d-434f-b791-f176de78f215",
            valor=1.00,
            nome_merchant="CASSIO RODRIGO D ANTONIO ",
            cidade="SAO PAULO",
            cep="05409000",
            mensagem='0520zdnNJxFvCvHr7nw6trlz'
            # mensagem='0520zdnNJxFvCvHr7nw6trlz'
        )

    def test_pix_code_gen(self):
        expected_pl = "00020126580014BR.GOV.BCB.PIX013611c358f9-a42d-434f-b791-f176de78f21552040000530398654041.005802BR5925CASSIO RODRIGO D ANTONIO 6009SAO PAULO61080540900062240520zdnNJxFvCvHr7nw6trlz63043ABB"
        res = self.realpix.calcular_crc16()
        print(len(res))
        print(f"{expected_pl:<200}")
        print(f"{res:<200}")
        self.assertEqual(expected_pl, res)

    def test_padronizar_valor(self):
        valores = [10, 10.0, '10', '10.0',
                   '1', '1.0',1, 1.0,
                   0, 0.0, '0', '0.0' ,
                   200, 200.0,'200', '0200',
                   10000, 10000.0, '010000', '10000.0']

        # valor = self.pg.padronizar_valor(10.0)
        # self.assertEqual("10.00", valor)
        indice = 0
        for _ in valores:
            with self.subTest(indice=indice):
                if indice < 4:
                    self.assertEqual("10.00", self.pg.padronizar_valor(valores[indice]))

                elif 4 <= indice < 8:
                    self.assertEqual("1.00", self.pg.padronizar_valor(valores[indice]))

                elif 8 <= indice < 12:
                    self.assertEqual("0.00", self.pg.padronizar_valor(valores[indice]))

                elif 12 <= indice < 16:
                    self.assertEqual("200.00", self.pg.padronizar_valor(valores[indice]))

                elif 16 <= indice < 20:
                    self.assertEqual("10000.00", self.pg.padronizar_valor(valores[indice]))
            indice += 1

    def test_writer(self):
        fim = self.writer.write('Testes', logging.INFO)
        self.assertEqual(fim, True)

    def test_show_separated_pix(self):
        pixstring = self.pg.calcular_crc16()
        index = 1
        for e in pixstring:
            print(e, end='')
            # if index == 4:
            #     print('\n', end='')
            index += 1

if __name__ == '__main__':
    unittest.main()



