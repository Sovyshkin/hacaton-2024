from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS, cross_origin

import os.path
import json
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import ast


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
    taskprof = db.Column(db.Text, default='') #описание профиля
    vuzuser = db.Column(db.Text, nullable=True) #вуз пользователя
    fakprof = db.Column(db.Text, nullable=True) #факультет пользователя
    kafprof = db.Column(db.Text, nullable=True) #кафедра пользователя
    userfak = db.Column(db.Text, nullable=True) #факультет пользователя
    userkaf = db.Column(db.Text, nullable=True) #факультет пользователя
    potprof = db.Column(db.Text, nullable=True) #поток пользователя
    grupprof = db.Column(db.Text, nullable=True) #группа пользователя
    ratingprof = db.Column(db.Text, nullable=True) #рейтинг пользователя
    zvezdprof = db.Column(db.Text, default='0') #звезды пользователя
    dostnauk = db.Column(db.Text, default='0') #достижения наука пользователя
    dostsport = db.Column(db.Text, default='0') #достижения спорта пользователя
    dosttvor = db.Column(db.Text, default='0') #достижения творчество пользователя
    dostvol = db.Column(db.Text, default='0') #достижения волонтерства пользователя
    userid = db.Column(db.Text, nullable=True) #для публикации
    publicationdescription = db.Column(db.Text, nullable=True) #описание публикаций
    publicationhash = db.Column(db.Text, nullable=True) #описание публикаций
    publicationphoto = db.Column(db.Text, nullable=True)#фото публикаций
    likes = db.Column(db.Text, default='0')#лайки публикаций
    koments = db.Column(db.Text, default='[]')#коменты публикаций
    nameevent = db.Column(db.Text, nullable=True)#название мероприятия
    typeevent = db.Column(db.Text, nullable=True)#тип мероприятия
    place = db.Column(db.Text, nullable=True)#место мероприятия
    date = db.Column(db.Text, nullable=True)#дата мероприятия
    vuzid = db.Column(db.Text, nullable=True)#для мероприятия
    eventreq = db.Column(db.Text, default='[]')#запрос для мероприятия
    eventmems = db.Column(db.Text, default='[]')#участники мероприятия
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
            result['likes'] = str(el.likes)  #лайки

            result['publicationphoto'] = str(el.publicationphoto) 
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
    
    dostnauk = '0'
    dostsport= '0'
    dosttvor = '0'
    dostvol= '0'
    zvezda = int(dostnauk) + int(dostsport) + int(dosttvor) + int(dostvol)
    onlyData = Data.query.all()
    for el in onlyData:
        if login == str(el.login):
            result['message'] = "Уже существует!"
            result['status'] = '400'

            return jsonify(result)
       
    dataSet = Data(login=login, password=password, nameprof=nameprof, surnameprof=surnameprof, zvezdprof=zvezda, dostvol=dostvol, dosttvor=dosttvor, dostsport=dostsport, dostnauk=dostnauk)
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
    userid = str(data['params']['userid'])
    print(userid)
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            el.nameprof = nameprof
            el.typeuser=typeuser
            el.fakprof=fakprof
            el.geovuz=geovuz
            el.userid=userid
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
            result['id'] = el.id
            result['message'] = "Уже существует!"
            result['status'] = '400'
            return jsonify(result)
        
    dataSet = Data(login=login, password=password, nameprof=nameprof, surnameprof=surnameprof, typeuser=typeuser)
    db.session.add(dataSet)
    db.session.commit()
    result['id'] = str(dataSet.id)
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
            result['publicationphoto'] = str(el.publicationphoto) 
            result['likes'] = str(el.likes)  #лайки
            result['status'] = '200'
            result['message'] = 'Успешно'
            result['typeuser'] = str(el.typeuser)
            print(result)
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
    userid = request.form.get('userid')
    desc = request.form.get('desc')
    hash = request.form.get('hash')
    files = request.files.getlist('files')
    for file in files:
        if file:
            fileName = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            fileName = f"{fileName}.jpeg"
            file.save(os.path.join('public/assets', fileName))
            dataSet = Data(publicationhash=str(hash), publicationdescription=str(desc), userid=str(userid), publicationphoto=str(fileName))
            db.session.add(dataSet)
            db.session.commit()

            result['status'] = '200'
            result['message'] = 'Успешно'

            return result
        
        else:
            result['message'] = "Добавьте фото!"
            result['status'] = '400'
            return jsonify(result)
    result['message'] = "Ошибка"
    result['status'] = '400'
    return jsonify(result)


