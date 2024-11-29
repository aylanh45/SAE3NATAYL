#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash
from more_itertools.recipes import grouper
#mysql --user=nfoucaul  --password=mdp --host=serveurmysql --database=BDD_nfoucaul

#mysql --user=ahaddou2  --password=mdp --host=serveurmysql --database=BDD_ahaddou2
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
            database="BDD_nfoucaul_tp",        # à modifier
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
def show_accueil():
    return render_template('layout.html')
@app.route('/mission/show')
def show_missions():
    mycursor = get_db().cursor()
    sql= ''' SELECT Mission.Id_Mission AS id, Mission.DateDébut AS DateDébut, Mission.DateFin AS DateFin, Mission.Kg_CO2 AS Kg_CO2, Agent.Nom AS Nom, Mission.Id_Agent
        FROM Mission
        INNER JOIN Agent ON Mission.Id_Agent = Agent.Id_Agent'''
    mycursor.execute(sql)
    liste_missions = mycursor.fetchall()
    return render_template('mission/show_mission.html', missions=liste_missions )


@app.route('/mission/add', methods=['GET'])
def add_mission():
    print('''affichage du formulaire pour saisir une mission''')
    mycursor = get_db().cursor()
    sql = '''SELECT Id_TypeMission, LibelleTypeMission
    FROM Type_mission'''
    mycursor.execute(sql)
    type_missions = mycursor.fetchall()
    sql_agents ='''SELECT Id_Agent, Nom FROM Agent'''
    mycursor.execute(sql_agents)
    agents = mycursor.fetchall()
    return render_template('mission/add_mission.html', type_missions=type_missions, agents=agents)

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
def edit_mission():
    mycursor = get_db().cursor()
    id=request.args.get('id','')
    sql = ''' SELECT Mission.Id_Mission AS id, Mission.DateDébut AS DateDébut, Mission.DateFin AS DateFin, Mission.Kg_CO2 AS Kg_CO2, Agent.Nom AS Nom, Mission.Id_TypeMission AS Id_TypeMission, Mission.Id_Agent
            FROM Mission
            INNER JOIN Agent ON Mission.Id_Agent = Agent.Id_Agent
            WHERE Mission.Id_Mission = %s;'''
    mycursor.execute(sql, (id,))
    mission = mycursor.fetchone()
    sql_agents='''SELECT Id_Agent, Nom FROM Agent'''
    mycursor.execute(sql_agents)
    agents = mycursor.fetchall()
    sql_types_mission = '''SELECT Id_TypeMission, LibelleTypeMission FROM Type_mission'''
    mycursor.execute(sql_types_mission)
    type_missions = mycursor.fetchall()
    return render_template('mission/edit_mission.html', mission=mission, agents=agents, type_missions=type_missions)


@app.route('/mission/add', methods=['POST'])
def valid_add_mission():
    print('''ajout de la mission dans le tableau''')
    DateDébut = request.form.get('DateDébut') or ''
    DateFin = request.form.get('DateFin') or ''
    Kg_CO2 = request.form.get('Kg_CO2') or ''
    Id_TypeMission = request.form.get('Id_TypeMission') or ''
    Id_Agent = request.form.get('Id_Agent')
    message = 'date de début :' + DateDébut + ' - Date de fin :' + DateFin  + ' - Killogramme de CO2 : ' + Kg_CO2 + '- le type de mission a pour identifiant' + Id_TypeMission + '- une mission réalisée par l agent d identifiant' + Id_Agent
    print(message)
    #insert
    mycursor = get_db().cursor()
    sql = ''' INSERT INTO Mission (DateDébut, DateFin, Kg_CO2,Id_TypeMission, Id_Agent) 
    VALUES (%s, %s, %s, %s, %s); '''
    tuple_param = (DateDébut, DateFin, Kg_CO2, Id_TypeMission, Id_Agent)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/mission/show')


@app.route('/mission/edit', methods=['POST'])
def valid_edit_mission():
    print('Modification de la mission dans le tableau')

    Id_Mission = request.form.get('Id_Mission')
    DateDébut = request.form.get('DateDébut') or None
    DateFin = request.form.get('DateFin') or None
    Kg_CO2 = request.form.get('Kg_CO2') or None
    Id_TypeMission = request.form.get('Id_TypeMission') or None
    Id_Agent = request.form.get('Id_Agent') or None
    sql = ''' UPDATE Mission 
              SET DateDébut = %s, DateFin = %s, Kg_CO2 = %s, Id_Agent = %s, Id_TypeMission = %s
              WHERE Id_Mission = %s; '''
    tuple_param = (DateDébut, DateFin, Kg_CO2, Id_Agent, Id_TypeMission, Id_Mission)
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/mission/show')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/etape/show')
def show_etapes():
mycursor = get_db().cursor()
sql= ''' SELECT Etape.Id_Etape AS id, Etape.DistanceParcourue AS DistanceParcourue, Etape.Id_MoyenTransport AS Id_MoyenTransport, Etape.Id_Lieu_depart AS Id_Lieu_depart, Etape.Id_Lieu_arrivee AS Id_Lieu_arrivee, Etape.Id_Mission AS Id_Mission 
FROM Etape'''
mycursor.execute(sql)
liste_etapes = mycursor.fetchall()
return render_template('etape/show_etape.html', etapes=liste_etapes )
@app.route('/etudiant/add', methods=['GET'])
def add_etudiant(): print('''affichage du formulaire pour saisir un étudiant''')
return render_template('etape/add_etape.html')
@app.route('/etape/delete')
def delete_etudiant():
print('''suppression d'une étape''')
print(request.args) print(request.args.get('id'))
id=request.args.get('id')
#delete
mycursor = get_db().cursor()
sql = ''' DELETE FROM etape WHERE Id_Etape = %s '''
tuple_param=(id)
mycursor.execute(sql, tuple_param)
get_db().commit()
return redirect('/etape/show')

