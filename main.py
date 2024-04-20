from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS, cross_origin

import os.path
import json
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime


BASE_PATH = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
version = "v1"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userInfo.db'
#app.config['SQLALCHEMY_BIND'] = {'publication' : 'sqlite:///publication.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['UPLOAD_FOLDER'] = './img'
db = SQLAlchemy(app) 
app.app_context().push()


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text, nullable=True) # логин
    password = db.Column(db.Text, nullable=True) # пароль
    typeuser = db.Column(db.Text, nullable=True) # вуз/предприятие/студент
    geovuz = db.Column(db.Text, nullable=True) #адрес вуза
    photoprof = db.Column(db.Text, default='/src/assets/no_photo.jpg') # фото профиля
    nameprof = db.Column(db.Text, nullable=True) #имя пользователя
    surnameprof = db.Column(db.Text, nullable=True) #фамилия пользователя
    taskprof = db.Column(db.Text, nullable=True) #описание профиля
    vuzuser = db.Column(db.Text, nullable=True) #вуз пользователя
    fakprof = db.Column(db.Text, nullable=True) #факультет пользователя
    kafprof = db.Column(db.Text, nullable=True) #кафедра пользователя
    userfak = db.Column(db.Text, nullable=True) #факультет пользователя
    userkaf = db.Column(db.Text, nullable=True) #факультет пользователя
    potprof = db.Column(db.Text, nullable=True) #поток пользователя
    grupprof = db.Column(db.Text, nullable=True) #группа пользователя
    ratingprof = db.Column(db.Text, nullable=True) #рейтинг пользователя
    zvezdprof = db.Column(db.Text, nullable=True) #звезды пользователя
    dostnauk = db.Column(db.Text, nullable=True) #достижения наука пользователя
    dostsport = db.Column(db.Text, nullable=True) #достижения спорта пользователя
    dosttvor = db.Column(db.Text, nullable=True) #достижения творчество пользователя
    dostvol = db.Column(db.Text, nullable=True) #достижения волонтерства пользователя
    userid = db.Column(db.Text, nullable=True) #для публикации
    publicationdescription = db.Column(db.Text, nullable=True) #описание публикаций
    publicationpphoto = db.Column(db.Text, nullable=True)#фото публикаций

# class Publication(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     idUser = db.Column(db.Text, nullable=True) # id пользователя



@app.route(f'/{version}/login', methods=['POST', 'GET'])
def login() -> json:
    result = {}
    data = request.get_json()
    login = str(data['params']['login']) 
    password = str(data['params']['password']) 
    onlyData = Data.query.all()

    for el in onlyData:
        if login == str(el.login) and password == str(el.password):
            result['id'] = str(el.id)           
            result['photoprof'] = str(el.photoprof)  # фото профиля
            result['nameprof'] = str(el.nameprof)  #имя пользователя
            result['surnameprof'] = str(el.surnameprof) #фамилия пользователя
            result['vuzuser'] = str(el.vuzuser) # вуз пользователя
            result['taskprof'] = str(el.taskprof) #описание
            result['fakprof'] = str(el.fakprof) #факультет пользователя
            result['kafprof'] = str(el.kafprof)#кафедра пользователя
            result['potprof'] = str(el.potprof) #поток пользователя
            result['grupprof'] = str(el.grupprof) #группа пользователя
            result['ratingprof'] = str(el.ratingprof) #рейтинг пользователя
            result['zvezdprof'] = str(el.zvezdprof) #звезды пользователя
            result['dostnauk'] = str(el.dostnauk) #достижения наука пользователя
            result['dostsport'] = str(el.dostsport)  #достижения спорта пользователя
            result['dosttvor'] = str(el.dosttvor) #достижения творчество пользователя
            result['dostvol'] = str(el.dostvol) #достижения волонтерства пользователя
            result['publicationdescription'] = str(el.publicationdescription)  #данные публикаций 
            result['publicationpphoto'] = str(el.publicationpphoto) 
            result['status'] = '200'
            result['message'] = 'Успешно'
            return jsonify(result)
        
    result['message'] = "Не найден пользователь"
    result['status'] = '400'
    return jsonify(result)    

