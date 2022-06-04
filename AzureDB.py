import pypyodbc
import azurecred

class AzureDB:


    dsn = 'DRIVER=' + azurecred.AZDBDRIVER + ';SERVER=tcp:' + azurecred.AZDBSERVER + ';PORT=1433;DATABASE = '+azurecred.AZDBNAME+';UID =w12'+';PWD =Haslo123'

    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def finalize(self):
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()

    def __enter__(self):
        return self

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT name,text from data")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit(1)

