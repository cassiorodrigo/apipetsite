import sqlite3

def mescla_db():
    conn = sqlite3.connect('dados/administracao.db')
    conlive = sqlite3.connect('dados/administracaolive.db')
    # conn.row_factory = sqlite3.Row
    # conlive.row_factory = sqlite3.Row
    c = conn.cursor()
    clive = conlive.cursor()

    q1 = """
    select username, email, clockin, clockout, delta from clock;
    """
    q2 = """
    insert or ignore into clock(username, email, clockin, clockout, delta) values(?,?,?,?,?)
    """
    res = clive.execute(q1).fetchall()
    c.executemany(q2, res)
    conn.commit()


if __name__ == "__main__":
    mescla_db()
