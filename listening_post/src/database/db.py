from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from mysql.connector import errorcode
from config import username, password

db = SQLAlchemy()
config = {
    'user': username, 
    'password': password,
    'host': 'localhost',
}

def initialise(app):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS listener")
        print("Database created successfully.")
        
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
        exit
        
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@localhost/listener'
    db.init_app(app)
    
    with app.app_context():
        db.create_all()