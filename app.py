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
            host="localhost",                 # à modifier
            user="ahaddou2",                     # à modifier
            password="mdp",                # à modifier
            database="BDD_ahaddou",        # à modifier
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
    sql= ''' SELECT Mission.Id_Mission AS id, Mission.DateDébut AS DateDébut, Mission.DateFin AS DateFin, Mission.Kg_CO2 AS Kg_CO2, Agent.Nom AS Nom, Mission.Id_Agent, Type_mission.LibelleTypeMission AS TypeMission, Mission.Budget AS Budget
        FROM Mission
        INNER JOIN Agent ON Mission.Id_Agent = Agent.Id_Agent
        INNER JOIN Type_mission ON Mission.Id_TypeMission = Type_mission.Id_TypeMission'''
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
    flash(f'Une mission a été suprrimée avec succès ! : Identifiant :{id} ')
    return redirect('/mission/show')

@app.route('/mission/edit', methods=['GET'])
def edit_mission():
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = ''' SELECT Mission.Id_Mission AS id, Mission.DateDébut AS DateDébut, Mission.DateFin AS DateFin, Mission.Kg_CO2 AS Kg_CO2, Mission.Budget AS Budget,Agent.Nom AS Nom, Mission.Id_TypeMission AS Id_TypeMission, Mission.Id_Agent AS Id_Agent
            FROM Mission
            INNER JOIN Agent ON Mission.Id_Agent = Agent.Id_Agent
            WHERE Mission.Id_Mission = %s;'''
    mycursor.execute(sql, (id,))
    mission = mycursor.fetchone()
    sql_agents = '''SELECT Id_Agent, Nom FROM Agent'''
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
    Budget = request.form.get('Budget') or ''
    message = f'Une mission a été ajoutée avec succès ! : date de début : {DateDébut} | date de fin : {DateFin} | Kg CO2 : {Kg_CO2}Kg - type de mission : {Id_TypeMission} | agent : {Id_Agent} | budget : {Budget}€'
    flash(message)
    mycursor = get_db().cursor()
    sql = ''' INSERT INTO Mission (DateDébut, DateFin, Kg_CO2, Id_TypeMission, Id_Agent, Budget) 
            VALUES (%s, %s, %s, %s, %s, %s); '''
    tuple_param = (DateDébut, DateFin, Kg_CO2, Id_TypeMission, Id_Agent, Budget)
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
    Budget = request.form.get('Budget') or None
    message = f"Mission mise à jour avec succès !  Dates : {DateDébut} - {DateFin} | CO2 estimé : {Kg_CO2} Kg | Type de mission : {Id_TypeMission} | Agent responsable : {Id_Agent} | Budget alloué : {Budget} €"
    flash(message)
    sql = ''' UPDATE Mission 
        SET DateDébut = %s, DateFin = %s, Kg_CO2 = %s, Id_Agent = %s, Id_TypeMission = %s, Budget = %s 
        WHERE Id_Mission = %s;'''
    tuple_param = (DateDébut, DateFin, Kg_CO2, Id_Agent, Id_TypeMission, Budget, Id_Mission)
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/mission/show')





@app.route('/etape/show')
def show_etapes():
    mycursor = get_db().cursor()
    sql= ''' SELECT Etape.Id_Etape AS id,Etape.DistanceParcourue AS DistanceParcourue,Moyen_transport.LibelleTransport AS MoyenTransport,Etape.Heure_depart AS HeureDepart,Etape.Heure_arrivee AS HeureArrivee,LieuDepart.LibelleLieu AS LieuDepart,LieuArrivee.LibelleLieu AS LieuArrivee,Mission.Id_Mission AS IdMission,Type_mission.LibelleTypeMission AS TypeMission
    FROM Etape
    JOIN Moyen_transport ON Etape.Id_MoyenTransport = Moyen_transport.Id_MoyenTransport
    JOIN Lieu AS LieuDepart ON Etape.Id_Lieu_depart = LieuDepart.Id_Lieu
    JOIN Lieu AS LieuArrivee ON Etape.Id_Lieu_arrivee = LieuArrivee.Id_Lieu
    JOIN Mission ON Etape.Id_Mission = Mission.Id_Mission
    JOIN Type_mission ON Mission.Id_TypeMission = Type_mission.Id_TypeMission;'''
    mycursor.execute(sql)
    liste_etapes = mycursor.fetchall()
    return render_template('etape/show_etape.html', etapes=liste_etapes )


