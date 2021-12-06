from fastapi import FastAPI
import uvicorn
import sqlite3, sqlalchemy
from sqlalchemy import inspect, create_engine, text
from pprint import pprint


# ####### importer la base de donnée ########## #
##########################################
engine = create_engine("sqlite:///bdd_datascientest_projet3.db")

# définir l'API
api = FastAPI(
            title='Projet 3',
            description="API sur la création et la manipulation des bases de données",
            version="1.0.1")


# premire route
@api.get('/', name= "Vérifier si l'API est fonctionnelle")
# def is_functionnal(username: str = Depends(get_current_username)):
def is_functionnal():
    """On vrifie si l'API est fonctionnelle."""
    return "l'API fonctionne correctement :)"


@api.get('/bd_information', name="Avoir les informations de la BDD ")
def bdd_info():
    bdd_info = ['', 'Affciher les tables de la bdd', '-----']
    # affciher les tables de la bdd
    inspector = inspect(engine)
    pprint(inspector.get_table_names())
    bdd_info.append(inspector.get_table_names())

    # afficher les attributs des tables:
    bdd_info.append(['', 'afficher les attributs des tables', '-----'])
    for table in inspector.get_table_names():
        tmp = inspector.get_columns(table_name=table)
        pprint(tmp)
        bdd_info.append(tmp)

    return bdd_info


@api.get('/api_test', name="tester l'API ")  # , include_in_schema=False)
def api_test():

    # afficher le top 10 des livres
    requette = text("SELECT book_title, rate, image_url_l FROM book INNER JOIN rating ON book.book_id = rating.book_id ORDER BY rate DESC LIMIT 10;")
    results = engine.execute(requette)
    print("\n Les 10 des livres les mieux notés:\n")
    
    query_result = ["Les 10 des livres les mieux notés:",\
        '---------------------------------------', '']
    tmp = (results.fetchall())
    for line in tmp:
        query_result += ['Title: ' + line[0], 'Rate: ' + line[1].__str__()]
        # query_result += '\n'

    print(query_result)

    return query_result


# requeter la base de donnée
@api.get('/api_query', name="requeter la base de donnée")  # , include_in_schema=False)
def api_query(query):

    # requette = text("SELECT book_title, rate, image_url_l FROM book INNER JOIN rating ON book.book_id = rating.book_id ORDER BY rate DESC LIMIT 10;")
    requette = text(query)
    results = engine.execute(requette)
    print("\n Resultat de la requete: \n")

    query_result = []
    tmp = (results.fetchall())
    for line in tmp:
        query_result += line

    print(query_result)

    return query_result



if __name__ == '__main__':
    uvicorn.run(api, host="0.0.0.0", port=5010)
