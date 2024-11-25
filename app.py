#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'


films = [
    {'id': 1 , 'titreFilm' : 'Le diner de con' , 'dateSortie' : '1998-04-15' , 'nomRealisateur' : 'Francis Veber' , 'genre_id' : 1 , 'duree' : 90, 'affiche':'film_1.jpg' },
    {'id':2,'titreFilm':'Intouchable' , 'dateSortie':'2012-03-28' , 'nomRealisateur':'Eric Toledano','genre_id':1 ,'duree':125, 'affiche':'film_2.jpg' },
    {'id':3,'titreFilm':'Piège de cristal' , 'dateSortie':'1988-09-21' , 'nomRealisateur':'John McTiernan' , 'genre_id':3 ,'duree':90, 'affiche':'film_3.jpg'},
    {'id':4,'titreFilm':'Indiana Jones' , 'dateSortie':'1989-10-18' , 'nomRealisateur':'Steven Spielberg' , 'genre_id':2 ,'duree':125, 'affiche':'film_4.jpg'},
    {'id':5,'titreFilm':'Blade Runner' , 'dateSortie':'1982-09-15' , 'nomRealisateur':'Ridley Scott' , 'genre_id':2 ,'duree' :145, 'affiche':'film_5.jpg'},
    {'id':6,'titreFilm':'Alien' , 'dateSortie':'1979-09-12' , 'nomRealisateur':'Ridley Scott' , 'genre_id':2 ,'duree' :125, 'affiche':'film_6.jpg'},
    {'id':7,'titreFilm':'L Exorciste' , 'dateSortie':'2001-03-14' , 'nomRealisateur':'William Friedkin' , 'genre_id':6 ,'duree':90, 'affiche':'film_7.jpg'},
    {'id':8,'titreFilm':'Psychose' , 'dateSortie':'1960-11-02' , 'nomRealisateur':'Alfred Hitchcock' , 'genre_id':6 ,'duree':125, 'affiche':'film_8.jpg'},
    {'id':9,'titreFilm':'Toy Story' , 'dateSortie':'1996-03-27' , 'nomRealisateur':'John Lasseter' , 'genre_id':5 ,'duree' :90, 'affiche':'film_9.jpg'},
    {'id':10,'titreFilm':'Shrek' , 'dateSortie':'2001-07-04' , 'nomRealisateur':'Andrew Adamson ' , 'genre_id':5 ,'duree' :90, 'affiche':'film_10.jpg'},
    {'id':11,'titreFilm':'La Communauté de l anneau' , 'dateSortie':'2001-12-19' , 'nomRealisateur':'Peter Jackson' , 'genre_id':4 ,'duree' :150, 'affiche':'film_11.jpg'},
    {'id':12,'titreFilm':'Les Deux Tours' , 'dateSortie':'2002-12-18' , 'nomRealisateur':'Peter Jackson' , 'genre_id':4 ,'duree' :152, 'affiche':'film_12.jpg'},
    {'id':13,'titreFilm':'Le Retour du roi' , 'dateSortie':'2003-12-17' , 'nomRealisateur':'Peter Jackson' , 'genre_id':4 ,'duree' :149, 'affiche':'film_13.jpg'},
    {'id':14,'titreFilm':'Inception' , 'dateSortie':'2010-07-08' , 'nomRealisateur':'Christopher Nolan' , 'genre_id':2 ,'duree' :90, 'affiche':'film_14.jpg'},
    {'id':15,'titreFilm':'Warrior' , 'dateSortie':'2011-09-14' , 'nomRealisateur':'Gavin O Connor' , 'genre_id':3 ,'duree' :120, 'affiche':'film_15.jpg'},
    {'id':16,'titreFilm':'Harry Potter à l école des sorciers' , 'dateSortie':'2001-12-05' , 'nomRealisateur':'Chris Columbus' , 'genre_id':4 ,'duree' :125, 'affiche':'film_16.jpg'},
    {'id':17,'titreFilm':'Harry Potter et la Chambre des secrets' , 'dateSortie':'2002-12-04' , 'nomRealisateur':'Chris Columbus' , 'genre_id':4 ,'duree' :125, 'affiche':'film_17.jpg'},
    {'id':18,'titreFilm':'Harry Potter et le Prisonnier d Azkaban' , 'dateSortie':'2004-06-02' , 'nomRealisateur':'Alfonso Cuarón' , 'genre_id':4 ,'duree' :125, 'affiche':'film_18.jpg'},
    {'id':19,'titreFilm':'Harry Potter et la Coupe de feu' , 'dateSortie':'2005-11-30' , 'nomRealisateur': 'Mike Newell' , 'genre_id':4 ,'duree' : 125, 'affiche':'film_19.jpg'},
    {'id':20,'titreFilm':'Harry Potter et l Ordre du phénix' , 'dateSortie':'2009-07-15' , 'nomRealisateur': 'David Yates' , 'genre_id':4 ,'duree' : 125, 'affiche':'film_19.jpg'}
]


genresFilms=[
    {'id':1,'libelleGenre':'Comedie', 'logo':'logo_comedie.png'},
    {'id':2,'libelleGenre':'Science-Fiction', 'logo':'logo_science_fiction.png'},
    {'id':3,'libelleGenre':'Action', 'logo':'logo_action.png'},
    {'id':4,'libelleGenre':'Fantasy', 'logo':'logo_fantasy.png'},
    {'id':5,'libelleGenre':'Animation', 'logo':'logo_animation.png'},
    {'id':6,'libelleGenre':'Horreur', 'logo':'logo_horreur.png'}
]

