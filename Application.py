#-------------------------------------------------------------------------------
# Name:        Zadatak Croz
# Purpose:     Testiranje
#
# Author:      Jadranko
#
# Created:     16.11.2019
# Copyright:   (c) Jadranko 2019
# Version:     2
#-------------------------------------------------------------------------------

from flask import ( Flask,
                    render_template,
                    redirect,
                    url_for,
                    flash,
                    request,
                    jsonify )

from appclasses import (UserConnection,
                        ConnectionData,
                        Db_connection,
                        JokeGrid,
                        JokeForm)

app = Flask(__name__)
app.secret_key = 'MySecretKey'

glo_login = False

# Početni ekran sa popisom viceva
@app.route('/', methods=['GET','POST'])
def index():
    records = ""
    if request.method == "POST":
        if glo_login:

            # Dohvaćamo like / dislike
            like    = request.form.get("like",0)
            dislike = request.form.get("dislike",0)
            row_id  = 0
            like_dislike = ""

            if int(like) > 0:
                like         = 1
                like_dislike = "Like"
                row_id       = request.form.get("like")

            if int(dislike) > 0:
                dislike      = 1
                like_dislike = "Dislike"
                row_id       = request.form.get("dislike")

            print("like: ", like,", dislike: ", dislike, ", id: ", row_id)

            if like > 0 or dislike > 0:
                db_conn = Db_connection.Db_connection( db_variable.getUser(),
                                                       db_variable.getPass(),
                                                       db_variable.getHost(),
                                                       db_variable.getPort(),
                                                       db_variable.getBase() )
                try:
                    db_conn.connect()
                    insert_query = f" UPDATE joke set likes = likes + {like}, dislikes = dislikes + {dislike} where id = {row_id} "
                    print("Query: ", insert_query)
                    db_conn.insert_data(insert_query)
                    updated = db_conn.rows_inserted
                    db_conn.disconnect()
                    if updated != 0:
                        flash(like_dislike + " je uspješno zabilježen!")
                        return redirect(url_for('index'))
                    else:
                        flash(like_dislike + " nije zabilježen!")
                        return redirect(url_for('index'))

                except Exception as e:
                    flash("Dogodila se pogreška kod ažuriranja sloga u bazi!", str(e))
                    db_conn.disconnect()
                    return redirect(url_for('index'))
        else:
            print("Za opcije like i dislike potrebno je biti logiran\n")
            flash("Za opcije like i dislike potrebno je biti logiran!")
            return redirect(url_for('index'))

    # Prikaz podataka
    dataGrid = JokeGrid.JokeGrid()
    try:
        records =  dataGrid.show()
    except Exception as e:
        flash("Dogodila se pogreška kod spajanja na bazu!", str(e))

    return render_template('index.html', records=records)

# Eekran za unos vica
@app.route('/new', methods=['GET','POST'])
def addJoke():
    # Ovisno o GET/POST prikazujem formu ili obrađujem podatke
    if not glo_login:
        flash("Za unos vica morate se prijaviti u sustav!")
        return redirect(url_for('index'))

    if request.method == "POST" and glo_login:
        db_conn = Db_connection.Db_connection( db_variable.getUser(),
                                               db_variable.getPass(),
                                               db_variable.getHost(),
                                               db_variable.getPort(),
                                               db_variable.getBase() )
        try:
            db_conn.connect()
            if len(request.form.get("content").strip()) == 0:
                print("Potrebno je unijeti sadržaj\n")
                flash("Potrebno je unijeti sadržaj!")

            if len(request.form.get("category").strip()) == 0:
                print("Potrebno je unijeti kategoriju\n")
                flash("Potrebno je unijeti kategoriju!")

            if len(request.form.get("category").strip()) == 0 or len(request.form.get("content").strip()) == 0:
                insertForm = JokeForm.JokeForm()
                form_data = insertForm.show()
                return render_template('add_joke.html', form_data=form_data)

            content  = request.form.get("content").strip()
            category = request.form.get("category")
            insert_query = f"INSERT INTO joke (id, content, category_id) VALUES (DEFAULT,'{content}','{category}')"

            """
            # SAFE EXAMPLES. DO THIS!
            cursor.execute("SELECT admin FROM users WHERE username = %s'", (username, ));
            cursor.execute("SELECT admin FROM users WHERE username = %(username)s", {'username': username});
            """

            print("Query: ", insert_query)
            db_conn.insert_data(insert_query)
            inserted = db_conn.rows_inserted
            db_conn.disconnect()
            if inserted != 0:
                flash("Slog je uspješno unesen u bazu!")
                return redirect(url_for('index'))
            else:
                flash("Slog nije unesen u bazu!")
                return redirect(url_for('index'))

        except Exception as e:
            flash("Dogodila se pogreška kod unosa novog sloga u bazu!", str(e))
            db_conn.disconnect()
            return redirect(url_for('index'))

    insertForm = JokeForm.JokeForm()
    try:
        form_data = insertForm.show()
    except Exception as e:
        flash("Dogodila se pogreška kod spajanja na bazu!", str(e))
        return render_template('index.html')
    return render_template('add_joke.html', form_data=form_data)

# Eekran za autentifikaciju
@app.route('/login', methods=['GET', 'POST'])
def authentication():
    global glo_login

    login_user = request.form.get("username",None)
    login_pass = request.form.get("password",None)

    print("auth: ",request.method,app_user.checkIfexists(login_user))

    # Provjere za login
    if request.method == "POST" and not glo_login:
        if login_user is None or len(login_user.strip()) == 0:
            print("Potrebno je unijeti korisničko ime\n")
            #flash("Potrebno je unijeti korisničko ime!")

        if login_pass is None or len(login_pass.strip()) == 0:
            print("Potrebno je unijeti lozinku\n")
            #flash("Potrebno je unijeti lozinku!")

        if app_user.checkIfexists(login_user) and login_pass == app_user.auth_data.getUser(login_user):
            glo_login = True
            flash("Uspješno ste se prijavili u sustav!")
            return redirect(url_for('index'))
        else:
            print("Neispravni podaci za autentikaciju\n")
            flash("Neispravni podaci za autentikaciju!")

    return render_template('login.html')

# Eekran za logout
@app.route('/logout', methods=['GET'])
def logout():
    global glo_login

    glo_login = False

    print("Uspješno ste se odjavili\n")
    flash("Uspješno ste odjavljeni!")

    # Prikaz podataka
    dataGrid = JokeGrid.JokeGrid()
    records =  dataGrid.show()

    return render_template('index.html', records=records)


# Glavno izvođenje programa ####################################################

if __name__ == '__main__':

    # Inicijalizacija korisnika sa vremenom konekcije
    app_user = UserConnection.UserConnection()

    # Inicijalizacija varijabli za konekciju
    db_variable = ConnectionData.ConnectionData()

    # Startanje aplikacije na portu 8080
    print("Start...")
    #app.run(debug = True, port=8080)
    app.run(debug = False, port=8080)

    # Pozdravna poruka za izlaz iz programa
    print("Stop.")