@app.route(f'/{version}/get_news', methods=['POST', 'GET'])
def getNews():
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    onlyData = Data.query.all()
    lst = []

    for el in onlyData:
        if id == str(el.userid) and el.typeuser != 'вуз' and el.typeuser != 'создатель вуза':
            lst.append({ "img": el.publicationphoto, "desc": el.publicationdescription, "hash": el.publicationhash, "userid": el.userid, "id": el.id })
    
    result["news"] = str(lst)
    print(lst)
    return jsonify(result)    


@app.route(f'/{version}/get_entry', methods=['POST', 'GET'])
def getEntry():
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            result["img"] = el.publicationphoto
            result["desc"] = el.publicationdescription
            result["hash"] = el.publicationhash
            result["comments"] = el.koments
            result["likes"] = el.likes
            result["userid"] = el.userid
            return jsonify(result)
    
    result['status'] = '400'
    result['message'] = 'Запись не найдена'
    return jsonify(result)    

@app.route(f'/{version}/save_desc', methods=['POST', 'GET'])
def saveDesk():
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    desc = str(data['params']['desc'])
    onlyData = Data.query.all()

    for el in onlyData:
        if id == str(el.id):
            el.taskprof = desc
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
    if namevuz == 'False':
        namevuz = False
    id = str(data['params']['id'])
    if id == 'False':
        id = False
    userid = str(data['params']['userid'])
    if userid == 'False':
        userid = False
    print(namevuz, id, userid)
    onlyData = Data.query.all()
    if id:
        for el in onlyData:
            if id == str(el.id):
                result['namevuz'] = str(el.nameprof)
                result['taskprof'] = str(el.taskprof)
                result['geovuz'] = str(el.geovuz)
                result['photoprof'] = str(el.photoprof)
                result['typeevent'] = str(el.typeevent)
                result['place'] = str(el.place)
                result['date'] = str(el.date)
                result['vuzid'] = str(el.vuzid)
                return jsonify(result)
            
        result['message'] = "Вуз не найден!"
        result['status'] = '400'
        return jsonify(result)
    elif userid:
        for el in onlyData:
            if str(userid) == str(el.userid):
                print(el.id)
                result['id'] = str(el.id)
                return jsonify(result)
                
        result['message'] = "Вуз не найден!"
        result['status'] = '400'
        return jsonify(result)
    else:
        print('name')
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

@app.route(f'/{version}/publish_event', methods=['POST', 'GET']) 
def ublishEvent(): 
    result = {} 
    userid = request.form.get('userid') 
    desc = request.form.get('desc') 
    vuzid = request.form.get('vuzid') 
    name = request.form.get('name') 
    place = request.form.get('place') 
    typeevent = request.form.get('typeevent') 
    date = request.form.get('date') 
    files = request.files.getlist('files') 
    if files: 
        filesName = []
        for file in files:
            if file:
                fileName = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
                fileName = f"{fileName}.jpeg"
                file.save(os.path.join('public/assets', fileName))
                #filesName += fileName
                filesName.append(fileName)
        dataSet = Data(vuzid = str(vuzid), nameevent = str(name), place = str(place), typeevent = str(typeevent), date = str(date), taskprof = str(desc), photoprof = str(filesName)) 
        db.session.add(dataSet) 
        db.session.commit() 

        result['status'] = '200' 
        result['message'] = 'Успешно' 

        return result 
        
    else: 
        result['message'] = "Добавьте фото!" 
        result['status'] = '400' 
        return jsonify(result)

