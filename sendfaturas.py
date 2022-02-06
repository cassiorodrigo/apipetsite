"""
MOntar dois links:
um link para acessar a fatura no site
preciso:
    uma url basica
    um token
e

um link para envio do link anterior pelo whatsapp
preciso:
    telefone
    mensagem

"""
from databasehandler import FaturasDB
import urllib.parse

def montalinkwapp(telefone, texto):
    link = f"https://web.whatsapp.com/send?phone=55{telefone}&text={texto}"
    return link


def monta_link_fatura():
    base_url = f'https://petparkapi.pythonanywhere.com/faturas'
    with FaturasDB() as nfat:

        res = nfat.c.execute('select NOMECAO, TUTOR, TOKEN, _ID from faturas').fetchall()
        for dog in res:
            try:
                telefone = nfat.c.execute("select Telefone FROM telclients WHERE Dog=?", [dog[0]]).fetchone()[0]
                print(f"""
                ID              NOMECAO             TUTOR               TELEFONE
                ------------------------------------------------------------------------------------------------------
                {[dog[3]-1]} ├ {dog[0]}     ╞       {dog[1]}       ├        {telefone}
                
                """)
            except Exception as err:
                telefone = ''
            texto = F"""
                    Olá {dog[1]}!
                    
                    O Pet está testando um novo método de envio de faturas. 
                    
                    Buscando maior privacidade, nós estamos testando o método de acesso passivo às faturas. 
                    
                    Basta clicar no link para visualizar a fatuar de
                    
                    *{dog[0]}*
                    
                    Lá você verá a fatura desse mês que só é possível acessar com o token presente na URL. 
                    
                    Muito obrigado! 
                    
                    {base_url+'?token='+dog[2]}
                    
                    
                     
                    """
            texto = urllib.parse.quote(texto)
            linkw = montalinkwapp(telefone, texto)
            yield linkw, dog[0]


def codefyurl(texto):
    return urllib.parse.quote(texto)


if __name__ == "__main__":
    for link in monta_link_fatura():
        with open('dados/links.html', 'a') as file:
            file.write(f'<a href={link[0]}>{link[1]}</a><br>')
            file.write('\n')