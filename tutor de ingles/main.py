from flask import Flask, jsonify,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
######################################
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import io
import base64


#pip install flask-mysqldb

app = Flask(__name__)
app.secret_key = '1a2b3c4d5e'

# Ingrese los detalles de su conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] ='Martha'
app.config['MYSQL_PASSWORD'] = 'MarthaAngelica12345'
app.config['MYSQL_DB'] = 'logintutor'

# Inicializar MySQL
mysql = MySQL(app)

# http://localhost:5000/tutorIngles/ - esta será la página de inicio de sesión, necesitamos usar solicitudes GET y POST
@app.route('/tutorIngles/', methods=['GET', 'POST'])
def login():
    msg = ''
    # Verificamos si existen solicitudes POST de "nombre de usuario" y "contraseña" (formulario enviado por el usuario)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Verifique si la cuenta existe
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM  cuenta  WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        # Si la cuenta existe en la base de datos
        if account:
            # Creamos datos de sesión, podemos acceder a estos datos en otras rutas
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['pre_test'] = account['pre_test']
            session['post_test'] = account['post_test']            
            # Redirigir a la página de inicio
            return redirect(url_for('home'))
        else:
            # La cuenta no existe o el nombre de usuario / contraseña es incorrecto
            msg = 'Usuario o password incorrectos!'
    return render_template('index.html', msg=msg)


def grafico_variable_fuzzy(fig,rutaImagen):
    img = io.BytesIO()
    fig.savefig(rutaImagen)
    #plt.savefig(rutaImagen, format='png')    
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return 'data:image/png;base64,{}'.format(graph_url)

def ParteDifusa(VADIDF):
        
    sujeto = ctrl.Antecedent(np.arange(0, 6, 1), 'sujeto')
    tiempo_verbal = ctrl.Antecedent(np.arange(0, 6, 1), 'tiempo_verbal')
    adjetivo = ctrl.Antecedent(np.arange(0, 6, 1), 'adjetivo')
    adverbio = ctrl.Antecedent(np.arange(0, 6, 1), 'adverbio')    
    nivelAprendizajeIngles = ctrl.Consequent(np.arange(5, 21, 1), 'nivelAprendizajeIngles')

    sujeto['bajo'] = fuzz.trimf(sujeto.universe, [0, 0, 3])
    sujeto['normal'] = fuzz.trimf(sujeto.universe, [2, 5, 5])
    tiempo_verbal['bajo'] = fuzz.trimf(tiempo_verbal.universe, [0, 0, 3])
    tiempo_verbal['normal'] = fuzz.trimf(tiempo_verbal.universe, [2, 5, 5])
    adjetivo['bajo'] = fuzz.trimf(adjetivo.universe, [0, 0, 3])
    adjetivo['normal'] = fuzz.trimf(adjetivo.universe, [2, 5, 5])    
    adverbio['bajo'] = fuzz.trimf(adverbio.universe, [0, 0, 3])
    adverbio['normal'] = fuzz.trimf(adverbio.universe, [2, 5, 5])
            
    nivelAprendizajeIngles['C'] = fuzz.trimf(nivelAprendizajeIngles.universe, [5, 5, 10])
    nivelAprendizajeIngles['B'] = fuzz.trimf(nivelAprendizajeIngles.universe, [8, 12, 16])
    nivelAprendizajeIngles['A'] = fuzz.trimf(nivelAprendizajeIngles.universe, [14, 16, 17])
    nivelAprendizajeIngles['AD'] = fuzz.trimf(nivelAprendizajeIngles.universe, [16, 20, 20])    

