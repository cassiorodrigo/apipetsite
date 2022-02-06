import logging


class Writer:

    def __init__(self):
        logging.basicConfig(filename='logs/logs.log', level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(name)s \n%(message)s",
                            datefmt="%d/%m/%Y [%H:%M:%S]")

    def write(self, message, level):
        try:
            logging.log(level=level, msg=message)
            return True
        except Exception as err:
            print(err)
            return False


if __name__ == "__main__":
    nwriter = Writer()
    nwriter.write('oi', logging.INFO)
