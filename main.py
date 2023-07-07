from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datubaze.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "4t5ryhj45erg454342rwefg45erh"

db = SQLAlchemy(app)

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vards = db.Column(db.String(50))
    epasts = db.Column(db.String(100), unique=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auksta_zupa')
def auksta_zupa():
    return render_template('auksta_zupa.html')

@app.route('/citrona_dzeriens')
def citrona_dzeriens():
    return render_template('citrona_dzeriens.html')

@app.route('/kontakti')
def kontakti():
    vardnica = request.args.to_dict()
    #if vardnica.get('q'):
    if 'tel' in vardnica:
        tel = vardnica['tel']
    else:
        tel = "Nav atrasts!"

    if 'epasts' in vardnica:
        epasts = vardnica['epasts']
    else:
        epasts = "Nav atrasts!"        
        
    return render_template('kontakti.html', telefons = tel, epasts = epasts)

@app.route('/parametri')
@app.route('/parametri/<vards>')
@app.route('/parametri/<vards>/<int:cipars>')
def parametri(vards = "Nav definēts", cipars = "Nav definēts"):

    return render_template('parametri.html', vards = vards, cipars = cipars)

@app.route('/forma', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        print("Ir saņemts iesniegums!")
        vards = request.form.get('vards')
        epasts = request.form.get('epasts')

        print("Vards:", vards, " Epasts:", epasts)

        persona = Persona(vards=vards, epasts=epasts)

        db.session.add(persona)
        try:
            db.session.commit()
            flash("Lietotājs ir pievienots", category="veiksmigi")
        except exc.IntegrityError:
            flash("Lietotājs ar šādu e-pastu jau eksistē!", category="kluda")
        except exc.SQLAlchemyError as error:
            print(error._message)
            flash("Radās neparedzēta kļūda datubāzē! Mēģiniet vēlāk vai sazinieties ar administrātoru!", category="Kļūda")
        
    return render_template('forma.html')

@app.route('/datubaze')
def datubaze():
    personas = Persona.query.all()
    # Druka DB saturu konsole
    # for persona in personas:
    #     print(persona.vards, persona.epasts)

    return render_template('datubaze.html', personas = personas)

@app.route('/meklet')
def meklet():
    dati = request.args.to_dict()
    epasts = ""
    if 'epasts' in dati:
        epasts = dati['epasts']
        persona = Persona.query.filter_by(epasts=epasts).first()
        if persona:
            flash("Persona ir atrasta", category="veiksmigi")
        else:
            flash("Persona nav atrasta!", category="kluda")
    
    return render_template('meklet.html', epasts = epasts)

@app.route('/persona/dzest/<int:id>')
def dzest(id):
    persona = Persona.query.filter_by(id=id).first()
    if persona:
        db.session.delete(persona)
        db.session.commit()
        flash("Persona ir dzēsta!", category="veiksmigi")
    else:
        flash("Persona ar šādu id neeksistē!", category="kluda")
    return redirect('/datubaze')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=8080)
    