@app.route(f'/{version}/get_events', methods=['POST', 'GET'])
def getEvents() -> json:
    result = {}
    data = request.get_json()
    vuzid = str(data['params']['vuzid']) 
    onlyData = Data.query.all()
    allevents = []

    for el in onlyData:
        if vuzid == str(el.vuzid):
            allevents.append({"id": el.id, "name": el.nameevent, "typeevent": el.typeevent, "place": el.place, "date": el.date, "vuzid": el.vuzid, "taskprof": el.taskprof, "photoprof": ast.literal_eval(el.photoprof), 'mems': ast.literal_eval(el.eventmems), 'reqs': ast.literal_eval(el.eventreq)})
    
    result['events'] = str(allevents)
    return jsonify(result)


@app.route(f'/{version}/get_event', methods=['POST', 'GET'])
def getEvent() -> json:
    result = {}
    data = request.get_json()
    idevent = str(data['params']['id']) 
    onlyData = Data.query.all()


    for el in onlyData:
        if idevent == str(el.id):
            event = el
 
    result['id'] = str(event.id)
    result['img'] = str(event.photoprof)
    result['desc'] = str(event.taskprof)
    result['name'] = str(event.nameevent)
    result['date'] = str(event.date)
    result['type'] = str(event.typeevent)
    result['place'] = str(event.place)
    result['reqs'] = str(event.eventreq)
    result['mems'] = str(event.eventmems)
    return jsonify(result)


@app.route(f'/{version}/set_like', methods=['POST', 'GET'])
def setLike() -> json:
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])

    onlyData = Data.query.all()
    for el in onlyData:
        if id == str(el.id):
            likes = int(el.likes)
            likes += 1
            el.likes = str(likes)
            db.session.commit()
            result['status'] = '200' 
            result['message'] = 'Успешно' 
            return result 
        
    result['message'] = "Запись не найдена!" 
    result['status'] = '400' 
    return jsonify(result)

    
@app.route(f'/{version}/get_like', methods=['POST', 'GET'])
def getLike() -> json:
    result = {}
    data = request.get_json()
    idZap = str(data['params']['userid']) 

    onlyData = Data.query.all()
    for el in onlyData:
        if idZap == str(el.userid):
            likes = str(el.likes)
            result['likes'] = likes 
            return result 
        

    result['message'] = "Запись не найдена!" 
    result['status'] = '400' 
    return jsonify(result)


@app.route(f'/{version}/set_koment', methods=['POST', 'GET'])
def setKoment() -> json:
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    name = str(data['params']['name']) 
    surname = str(data['params']['surname']) 
    img = str(data['params']['img'])
    text = str(data['params']['text']) 
    userid = str(data['params']['userid']) 
    if img:
        img = img[2:-2]

    onlyData = Data.query.all()
    for el in onlyData:
        if id == str(el.id):
            koments = f"{el.koments}"
            koments = ast.literal_eval(koments)
            koments.append({"name": name, "text": text, "surname": surname, "img": img, "userid": userid})
            el.koments = str(koments)
            db.session.commit()
            result['status'] = '200' 
            result['message'] = 'Успешно' 
            return jsonify(result) 
        

    result['message'] = "Запись не найдена!" 
    result['status'] = '400' 
    return jsonify(result)


@app.route(f'/{version}/get_koment', methods=['POST', 'GET'])
def getKoment() -> json:
    result = {}
    data = request.get_json()
    id = str(data['params']['id'])
    onlyData = Data.query.all()
    for el in onlyData:
        if id == str(el.id):
            koments = str(el.koments)
            result['koments'] = koments 
            return jsonify(result) 
        

    result['message'] = "Запись не найдена!" 
    result['status'] = '400' 
    return jsonify(result)



# @app.route(f'/{version}/set_dostig', methods=['POST', 'GET'])
# def setDostig() -> json:
#     result = {}
#     data = request.get_json()
#     userid = str(data['params']['userid'])
#     typeevent = str(data['params']['typeevent'])

#     onlyData = Data.query.all()

#     for el in onlyData:
#         if userid == str(el.id):

