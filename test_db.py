import sqlite3
import sqlalchemy
from sqlalchemy import inspect, create_engine, text
from pprint import pprint
import fastapi

engine = create_engine("sqlite:///bdd_datascientest_projet3.db")


#affciher les tables de la bdd
inspector = inspect(engine)
pprint(inspector.get_table_names())

#afficher les attributs des tables:
for table in inspector.get_table_names():
    pprint(inspector.get_columns(table_name=table))
    
#affichier les clefs etrangeres de la able rating
print("\n",inspector.get_foreign_keys(table_name='rating'))
    
#afficher le top 10 des livre 
requette = text("SELECT book_title, rate, image_url_l FROM book INNER JOIN rating ON book.book_id = rating.book_id ORDER BY rate DESC LIMIT 10 ")
results = engine.execute(requette)
print("\n les 10 des livres les mieux notés:\n")
pprint(results.fetchall())


#affichier la distribution de l'age 
requette = text("SELECT age, COUNT(age) AS distribution FROM USER GROUP BY age ORDER BY age")
results = engine.execute(requette)
print("\n la distribution de l'age:")
pprint(results.fetchall())