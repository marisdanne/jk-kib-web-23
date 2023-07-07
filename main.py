from flask import Flask, render_template, request

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True, port=8080)