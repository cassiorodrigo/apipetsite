import datetime
import unittest
from models.UserModel import tabela
from resources import engine


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.user = tabela
    def test_something(self):
        ins = tabela.insert().values(
            username="cassiorodrigo",
            name='Cassio Rodrigo',
            email='cassiorodrigo@gmail.com',
            role='superadmin',
            public_id=1,
            dog="Dumbledore",
            date=datetime.date.today(),
            dateandtime=datetime.datetime.now()
        )
        conn = engine.connect()
        conn.execute(ins)



if __name__ == '__main__':
    unittest.main()