@app.route(f'/{version}/registration-prof', methods=['POST', 'GET'])
def registrationprof() -> json:
    result = {}
    data = request.get_json()
    login = str(data['params']['login']) 
    password = str(data['params']['password']) 
    nameprof = str(data['params']['nameprof']) 
    surnameprof = str(data['params']['surnameprof']) 

    onlyData = Data.query.all()
    for el in onlyData:
        if login == str(el.login):
            result['message'] = "Уже существует!"
            result['status'] = '400'

            return jsonify(result)
        
    dataSet = Data(login=login, password=password, nameprof=nameprof, surnameprof=surnameprof)
    db.session.add(dataSet)
    db.session.commit()
    result['status'] = '200'
    result['message'] = 'Успешно'
    result['id'] = str(dataSet.id)

    return result

@app.route(f'/{version}/registration-vuz', methods=['POST', 'GET'])
def registrationvuz() -> json:
    data = request.get_json()
    nameprof = str(data['params']['nameprof']) 
    typeuser = 'вуз'
    fakprof = str(data['params']['fakprof'])
    geovuz = str(data['params']['geovuz'])
    id = str(data['params']['id'])
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            el.nameprof = nameprof
            el.typeuser=typeuser
            el.fakprof=fakprof
            el.geovuz=geovuz
            db.session.commit()
            result = {}
            result['status'] = '200'
            result['message'] = 'Успешно'
            return jsonify(result)
    # dataSet = Data(nameprof=nameprof, typeuser=typeuser, fakprof=fakprof, geovuz=geovuz)
    # db.session.add(dataSet)
    # db.session.commit()
    result = {}
    result['status'] = '400'
    result['message'] = 'Ошибка в создании вуза'
    #result['id'] = str(dataSet.id)
    return jsonify(result)

    

@app.route(f'/{version}/registration-profvuz', methods=['POST', 'GET'])
def registrationprofvuz() -> json:
    result = {}
    data = request.get_json()
    login = str(data['params']['login']) 
    password = str(data['params']['password']) 
    nameprof = str(data['params']['nameprof']) 
    surnameprof = str(data['params']['surnameprof']) 
    typeuser = 'создатель вуза'

    onlyData = Data.query.all()
    for el in onlyData:
        if login == str(el.login):
            result['message'] = "Уже существует!"
            result['status'] = '400'
            return jsonify(result)
        
    dataSet = Data(login=login, password=password, nameprof=nameprof, surnameprof=surnameprof, typeuser=typeuser)
    db.session.add(dataSet)
    db.session.commit()
    result['status'] = '200'
    result['message'] = 'Успешно'

    return jsonify(result)

@app.route(f'/{version}/info-profile', methods=['POST', 'GET'])
def infoprof() -> json:
    result = {}
    data = request.get_json()
    id = str(data['params']['id']) 
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            result['id'] = str(el.id)           
            result['photoprof'] = str(el.photoprof)  # фото профиля
            result['nameprof'] = str(el.nameprof)  #имя пользователя
            result['surnameprof'] = str(el.surnameprof) #фамилия пользователя
            result['taskprof'] = str(el.taskprof) #описание
            result['vuzuser'] = str(el.vuzuser) # вуз пользователя
            result['fakprof'] = str(el.fakprof) #факультет пользователя
            result['kafprof'] = str(el.kafprof)#кафедра пользователя
            result['userfak'] = str(el.userfak)#кафедра пользователя
            result['userkaf'] = str(el.userkaf)#кафедра пользователя
            result['potprof'] = str(el.potprof) #поток пользователя
            result['grupprof'] = str(el.grupprof) #группа пользователя
            result['ratingprof'] = str(el.ratingprof) #рейтинг пользователя
            result['zvezdprof'] = str(el.zvezdprof) #звезды пользователя
            result['dostnauk'] = str(el.dostnauk) #достижения наука пользователя
            result['dostsport'] = str(el.dostsport)  #достижения спорта пользователя
            result['dosttvor'] = str(el.dosttvor) #достижения творчество пользователя
            result['dostvol'] = str(el.dostvol) #достижения волонтерства пользователя
            result['publicationdescription'] = str(el.publicationdescription)  #данные публикаций 
            result['publicationpphoto'] = str(el.publicationpphoto) 
            result['status'] = '200'
            result['message'] = 'Успешно'
            return jsonify(result)
        
    result['message'] = "Не найден пользователь"
    result['status'] = '400'
    return jsonify(result) 