#################################################################################################
    figVisualizacion =ctrl.fuzzyvariable.FuzzyVariableVisualizer(sujeto).view() 
    figAnalisis =ctrl.fuzzyvariable.FuzzyVariableVisualizer(tiempo_verbal).view()       
    figDeduccionInformal =ctrl.fuzzyvariable.FuzzyVariableVisualizer(adjetivo).view()
    figDeduccionFormal =ctrl.fuzzyvariable.FuzzyVariableVisualizer(adverbio).view()
    figNCG =ctrl.fuzzyvariable.FuzzyVariableVisualizer(nivelAprendizajeIngles).view() 
    graph1_url = grafico_variable_fuzzy(figVisualizacion[0],"static/images/fuzzy/sujeto.jpg")    
    graph2_url = grafico_variable_fuzzy(figAnalisis[0],"static/images/fuzzy/tiempo_verbal.jpg")
    graph3_url = grafico_variable_fuzzy(figDeduccionInformal[0],"static/images/fuzzy/adjetivo.jpg")
    graph4_url = grafico_variable_fuzzy(figDeduccionFormal[0],"static/images/fuzzy/adverbio.jpg")
    graph5_url = grafico_variable_fuzzy(figNCG[0],"static/images/fuzzy/nivelAprendizajeIngles.jpg")
    
#################################################################################################
    
    #-------reglas nivelAprendizajeIngles
    rule1 = ctrl.Rule(sujeto['bajo'] & tiempo_verbal['bajo'] & adjetivo['bajo'] & adverbio['bajo'], nivelAprendizajeIngles['C'])
    rule2 = ctrl.Rule(sujeto['bajo'] & tiempo_verbal['bajo'] & adjetivo['bajo'] & adverbio['normal'], nivelAprendizajeIngles['C'])
    rule3 = ctrl.Rule(sujeto['bajo'] & tiempo_verbal['bajo'] & adjetivo['normal'] & adverbio['bajo'], nivelAprendizajeIngles['C'])
    rule4 = ctrl.Rule(sujeto['bajo'] & tiempo_verbal['bajo'] & adjetivo['normal'] & adverbio['normal'], nivelAprendizajeIngles['C'])        
    rule5 = ctrl.Rule(sujeto['bajo'] & tiempo_verbal['normal'] & adjetivo['bajo'] & adverbio['bajo'], nivelAprendizajeIngles['C'])
    rule6 = ctrl.Rule(sujeto['bajo'] & tiempo_verbal['normal'] & adjetivo['bajo'] & adverbio['normal'], nivelAprendizajeIngles['C'])
    rule7 = ctrl.Rule(sujeto['bajo'] & tiempo_verbal['normal'] & adjetivo['normal'] & adverbio['bajo'], nivelAprendizajeIngles['C'])   
    rule8 = ctrl.Rule(sujeto['bajo'] & tiempo_verbal['normal'] & adjetivo['normal'] & adverbio['normal'], nivelAprendizajeIngles['C'])
    rule9 = ctrl.Rule(sujeto['normal'] & tiempo_verbal['bajo'] & adjetivo['bajo'] & adverbio['bajo'], nivelAprendizajeIngles['B'])
    rule10 = ctrl.Rule(sujeto['normal'] & tiempo_verbal['bajo'] & adjetivo['bajo'] & adverbio['normal'], nivelAprendizajeIngles['B'])
    rule11 = ctrl.Rule(sujeto['normal'] & tiempo_verbal['bajo'] & adjetivo['normal'] & adverbio['bajo'], nivelAprendizajeIngles['B'])
    rule12 = ctrl.Rule(sujeto['normal'] & tiempo_verbal['bajo'] & adjetivo['normal'] & adverbio['normal'], nivelAprendizajeIngles['B'])
    rule13 = ctrl.Rule(sujeto['normal'] & tiempo_verbal['normal'] & adjetivo['bajo'] & adverbio['bajo'], nivelAprendizajeIngles['B'])
    rule14 = ctrl.Rule(sujeto['normal'] & tiempo_verbal['normal'] & adjetivo['bajo'] & adverbio['normal'], nivelAprendizajeIngles['A'])
    rule15 = ctrl.Rule(sujeto['normal'] & tiempo_verbal['normal'] & adjetivo['normal'] & adverbio['bajo'], nivelAprendizajeIngles['A'])
    rule16 = ctrl.Rule(sujeto['normal'] & tiempo_verbal['normal'] & adjetivo['normal'] & adverbio['normal'], nivelAprendizajeIngles['AD'])
    
    acc_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
                                    rule11, rule12, rule13, rule14, rule15, rule16])
    
    acc = ctrl.ControlSystemSimulation(acc_ctrl)
    
    
    #entradas al sistema
    acc.input['sujeto'] = VADIDF[0]
    acc.input['tiempo_verbal'] = VADIDF[1]
    acc.input['adjetivo'] = VADIDF[2]
    acc.input['adverbio'] = VADIDF[3]    
    acc.compute()
    nivel_competencia = acc.output['nivelAprendizajeIngles']
    print("nivel de Aprendizaje en Ingles: ",nivel_competencia)  
   
    figNCG2 =ctrl.fuzzyvariable.FuzzyVariableVisualizer(nivelAprendizajeIngles).view(sim=acc)    
    graph6_url = grafico_variable_fuzzy(figNCG2[0],"static/images/fuzzy/nivelAprendizajeIngles.jpg")        
    return nivel_competencia



