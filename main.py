from flask import Flask,render_template,request,redirect, session
import sqlite3 as sql
import os
import Pokemon
import re


app = Flask(__name__)
app.secret_key = os.urandom(24)
pokemonFolder = os.path.join('static', 'pokemon')
app.config['UPLOAD_FOLDER'] = pokemonFolder

@app.route('/')
def login():
    if 'ERROR' in session:

        msg = session['ERROR']
        session.pop('ERROR')
        return render_template('index.html', msg= msg)
    else:
        return render_template('index.html')


@app.route('/register')
def about():
    if 'ERROR' in session:

        msg = session['ERROR']
        session.pop('ERROR')
        return render_template('register.html', msg= msg)
    else:
        return render_template('register.html')



@app.route('/home')
def home():
    #Verifie si l'utilisateur est connecter
    if 'user_id' in session:
        #Racourcis pour la classe
        a = Pokemon.Pokemon()
        #Execute proba dans la classe pokemon
        carte = a.proba()
        file = open("static/JS.js", "r")
        lignes = file.readlines()
        file.close()
        z = str(carte)
        lignes[0] = 'var test ='+z+'\n'
        file = open("static/JS.js", "w")
        file.writelines(lignes)
        file.close()

        #Connection à la base de donné
        with sql.connect("database\database.db") as con:
            cur = con.cursor()
            #Selectionne dans la conlonne carte de la table collection avec user_id comme la variable dasn le cache
            cur.execute("SELECT cartes FROM collection WHERE user_id LIKE '{}'".format(session['user_id']))
            #Transfrome en liste
            test = cur.fetchall()
            #Recuper juste la chaine de caractere qui a l'aspect d'une liste
            test = test[0][0]
            #Supprime toute les ',' de la chaine de charactere
            test = re.sub("[,]", '', test)
            #Prend les caractere dans l'intervalle
            test = test[1:len(test) - 1]
            test = re.sub(r"\s+", "", test)
            test = list(map(int, test))
            for i in range(len(carte)):
                a= carte[i]
                b= a[0:3]
                x=3
                #Boucle qui se termine quand le type de b est un entier
                while type(b) != int:
                    try:
                        b = int(b)
                    # si b est un entier la boucle s'arrete sinon elle continue
                    except ValueError:
                        #en changeant l'intervale pour reduire et prendre le chiffre
                        x -= 1
                        b = a[0:x]
                #On enleve 1 car le chiffre des carte commence à 1 et non 0
                b-=1
                #Sa place l'indicateur 1 au bon index de la liste
                for i in range(len(test)):
                    if i == b:
                        test[i] = 1
            #Remplace la donné de la case cartes par la nouvelle
            file = open("templates/collection.html", "r")
            lignes = file.readlines()
            file.close()
            z = test
            z = str(z)
            lignes[37] =  		'const list ='+z+ '\n'
            file = open("templates/collection.html","w")
            file.writelines(lignes)
            file.close()
            cur.execute("UPDATE collection SET cartes = '{}' WHERE user_id ={} ".format(test,session['user_id']))
        return render_template('home.html',carte=carte)
    else:
        return redirect('/')

@app.route('/collection')
def collection():
    if 'user_id' in session:


        return render_template('collection.html')

    else:
        return render_template('index.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    #Recupere les champs du site
    name = request.form.get('name')
    password = request.form.get('password')
    #Ce connecte à la base de donné
    with sql.connect("database\database.db") as con:
        cur = con.cursor()
        #Selectionne dans la table identifiant la ligne avec le nom et le mot de passe comme les variables recuperer avant
        cur.execute("SELECT * FROM identifiant WHERE name LIKE '{}' AND password LIKE '{}'".format(name,password)  )
        #transforme en liste
        users = cur.fetchall()

    #Condition si les donné son trouvé dans la base de donné
    if len(users)>0:
        #Rentre dans le cache la valeur de l'id de l'utilisateur
        session['user_id'] = users[0][0]

        return redirect('/home')
    #Si les donné ne sont pas trouvé dans la base de donné, un message d'erreur se crée pour avertir l'utilisateur que ses information ne sont pas correcte
    else:
        msg = "Le mot de passe ou l'adresse email est incorrecte"
        session['ERROR']= msg
        return redirect('/')



@app.route('/add_user', methods=['POST'])
def add_user():
    #Récupere les champs entré
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    ipassword = request.form.get('ipassword')
    #Je test pour voir si sa marche et si sa marche pas cela veut dire qu'il y'a des information en double
    try:
        if password == ipassword :
            #Je me connecte à ma base de donné
            with sql.connect("database\database.db") as con:
                cur = con.cursor()
            #J'execute ma ligne de SQL qui rentre dans ma table identifiant les donné dans les bonnes colonne
                cur.execute("INSERT INTO identifiant (user_id,name,email,password) VALUES (NULL,'{}','{}','{}')".format (name, email, password))

                con.commit()
                cur.execute("SELECT * FROM identifiant WHERE email LIKE '{}'".format(email))
                myuser = cur.fetchall()
                session['user_id'] = myuser[0][0]
                carte1 = []
                for i in range(102):
                    carte1.append(0)
                cur.execute("INSERT INTO collection (user_id,cartes) VALUES ('{}','{}')".format(session['user_id'],carte1))
                session['collection']=carte1
            return redirect('/home')
        else:
            msg = "Les mot de passe ne sont pas identique"
            session['ERROR'] = msg
            return redirect('/register')

    except sql.IntegrityError:
        msg = "Votre pseudo ou votre adresse e-mail est deja utilisé"
        session['ERROR'] = msg
        return redirect('/register')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