@app.route(f'/{version}/upload', methods=['POST', 'GET'])
def upload():
    result = {}
    id = request.form.get('id')
    if not id:
        files = request.files.getlist('files') #request.files['file']
        print(files)
        #filesName = ''
        filesName = []
        for file in files:
            if file:
                fileName = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
                fileName = f"{fileName}.jpeg"
                file.save(os.path.join('public/assets', fileName))
                #filesName += fileName
                filesName.append(fileName)

        dataSet = Data(photoprof=str(filesName))
        db.session.add(dataSet)
        db.session.commit()

        result['status'] = '200'
        result['message'] = 'Успешно'
        result['id'] = str(dataSet.id)

        return result
    else: 
        result = {}
        id = request.form.get('id')
        print(id)
        onlyData = Data.query.all()
        files = request.files.getlist('files')
        for el in onlyData:
            if id == str(el.id):
                filesName = []
                for file in files:
                    if file:
                        fileName = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
                        fileName = f"{fileName}.jpeg"
                        file.save(os.path.join('public/assets', fileName))
                        #filesName += fileName
                        filesName.append(fileName)
                        el.photoprof = str(filesName)
                        db.session.commit()
                        result['status'] = '200'
                        result['message'] = 'Успешно'
                        return result

@app.route(f'/{version}/new-entry', methods=['POST', 'GET'])
def newEntry():
    result = {}
    userid = request.form.get('userID')
    desc = request.form.get('desc')

    onlyData = Data.query.all()
    for el in onlyData:
        if id == str(el.id):
            file = request.files.getlist('files')
            data = request.get_json()
            description = str(data['params']['description']) 
            print(file)
            entryData = el.publicationdata
            if file:
                fileName = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f') + '.jpeg'
                file.save(os.path.join('dist/img/entry', fileName))
                entryData[f'{fileName}'] = description
                dataSet = Data(publicationdata=str(entryData))
                db.session.add(dataSet)
                db.session.commit()

                result['status'] = '200'
                result['message'] = 'Успешно'

                return result
            
            else:
                result['message'] = "Добавьте фото!"
                result['status'] = '400'
                return jsonify(result)

@app.route(f'/{version}/save_desk', methods=['POST', 'GET'])
def saveDesk():
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    desc = str(data['params']['desc'])
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            dataSet = Data(taskprof=str(desc))
            db.session.add(dataSet)
            db.session.commit()
            result['message'] = "Успешно"
            result['status'] = '200'
            return jsonify(result)

    result['message'] = "Пользователь не найден!"
    result['status'] = '400'
    return jsonify(result)

@app.route(f'/{version}/set_vuz', methods=['POST', 'GET'])
def steVuz():
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    vuz = str(data['params']['vuz'])
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            el.vuzuser = str(vuz)
            db.session.commit()
            result['message'] = "Успешно"
            result['status'] = '200'
            return jsonify(result)

    result['message'] = "Пользователь не найден!"
    result['status'] = '400'
    return jsonify(result)

@app.route(f'/{version}/set_fak', methods=['POST', 'GET'])
def steFak():
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    fak = str(data['params']['fak'])
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            el.userfak = str(fak)
            db.session.commit()
            result['message'] = "Успешно"
            result['status'] = '200'
            return jsonify(result)

    result['message'] = "Пользователь не найден!"
    result['status'] = '400'
    return jsonify(result)

@app.route(f'/{version}/set_kaf', methods=['POST', 'GET'])
def steKaf():
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    kaf = str(data['params']['kaf'])
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            el.userfak = str(kaf)
            db.session.commit()
            result['message'] = "Успешно"
            result['status'] = '200'
            return jsonify(result)

    result['message'] = "Пользователь не найден!"
    result['status'] = '400'
    return jsonify(result)


@app.route(f'/{version}/get_vuzs', methods=['POST', 'GET'])
def getVuzs():
    result = {}
    onlyData = Data.query.all()
    allvuzs = []

    for el in onlyData:
        if str(el.typeuser) == 'вуз':
            namevuz = str(el.nameprof)
            allvuzs.append(namevuz)

    result['vuzs'] = str(allvuzs)
    return jsonify(result)

@app.route(f'/{version}/get_vuz', methods=['POST', 'GET'])
def getVuz():
    result = {}
    data = request.get_json()
    namevuz = str(data['params']['namevuz'])
    onlyData = Data.query.all()


    for el in onlyData:
        if namevuz == str(el.nameprof):
            result['namevuz'] = str(el.nameprof)
            result['fakultet'] = str(el.fakprof)
            result['geovuz'] = str(el.geovuz)
            result['photoprof'] = str(el.photoprof)
            return jsonify(result)
        
    result['message'] = "Вуз не найден!"
    result['status'] = '400'
    return jsonify(result)    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5010)# port=5010,