#             if typeevent == 'dostnauk':
#                 dostnauk = int(el.dostnauk)
#                 dostnauk += 10
#                 el.dostnauk = str(dostnauk)
#                 db.session.commit()
#                 result['status'] = '200' 
#                 result['message'] = 'Успешно' 
#                 return result

#             if typeevent == 'dostsport':
#                 dostsport = int(el.dostsport)
#                 dostsport += 10
#                 el.dostsport = str(dostsport)
#                 db.session.commit()
#                 result['status'] = '200' 
#                 result['message'] = 'Успешно' 
#                 return result

#             if typeevent == 'dosttvor':
#                 dosttvor = int(el.dosttvor)
#                 dosttvor += 10
#                 el.dosttvor = str(dosttvor)
#                 db.session.commit()
#                 result['status'] = '200' 
#                 result['message'] = 'Успешно' 
#                 return result

#             if typeevent == 'dostvol':  
#                 dostvol = int(el.dostvol)
#                 dostvol += 10
#                 el.dostvol = str(dostvol)
#                 db.session.commit()
#                 result['status'] = '200' 
#                 result['message'] = 'Успешно' 
#                 return result

#             else:
#                 result['message'] = "Тип мероприятия не найден!" 
#                 result['status'] = '400' 
#                 return jsonify(result)
        

#     result['message'] = "Пользователь не найден!" 
#     result['status'] = '400' 
#     return jsonify(result)


@app.route(f'/{version}/get_top', methods=['POST', 'GET'])
def getTop() -> json:
    result = {}
    counter = 0

    onlyData = Data.query.all()
    for el in onlyData:
        dostnauk = int(str(el.dostnauk)) 
        dostsport= int(str(el.dostsport))
        dosttvor = int(str(el.dosttvor))
        dostvol= int(str(el.dostvol))
        zvezdprof = int(dostnauk) + int(dostsport) + int(dosttvor) + int(dostvol)
        el.zvezdprof = str(zvezdprof)
        db.session.commit()

    onlyData = Data.query.order_by(Data.zvezdprof).all()
    usersTop = [] 

    for el in onlyData:
        if counter < 5 and str(el.typeuser) != 'вуз' and str(el.typeuser) != 'создатель вуза':
            src = ''
            namevuz = ''
            name = ''
            surname = ''
            if el.photoprof:
                src = el.photoprof[2:-2]
            else:
                src = 'no_photo.png'
            if el.vuzuser:
                namevuz = el.vuzuser
            if el.nameprof:
                name = el.nameprof
            if el.surnameprof:
                surname = el.surnameprof


            usersTop.append({ "name": name, "surname": surname, "photoprof": src, "id": el.id, "zvezd": el.zvezdprof, "vuzuser": namevuz })
            counter += 1
        if counter > 5:
            break 
    result['topusers'] = str(usersTop)
    return result

@app.route(f'/{version}/create_req', methods=['POST', 'GET'])
def createRreq() -> json:
    result = {}
    data = request.get_json()
    userid = str(data['params']['userid']) 
    eventid = str(data['params']['eventid']) 
    all_eventreq = []

    onlyData = Data.query.all()
    for el in onlyData:
        if eventid == str(el.id):
            all = f"{el.eventreq}"
            all = ast.literal_eval(all)
            all.append(userid)
            el.eventreq = str(all)
            db.session.commit()
            result['status'] = '200' 
            result['message'] = 'Успешно' 
            return result

    result['message'] = "Запись не найдена!" 
    result['status'] = '400' 
    return jsonify(result)