@app.route('/', methods=['GET'])
def show_layout():
    return render_template('layout.html')

@app.route('/genre-film/show', methods=['GET'])
def show_genre():
    return render_template('genre/show_genre.html', genresFilms = genresFilms )

@app.route('/genre-film/add', methods=['GET'])
def add_genre():
    return render_template('genre/add_genre.html', genresFilms = genresFilms)

@app.route('/genre-film/add', methods=['POST'])
def valid_add_genre():
    libelleGenre = request.form.get('libelleGenre', '')
    logo = request.form.get('logo', '')
    print(u'ville ajoutée , Ville :', libelleGenre, logo)
    message = u'Genre ajouté , Genre:'+libelleGenre + ' - logo' + logo
    flash(message, 'alert-success')
    return redirect('/genre-film/show')

@app.route('/genre-film/delete', methods=['GET'])
def delete_genre():
    id = request.args.get('id', '')
    print ("Un genre supprimé, id :",id)
    message=u'Un genre supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/genre-film/show')

@app.route('/genre-film/edit', methods=['GET'])
def edit_genre(genresFilms=None):
    id = request.args.get('id', '')
    id=int(id)
    genresFilms = genresFilms[id-1]
    return render_template('genre/edit_genre.html', genresFilms = genresFilms )

@app.route('/genre-film/edit', methods=['POST'])
def valid_edit_genre():
    libelleGenre = request.form.get('libelle', '')
    id = request.form.get('id', '')
    logo = request.form.get('logo', '')
    print(u'Genre modifié, id: ',id, " - Genre :", libelleGenre, " - Film :", logo)
    message=u'Genre modifié, id: ' + id + " - Genre : " + libelleGenre + " - Logo : " + logo
    flash(message, 'alert-success')
    return redirect('/genre-film/show')

@app.route('/film/show', methods=['GET'])
def show_film():
    return render_template('film/show_film.html', films=films)

@app.route('/film/add', methods=['GET'])
def add_film():
    return render_template('film/add_film.html', films=films, genresFilms=genresFilms)

@app.route('/film/add', methods=['POST'])
def valid_add_film():
    titreFilm = request.form.get('titreFilm', '')
    dateSortie = request.form.get('dateSortie', '')
    nomRealisateur = request.form.get('nomRealisateur', '')
    genre_id = request.form.get('genre_id', '')
    duree = request.form.get('duree', '')
    affiche = request.form.get('affiche', '')
    message = u'Film ajouté ' + ',  titreFilm:' + titreFilm + ' - dateSortie:' + dateSortie + ' - nomRealisateur:'+  nomRealisateur + ' - genre_id:' + genre_id + ' - duree:' + duree + ' - affiche:' + affiche
    print(message)
    flash(message, 'alert-success')
    return redirect('/film/show')

@app.route('/film/delete', methods=['GET'])
def delete_film():
    id = request.args.get('id', '')
    message=u'un film supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/film/show')

@app.route('/film/edit', methods=['GET'])
def edit_film(genresFilms=None):
    id = request.args.get('id', '')
    id=int(id)
    genresFilms = genresFilms[id-1]
    return render_template('film/edit_film.html', films=films, genresFilms=genresFilms)

@app.route('/film/edit', methods=['POST'])
def valid_edit_film():
    titreFilm = request.form.get('titreFilm', '')
    dateSortie = request.form.get('dateSortie', '')
    nomRealisateur = request.form.get('nomRealisateur', '')
    genre_id = request.form.get('genre_id', '')
    duree = request.form.get('duree', '')
    affiche = request.form.get('affiche', '')
    message = u'Parking modifié' + ', titreFilm:' + titreFilm + ' - id :' + id + ' - dateSortie:' + dateSortie + ' - nomRealisateur:' + nomRealisateur + ' - genre_id:' + genre_id + ' - duree:' + duree + ' - affiche:' + affiche
    print(message)
    flash(message, 'alert-success')
    return redirect('/film/show')


@app.route('/film/filtre', methods=['GET'])
def filtre_film():
    filter_word = request.args.get('filter_word', None)
    filter_value_min = request.args.get('filter_value_min', None)
    filter_value_max = request.args.get('filter_value_max', None)
    filter_items = request.args.getlist('filter_items')

    if filter_word and filter_word != "":
        message = u'Filtre sur le mot : ' + filter_word
        flash(message, 'alert-success')
        if filter_value_min or filter_value_max:
            if filter_value_min.isdecimal() and filter_value_max.isdecimal():
                if int(filter_value_min) < int(filter_value_max):
                    message = u'Filtre sur la colonne avec un numérique entre : ' + filter_value_min + ' et ' + filter_value_max
                    flash(message, 'alert-success')
                else:
                    message = u'min < max'
                    flash(message, 'alert-warning')
            else:
                message = u'min et max doivent être des numériques'
                flash(message, 'alert-warning')

        if filter_items:
            message = u'Cases sélectionnées : '
            for case in filter_items:
                message += 'id' + case + ' '
            flash(message, 'alert-success')
    return render_template('/film/front_film_filtre_show.html', films=films, genresFilms=genresFilms)

if __name__ == '__main__':
    app.run()