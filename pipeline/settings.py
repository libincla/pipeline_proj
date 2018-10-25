'''
settings for pipeline
'''

USERNAME = 'root'
PASSWORD = 'htjy123'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'pipeline'

DATABASE_DEBUG = True

URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

