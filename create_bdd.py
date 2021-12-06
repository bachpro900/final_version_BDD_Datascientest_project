import sqlite3, sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, create_engine, text, inspect
from IPython.display import Markdown, display
import csv

from sqlalchemy.sql.sqltypes import Float


def show_table(table):
    for row in table:
        print(row)


# creer et connecter a la bdd
print('creer et connecter a la bdd')
engine = create_engine('sqlite:///bdd_datascientest_projet3.db', echo=True)
meta = MetaData()


# ####################################################################
# ###################### creation des tables #########################

# créer la table de user (lecteur)
print('créer la table user (lecteur)')
user = Table (
    'user', meta,
    Column('user_id', Integer, primary_key=True),
    Column('location', String),
    Column('age', Integer)
)


# créer la table de book
print('créer la table book')
book = Table (
    'book', meta,
    Column('book_id', String, primary_key=True),
    Column('book_title', String),
    Column('book_author', String),
    Column('year_of_publication', Integer),
    Column('publisher', String),
    Column('image_url_s', String),
    Column('image_url_m', String),
    Column('image_url_l', String)
)


# créer la table de rating
print('créer la table rating')
rating = Table (
    'rating', meta,
    Column('user_id', Integer, ForeignKey("user.user_id"), primary_key=True),
    Column('book_id', String, ForeignKey("book.book_id")),
    Column('rate', Float)
)


# afficher les tables de la bdd
print('afficher les tables de la bdd')
inspector = inspect(engine)
print(inspector.get_table_names())


# creation des 3 tables
# sql = text('DROP TABLE IF EXISTS rating;')
# result = engine.execute(sql)
meta.create_all(engine)




#########################################################################################
############################# Population des tables #####################################

# peupler la table user

with engine.connect() as connection:
    with open ("users.csv") as user_csv:
        user_reader = csv.reader(user_csv, delimiter=';')
        for row in user_reader:
            if user_reader.line_num == 1 :
                continue
            #row=l.split('')
            user_id= (row[0])
            location = (row[1])
            age = (row[2])
            with connection.begin() as transaction:
                try:
                    markers = ','.join('?'* len(row))
                    insere = 'INSERT OR REPLACE INTO {tablename} VALUES ({markers})'
                    insere = insere.format(tablename=user.name, markers=markers)
                    connection.execute(insere, (user_id, location, age))
                except:
                    transaction.rollback()
                    raise
                else:
                    transaction.commit()       


# afficher la table user

with engine.connect() as connection:
    print("\nafficher les 10 premiers éléments de la table user")
    results = connection.execute("SELECT * FROM user LIMIT 10;")
    table_user = results.fetchall()
    show_table((table_user))




# peupler la table book

with engine.connect() as connection:
    results = connection.execute("SELECT * FROM user;")
    taille_table_user = len(results.fetchall())
    print(taille_table_user)
    with open ("books.csv") as book_csv:
        book_reader = csv.reader(book_csv, delimiter=';')
        for row in book_reader:
            if (book_reader.line_num == 1 or book_reader.line_num >  taille_table_user ):
                continue
            #row=l.split('')
            book_id= (row[0])
            book_title = (row[1])
            book_author = (row[2])
            year_of_publication = (row[3])
            publisher = (row[4])
            image_url_s = (row[5])
            image_url_m = (row[6])
            image_url_l = (row[7])

            with connection.begin() as transaction:
                try:
                    markers = ','.join('?'* len(row))
                    insere = 'INSERT OR REPLACE INTO {tablename} VALUES ({markers})'
                    insere = insere.format(tablename=book.name, markers=markers)
                    connection.execute(insere, (book_id, book_title, book_author, year_of_publication, publisher, image_url_s, image_url_m, image_url_l))
                except:
                    transaction.rollback()
                    #raise
                else:
                    transaction.commit() 


# afficher la table book

with engine.connect() as connection:
    print("\nafficher les 10 premiers éléments de la table book")
    results = connection.execute("SELECT * FROM book LIMIT 10;")
    show_table((results.fetchall()))


# peupler la table ratings

with engine.connect() as connection:
    results = connection.execute("SELECT * FROM user;")
    taille_table_user = len(results.fetchall())
    with open ("ratings.csv") as rating_csv:
        rating_reader = csv.reader(rating_csv, delimiter=';')
        for row in rating_reader:
            if rating_reader.line_num == 1 :
                continue
            #row=l.split('')
            user_id= (row[0])
            book_id = (row[1])
            rate = (row[2])
            with connection.begin() as transaction:
                try:
                    markers = ','.join('?'* len(row))
                    insere = 'INSERT OR REPLACE INTO {tablename} VALUES ({markers})'
                    insere = insere.format(tablename=rating.name, markers=markers)
                    connection.execute(insere, (user_id, book_id, rate))
                except:
                    transaction.rollback()
                    raise
                else:
                    transaction.commit() 


# afficher la table rating

with engine.connect() as connection:
    print("\nafficher les 10 premiers éléments de la table rating")
    results = connection.execute("SELECT * FROM rating LIMIT 10;")
    show_table((results.fetchall()))

