#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash
from more_itertools.recipes import grouper
#mysql --user=nfoucaul  --password=mdp --host=serveurmysql --database=BDD_nfoucaul
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

                                    ## à ajouter
from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="serveurmysql",                 # à modifier
            user="nfoucaul",                     # à modifier
            password="mdp",                # à modifier
            database="BDD_nfoucaul",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
@app.route('/')
@app.route('/mission/show')
def show_missions():
    mycursor = get_db().cursor()
    sql= ''' SELECT Id_Mission AS id, DateDébut AS DateDébut, DateFin AS DateFin, Kg_CO2 AS Kg_CO2 
    FROM Mission
    ORDER BY DateDébut DESC; '''
    mycursor.execute(sql)

    liste_missions = mycursor.fetchall()
    return render_template('mission/show_mission.html', missions=liste_missions )


@app.route('/mission/add', methods=['GET'])
def add_mission():
    print('''affichage du formulaire pour saisir une mission''')
    return render_template('mission/add_mission.html')

@app.route('/mission/delete')
def delete_mission():
    print('''suppression d'une mission''')
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id')
    #delete
    mycursor = get_db().cursor()
    sql = ''' DELETE FROM Mission WHERE Id_Mission = %s '''
    tuple_param=(id)
    mycursor.execute(sql, tuple_param)

    get_db().commit()
    return redirect('/mission/show')

@app.route('/mission/edit', methods=['GET'])
def edit_etudiant():
    print('''affichage du formulaire pour modifier une mission''')
    print(request.args.get('id'))
    id=request.args.get('id')
    if id != None and id.isnumeric():
        indice = int(id)
        mycursor = get_db().cursor()
        sql = ''' SELECT Id_Mission AS id, DateDébut AS DateDébut, DateFin AS DateFin, Kg_CO2 AS Kg_CO2
            FROM Mission
            WHERE Id_Mission=%s;'''
        mycursor.execute(sql, (id))
        mission = mycursor.fetchone()
    else:
        mission=[]
    return render_template('mission/edit_mission.html', mission=mission)


@app.route('/mission/add', methods=['POST'])
def valid_add_mission():
    print('''ajout de la mission dans le tableau''')
    DateDébut = request.form.get('DateDébut')
    DateFin = request.form.get('DateFin')
    Kg_CO2 = request.form.get('Kg_CO2')
    message = 'date de début :' + DateDébut + ' - Date de fin :' + DateFin  + ' - Killogramme de CO2 : ' + Kg_CO2
    print(message)
    #insert
    mycursor = get_db().cursor()
    sql = ''' INSERT INTO Mission (Id_Mission, DateDébut, DateFin, Kg_CO2) 
    VALUES (NULL, %s, %s); '''
    tuple_param = (DateDébut, DateFin, Kg_CO2)
    mycursor.execute(sql, tuple_param)


    get_db().commit()
    return redirect('/mission/show')

@app.route('/mission/edit', methods=['POST'])
def valid_edit_etudiant():
    print('''modification de la mission dans le tableau''')
    id = request.form.get('id')
    DateDébut = request.form.get('DateDébut')
    DateFin = request.form.get('DateFin')
    Kg_CO2 = request.form.get('Kg_CO2')
    message = 'Date de début :' + DateDébut + ' - Date de fin :' + DateFin + ' - Kilogrammes de CO2 ' + Kg_CO2 + ' pour l etudiant d identifiant :' + id
    print(message)
    #update
    mycursor = get_db().cursor()
    sql = ''' UPDATE Mission SET DateDébut = %s, DateDébut = %s, Kg_CO2 = %s ,WHERE Id_Mission = %s;'''
    tuple_param = (DateDébut, DateFin, Kg_CO2 ,id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/mission/show')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