@app.route('/pre_diagnostico')
def pre_diagnostico():

    if 'loggedin' in session:    
        #a = request.args.get('a', 0, type=int)
        #b = request.args.get('b', 0, type=int)
        respuestas = [1,0,0,1,0,0,2,0,0,1]        
        selections = request.args.get('selections')
        print ("respuestas: ",respuestas)
        selections=selections.strip('[]')
        res = selections.split(',')
        i=0
        numCorrect = 0
        print ("res:",res)
        for elem in res: 
            print(respuestas[i] ," - ", elem)
            if respuestas[i] == int(elem):
                numCorrect=numCorrect+2
            i=i+1 
        
        print ("numCorrect: ",numCorrect)
        if(numCorrect<12):
            msg= 'El estudiante inicia con un nivel C en Inglés.'
        elif(numCorrect<14):
            msg= 'El estudiante inicia con un nivel B en Inglés.'
        elif(numCorrect<17):
            msg= 'El estudiante inicia con un nivel A en Inglés.'        
        else:
            msg= 'El estudiante inicia con un nivel AD en Inglés. '        
                                
        msg+= ' -->Y posee un puntaje en el test de: '+ str(numCorrect)                                             
        msg+= "<br><br> Se le recomienda ver los siguientes videos de Abjetivos:"
        msg+= "<br><br>&nbsp; &nbsp; &nbsp; &nbsp;<iframe width='450' height='300' src='https://www.youtube.com/embed/l0Xtt9WpHVY' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>"
        msg+= "&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; <iframe width='450' height='300' src='https://www.youtube.com/embed/LsP_goPklng' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>"
        id_logged=session['id']
        pre_test=int(numCorrect)
        #pre_test=pre_test+1
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE cuenta SET pre_test = %s WHERE id = %s', (pre_test, id_logged))      
        mysql.connection.commit()
        return jsonify(result=msg)
    return redirect(url_for('login'))   

