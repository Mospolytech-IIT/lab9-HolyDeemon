from fastapi import FastAPI, Header, Cookie, Request
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
import json

from models import User
class Me:
    age :int
    name : str
    surname : str
    hobby : str
    def __init__(self,  name : str, surname : str, age : int, hobby : str):
        self.name = name
        self.surname = surname
        self.age = age
        self.hobby = hobby
    def dictionary(self):
        return {"name" : self.name, "surname" : self.surname, "age" : self.age, "hobby" : self.hobby}

Users = []

loginedids = []

#Создайте экземпляр класса FastAPI.
app = FastAPI()
@app.get("/")
async def read_root():
    return {"Hello": "World"}

#Обработка параметров:
@app.get("/greet/{name}")
def read_greet(name):
    return f"Hello {name}!"

@app.get("/search/{query}/")
def get_search(query):
    return f"You searched for {query}."

#Отправка различных типов данных:
me = Me("Dmitry", "Popov", 20, "making 21 functions in Backend")
@app.get("/json")
async def get_json():
    return json.dumps(me.dictionary())

@app.get("/file")
async def get_file():
    return FileResponse(path='reqirements.txt')

@app.get("/redirect")
async def get_redirect():
    return RedirectResponse("https://pikabu.ru/story/pochemu_yapontsyi_umirayut_na_rabote_karosi__smert_ot_pererabotki_v_yaponii_5214503")

#Работа с заголовками и куками:
@app.get("/header")
async def def_header(user_agent: str = Header()):
    return {"User-Agent": user_agent}

@app.put("/set-cookie/{user_name}")
async def def_set_coockie(user_name):
    response = JSONResponse({"message": "кука по имени username установлена"})
    response.set_cookie("username", user_name)
    return response

@app.get("/get-cookie")
async def def_cookie(username: str | None = Cookie(None)):
    if username == None:
        return {"message": "куки пока тут нет"}
    else:
        return {"username": username}

#Обработка данных запроса:
@app.get("/login/{login}/{password}")
async def log_in(login, password):
    for user in Users:
        if user.login == login and user.password == password:
            if user.id not in loginedids:
                loginedids.append(user.id)
                return f"Welcome {user.username}"
            else:
                return {"message": "Вы уже в сети"}
    return {"message": "Вы не зарегистрированны!"}

@app.post("/register/{login}/{password}/{name}/{email}")
async def register(login, password, name, email):
    ids = []
    for user in Users:
        if user.login == login and user.password == password:
            return {"message": "Вы уже зарегистрированны!"}
        ids.append(user.id)
    if(ids != []):
        for i in (0, max(ids)+1):
            if(i not in ids):
                a = User(i, name, email, login, password)
                Users.append(a)
                return json.dumps(a.dictionary())
    a = User(0, name, email, login, password)
    Users.append(a)
    return json.dumps(a.dictionary())

#Работа с классами
@app.get("/users")
async def get_users():
    return Users

@app.get("/user/{id}")
async def get_user(id : int):
    for user in Users:
        if user.id == id:
            return user