@app.route(f'/{version}/set_mems', methods=['POST', 'GET'])
def setMems() -> json:
    result = {}
    data = request.get_json()
    userid = str(data['params']['userid']) 
    eventid = str(data['params']['eventid']) 
    confirm = str(data['params']['confirm'])
    typeevent = str(data['params']['typeevent'])
    all_eventreq = []

    if confirm == 'True':
        onlyData = Data.query.all()
        for el in onlyData:
            if eventid == str(el.id):
                all = f"{el.eventreq}"
                all = ast.literal_eval(all)
                #all.append(userid)
                all.remove(userid)
                el.eventreq = str(all)

                all_mems = f"{el.eventmems}"
                all_mems = ast.literal_eval(all_mems)
                all_mems.append(userid)
                el.eventmems = str(all)

                db.session.commit()
                # result['status'] = '200' 
                # result['message'] = 'Успешно' 
                # return result

        for el in onlyData:
            if userid == str(el.id):
                if typeevent == 'Наука':
                    dostnauk = int(str(el.dostnauk))
                    dostnauk += 10
                    el.dostnauk = str(dostnauk)
                    db.session.commit()
                    result['status'] = '200' 
                    result['message'] = 'Успешно' 
                    return result

                if typeevent == 'Спорт':
                    dostsport = int(str(el.dostsport))
                    dostsport += 10
                    el.dostsport = str(dostsport)
                    db.session.commit()
                    result['status'] = '200' 
                    result['message'] = 'Успешно' 
                    return result

                if typeevent == 'Творчество':
                    dosttvor = int(str(el.dosttvor))
                    dosttvor += 10
                    el.dosttvor = str(dosttvor)
                    db.session.commit()
                    result['status'] = '200' 
                    result['message'] = 'Успешно' 
                    return result

                if typeevent == 'Волонтёрство':  
                    dostvol = int(str(el.dostvol))
                    dostvol += 10
                    el.dostvol = str(dostvol)
                    db.session.commit()
                    result['status'] = '200' 
                    result['message'] = 'Успешно' 
                    return result

                else:
                    result['message'] = "Тип мероприятия не найден!" 
                    result['status'] = '400' 
                    return jsonify(result)

    if confirm == 'False':
        onlyData = Data.query.all()
        for el in onlyData:
            if eventid == str(el.id):
                all = f"{el.eventreq}"
                all = ast.literal_eval(all)
                #all.append(userid)
                all.remove(userid)
                el.eventreq = str(all)
                db.session.commit()
                result['status'] = '200' 
                result['message'] = 'Успешно' 
                return result
            
    result['message'] = "Запись не найдена!" 
    result['status'] = '400' 
    return jsonify(result)


@app.route(f'/{version}/search', methods=['POST', 'GET'])
def search() -> json:
    result = {}
    data = request.get_json()
    datasearch = str(data['params']['datasearch'])
    onlyData = Data.query.all()

    for el in onlyData:

        # if datasearch in str(el.nameevent):
        #     result['search'] = str({"img": el.publicationphoto, "desc": publicationdescription, "hash": el.publicationhash, "userid": el.userid})
        #     return jsonify(result)
        
        if datasearch in str(el.publicationdescription) or datasearch in str(el.publicationhash):
            result['search'] = str({"id": el.id, "img": el.publicationphoto, "desc": el.publicationdescription, "hash": el.publicationhash, "userid": el.userid})
            return jsonify(result)
        
    result['message'] = "Ничего не найдено!" 
    result['status'] = '400' 
    return jsonify(result)

@app.route(f'/{version}/lenta', methods=['POST', 'GET'])
def lenta() -> json:
    result = {}
    lst = []
    onlyData = Data.query.all()
    for el in onlyData:

        if el.publicationdescription or el.publicationhash:
            lst.append({"id": el.id, "img": el.publicationphoto, "desc": el.publicationdescription, "hash": el.publicationhash, "userid": el.userid})
    result['publication'] = str(lst)
    return jsonify(result)

@app.route(f'/{version}/lenta_events', methods=['POST', 'GET'])
def lentaEvent() -> json:
    result = {}
    lst = []
    onlyData = Data.query.all()
    for el in onlyData:
        if el.nameevent:
            lst.append({"id": el.id, "name": el.nameevent, "typeevent": el.typeevent, "place": el.place, "date": el.date, "vuzid": el.vuzid, "taskprof": el.taskprof, "photoprof": ast.literal_eval(el.photoprof), 'mems': ast.literal_eval(el.eventmems), 'reqs': ast.literal_eval(el.eventreq)})
    result['publication'] = str(lst)
    return jsonify(result)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5010)# port=5010,