######################################################################    
@app.route('/post_diagnostico')
def post_diagnostico():

    if 'loggedin' in session:    
        #a = request.args.get('a', 0, type=int)
        #b = request.args.get('b', 0, type=int)
        respuestas =        [2,0,1,0,2,0,2,2,1,2,2,0,1,0,1,1,0,0,1,2]   #1 punto     
        medias_respuestas = [1,2,2,1,2,1,1,0,2,1,1,1,2,1,2,0,1,1,0,1]   #0.5 puntos
        VADIDF = [0,0,0,0]
        selections = request.args.get('selections')
        print ("respuestas: ",respuestas)
        selections=selections.strip('[]')
        res = selections.split(',')
        i=0
        print ("res:",res)
        for elem in res: 
            #print(respuestas[i] ," - ", elem)
            pos=i%4
        
            if respuestas[i] == int(elem):
                VADIDF[pos]+=1
            else:
                if medias_respuestas[i] == int(elem):
                    VADIDF[pos]+=0.5
                else:
                    VADIDF[pos]+=0.25            
            i=i+1
        print ("VADIDF: ",VADIDF) 


        nivel_competencia = ParteDifusa(VADIDF)
        nivel_competencia = round(nivel_competencia,2)

  
        if(nivel_competencia>16):
            msg= 'El estudiante ya se encuentra con un nivel AVANZADO en inglés!'            
            msg+= ' --> Y tiene una nota en el post test de: '+ str(nivel_competencia)                                      

        else:
            msg= 'El estudiante tiene una nota de '+ str(nivel_competencia)

                                           
        msg+= "<br><br> Se le recomienda ver los siguientes videos:"
        msg+= "<br><br>&nbsp; &nbsp; &nbsp; &nbsp; <iframe width='450' height='300' src='https://www.youtube.com/embed/CqujZ4YEH80' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>"
        msg+= "&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; <iframe width='450' height='300' src='https://www.youtube.com/embed/qf9eyVU8xKo' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>"

        
        id_logged=session['id']
        post_test=int(nivel_competencia)
        nota_test=nivel_competencia
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE cuenta SET post_test = %s WHERE id = %s', (post_test, id_logged))      
        mysql.connection.commit()        
        cursor.execute('INSERT INTO examen VALUES (%s, %s)', [id_logged,nota_test])
        mysql.connection.commit()        
        return jsonify(result=msg)
    return redirect(url_for('login'))   


#######################################################################


# http://localhost:5000/pythinlogin/home - esta será la página de inicio, solo accesible para usuarios registrados
@app.route('/tutorIngles/home')
def home():
    # Comprueba si el usuario está conectado
    if 'loggedin' in session:
        # El usuario ha iniciado sesión, mostrarle la página de inicio
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuenta WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        menuInicio="active"
        return render_template('home.html', menuInicio=menuInicio, username=account['username'], pre_test=account['pre_test'], post_test=account['post_test'])
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
    return redirect(url_for('login'))    

@app.route('/tutorIngles/progreso')
def progreso():
    # Comprueba si el usuario está conectado
    if 'loggedin' in session:
        # El usuario ha iniciado sesión, mostrarle la página de inicio
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuenta WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM examen WHERE id = %s', (session['id'],))
        ListaNotas = cursor.fetchall() 
        print (ListaNotas)
        menuProgreso="active"
        return render_template('progreso.html',  menuProgreso=menuProgreso,account=account,ListaNotas=ListaNotas)
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
    return redirect(url_for('login'))   

@app.route('/tutorIngles/temas')
def temas():
    # Comprueba si el usuario está conectado
    if 'loggedin' in session:
        # El usuario ha iniciado sesión, mostrarle la página de inicio
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuenta WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        menuRevisar="active"
        return render_template('temas.html', menuRevisar=menuRevisar, account=account)
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
    return redirect(url_for('login'))  



@app.route('/tutorIngles/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('pre_test', None)
    session.pop('post_test', None)    
    
    print("Te desconectaste con exito!!")
    return redirect(url_for('login'))

@app.route('/tutorIngles/quiz')
def quiz():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuenta WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        pre_test=account['pre_test']
        pre_test=int(pre_test)
        print ("quiz pre_test: ", pre_test)
        if pre_test == -1:            
            return render_template('quiz.html',username=session['username'])
        else:
            return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/tutorIngles/quiz_pos')
def quiz_pos():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuenta WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        post_test=account['post_test']
        post_test=int(post_test)
        if post_test <= 16:            
            return render_template('quiz_pos.html',username=session['username'])
        else:
            return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/')
def raiz():
    return redirect(url_for('login'))
    


if __name__ =='__main__':
	app.run()