@app.route('/etape/add', methods=['GET'])
def add_etape():
    print("Affichage du formulaire pour saisir une étape")
    mycursor = get_db().cursor()
    sql_moyens_transport = '''SELECT Id_MoyenTransport, LibelleTransport FROM Moyen_transport'''
    mycursor.execute(sql_moyens_transport)
    moyens_transport = mycursor.fetchall()
    sql_lieux = '''SELECT Id_Lieu, LibelleLieu FROM Lieu'''
    mycursor.execute(sql_lieux)
    lieux = mycursor.fetchall()
    sql_missions = '''SELECT Id_Mission, DateDébut FROM Mission'''
    mycursor.execute(sql_missions)
    missions = mycursor.fetchall()
    return render_template('etape/add_etape.html', moyens_transport=moyens_transport, lieux=lieux, missions=missions)


@app.route('/etape/delete')
def delete_etape():
    print('''suppression d'une étape''')
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id')
#delete
    mycursor = get_db().cursor()
    sql = ''' DELETE FROM Etape WHERE Id_Etape = %s '''
    tuple_param=(id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/etape/show')


@app.route('/etape/edit', methods=['GET'])
def edit_etape():
    print('Affichage du formulaire pour modifier une étape')
    id = request.args.get('id')
    id = int(id)
    mycursor = get_db().cursor()
    sql = ''' SELECT Etape.Id_Etape, Etape.DistanceParcourue, Etape.Id_MoyenTransport, Etape.Id_Lieu_depart, Etape.Id_Lieu_arrivee, Etape.Id_Mission
            FROM Etape
            WHERE Etape.Id_Etape = %s; '''
    mycursor.execute(sql, (id,))
    etape = mycursor.fetchone()
    sql_moyens_transport = '''SELECT Id_MoyenTransport, LibelleTransport FROM Moyen_transport'''
    mycursor.execute(sql_moyens_transport)
    moyens_transport = mycursor.fetchall()
    sql_lieux = '''SELECT Id_Lieu, LibelleLieu FROM Lieu'''
    mycursor.execute(sql_lieux)
    lieux = mycursor.fetchall()
    sql_missions = ''' SELECT Mission.Id_Mission, Type_mission.LibelleTypeMission AS TypeMission
                    FROM Mission
                    JOIN Type_mission ON Mission.Id_TypeMission = Type_mission.Id_TypeMission;'''
    mycursor.execute(sql_missions)
    missions = mycursor.fetchall()
    return render_template('etape/edit_etape.html', etape=etape, moyens_transport=moyens_transport, lieux=lieux,missions=missions)


@app.route('/etape/add', methods=['POST'])
def valid_add_etape():
    print("Ajout de l'étape dans le tableau")
    DistanceParcourue = request.form.get('DistanceParcourue') or ''
    Id_MoyenTransport = request.form.get('Id_MoyenTransport') or ''
    Id_Lieu_depart = request.form.get('Id_Lieu_depart') or ''
    Id_Lieu_arrivee = request.form.get('Id_Lieu_arrivee') or ''
    Id_Mission = request.form.get('Id_Mission') or ''
    Heure_depart = request.form.get('Heure_depart') or ''
    Heure_arrivee = request.form.get('Heure_arrivee') or ''
    message = f"Étape ajouté avec succès ! pour la mission d'identifiant {Id_Mission} | Distance parcourue : {DistanceParcourue} km | Moyen de transport : {Id_MoyenTransport} | Lieu départ : {Id_Lieu_depart} | Lieu arrivée : {Id_Lieu_arrivee}  | Heure départ : {Heure_depart}:00 | Heure arrivée : {Heure_arrivee}:00"
    flash(message)
    mycursor = get_db().cursor()
    sql = '''INSERT INTO Etape (DistanceParcourue, Id_MoyenTransport, Id_Lieu_arrivee, Id_Lieu_depart, Id_Mission, Heure_depart, Heure_arrivee) 
             VALUES (%s, %s, %s, %s, %s, %s, %s);'''
    tuple_param = (DistanceParcourue, Id_MoyenTransport, Id_Lieu_arrivee, Id_Lieu_depart, Id_Mission, Heure_depart, Heure_arrivee)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/etape/show')


@app.route('/etape/edit', methods=['POST'])
def valid_edit_etape():
    print('Modification de l étape dans le tableau')
    IdEtape = request.form.get('IdEtape')
    DistanceParcourue = request.form.get('DistanceParcourue') or None
    Id_MoyenTransport = request.form.get('Id_MoyenTransport') or None
    Id_Lieu_arrivee = request.form.get('Id_Lieu_arrivee') or None
    Id_Lieu_depart = request.form.get('Id_Lieu_depart') or None
    Id_Mission = request.form.get('Id_Mission') or None
    message = f"Étape mise à jour avec succès !  Distance parcourue : {DistanceParcourue} km | Moyen de transport : {Id_MoyenTransport} | Lieu de départ : {Id_Lieu_depart} | Lieu d'arrivée : {Id_Lieu_arrivee} | Mission associée : {Id_Mission}"
    flash(message)
    sql = '''UPDATE Etape
                SET DistanceParcourue = %s, Id_MoyenTransport = %s, Id_Lieu_arrivee = %s, Id_Lieu_depart = %s, Id_Mission = %s
                WHERE Id_Etape = %s;'''
    tuple_param = (DistanceParcourue, Id_MoyenTransport, Id_Lieu_arrivee, Id_Lieu_depart, Id_Mission, IdEtape)
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/etape/show')

@app.route('/mission/etat-mission/')
def etat_missions():
    return render_template('mission/choix_etat_mission.html')

@app.route('/mission/etat-mission/agents')
def etat_agents():
    mycursor = get_db().cursor()
    sql = '''SELECT Agent.Nom AS Nom_Agent, Agent.Prenom AS Prenom_Agent,
                COUNT(Mission.Id_Mission) AS Nombre_Missions
            FROM Mission
            JOIN Agent ON Mission.Id_Agent = Agent.Id_Agent
            GROUP BY Agent.Id_Agent, Agent.Nom, Agent.Prenom;'''
    mycursor.execute(sql)
    agents_missions = mycursor.fetchall()
    return render_template('mission/etat_mission_agent.html', agents_missions=agents_missions)

@app.route('/mission/etat-mission/budget')
def etat_missions_par_budget():
    mycursor = get_db().cursor()
    sql = '''SELECT Agent.Nom AS Nom_Agent, Agent.Prenom AS Prenom_Agent,
                SUM(Mission.Budget) AS Total_Budget
            FROM Mission
            JOIN Agent ON Mission.Id_Agent = Agent.Id_Agent
            GROUP BY Agent.Id_Agent, Agent.Nom, Agent.Prenom;'''
    mycursor.execute(sql)
    agents_budget_data = mycursor.fetchall()
    return render_template('mission/etat_mission_budget.html', agents_budget=agents_budget_data)


@app.route('/mission/etat-mission/agent_du_mois')
def agent_du_mois():
    mycursor = get_db().cursor()
    sql = '''SELECT Agent.Nom AS Nom_Agent, Agent.Prenom AS Prenom_Agent,
                COALESCE(SUM(Mission.Kg_CO2), 0) AS Total_CO2
            FROM Agent
            LEFT JOIN Mission ON Mission.Id_Agent = Agent.Id_Agent
            GROUP BY Agent.Id_Agent, Agent.Nom, Agent.Prenom
            ORDER BY Total_CO2 ASC'''
    mycursor.execute(sql)
    agent_du_mois = mycursor.fetchone()
    return render_template('mission/etat_mission_agent_du_mois.html', agent=agent_du_mois)

@app.route('/etape/etat-etape/')
def etat_etapes():
    return render_template('etape/choix_etat_etape.html')


@app.route('/etape/etat-etape/mission')
def etat_etapes_mission():
    mycursor = get_db().cursor()
    sql = '''SELECT Mission.DateDébut, 
                COUNT(Etape.Id_Etape) AS Nombre_Etapes
            FROM Etape
            JOIN Mission ON Etape.Id_Mission = Mission.Id_Mission
            GROUP BY Mission.Id_Mission;'''
    mycursor.execute(sql)
    etapes = mycursor.fetchall()
    return render_template('etape/etat_etape_mission.html', etapes=etapes)

@app.route('/etape/etat-etape/distance')
def etat_etapes_distance():
    mycursor = get_db().cursor()
    sql = '''SELECT Type_mission.LibelleTypeMission,
                SUM(Etape.DistanceParcourue) AS Distance_Totale
            FROM Etape
            JOIN Mission ON Etape.Id_Mission = Mission.Id_Mission
            JOIN Type_mission ON Mission.Id_TypeMission = Type_mission.Id_TypeMission
            GROUP BY Type_mission.LibelleTypeMission;'''
    mycursor.execute(sql)
    distance = mycursor.fetchall()
    return render_template('etape/etat_etape_distance.html', distances=distance)

@app.route('/etape/etat-etape/transport')
def etat_etapes_transport():
    mycursor = get_db().cursor()
    mycursor.execute()
    transport = mycursor.fetchall()
    return render_template('etape/etat_etape_transport.html', transport=transport)

if __name__ == '__main__':
    app.run(debug=True, port=5000)