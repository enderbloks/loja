from fastapi import FastAPI

from pydantic import BaseModel

from typing import Optional, Text

import hashlib

import random

import sqlite3

app = FastAPI()
class Logon(BaseModel):
    email: Text
    senha: Text

class User(BaseModel):
    email: Text
    nome: Text
    senha1: Text
    senha2: Text

@app.post("/user")
async def add_user(us: User):
    if check(us):
        return {"msg": create(us)}
    else:
        return {"msg":"senha incorreta"}

@app.post("/login")
async def login(us: Logon):
    if valid_email(us):
        return valid_senha(us)
    else:
        return False

@app.get("/health")
async def health():
    return {"message": "ok"}

def check(us: User):
    if us.senha1 == us.senha2:
        return True
    else:
        return False

def create(us: User):
    s = crypt(us.senha1)
    try:
        print("conectar")
        c = sqlite3.connect("sistema.db")
        print("conectar2")
        cr = c.cursor()
        print("conectar3")
        cr.execute(""" insert into usuario (email,nome,senha) values (?,?,?)""",(us.email,us.nome,s))
        print("conectar4")
        c.commit()
        c.close()
        print("conectar5")
    except:
        return{"msg":"erro database"}
    else:
        return{"msg":"registro encluido com sucesso"}

def crypt(s):
    r = str(random.randrange(1,20000))
    h = hashlib.sha512((s+r).encode("utf-8")).hexdigest() + "#" + r
    return h

def valid_email(us: Logon):
    try:
        r = False
        c = sqlite3.connect("sistema.db")
        cr = c.cursor()
        cr.execute(""" select email from usuario where email = ? """,(us.email,))
        for linha in cr.fetchall():
            r = True
        
        c.close()
        
    except:
        return r
    else:
        return r
    return r

def valid_senha(us: Logon):
    try:
        r = False
        a = ""
        senha = ""
        c = sqlite3.connect("sistema.db")
        cr = c.cursor()
        cr.execute(""" select senha from usuario where email = ? """,(us.email,))
        for linha in cr.fetchall():
            senha = linha[0]
            a = senha.split("#")
        s = crypt_senha(us.senha + a[1])
        if a[0] == s:
            r = True
        else:
            r = False
        c.close()
        
    except:
        return r
    else:
        return r
    return r

def crypt_senha(s):
    #r = str(random.randrange(1,20000))
    h = hashlib.sha512((s).encode("utf-8")).hexdigest()
    return h