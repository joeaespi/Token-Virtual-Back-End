from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse, Http404
import threading, time
import json
import requests
from .models import Usuario, TokenLog
from typing import List
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .serializers import UsuarioSerializer, TokenLogSerializer
from datetime import datetime
import secrets

usuarios = []
flag = False
segundos = 58


class Usuarios(generics.GenericAPIView):
    """
    Manejas a los usuarios dentro del sistema
    -------
    get(usuario)
        Muestra todos los usuarios del sistema.

    """
    def get(self, request):
        global flag
        res = dict()
        usuarios = Usuario.objects.all()
        print(usuarios[0],len(usuarios))
        print("Es la bandera del hilo",flag)
        for usuario in usuarios:
            tmp = dict()
            tmp["usuario"] = usuario.usuario
            tmp["nombres"] = usuario.nombres+" "+usuario.apellidos
            tmp["token"] = usuario.tokena
            res[usuario.id]=tmp 
        flag = False
        return JsonResponse(res, status=200)
    

class UsuarioToken(generics.GenericAPIView):
    """
    Manejo de los usuario con respecto a su token.
    Methods
    -------
    get(usuario)
        Obtiene la información del usuario junto a su token.
    """
    def get(self, request):
        global flag
        print("Es la bandera del hilo",flag)
        usuario = str(request.GET['cliente'])
        token = str(request.GET['token'])
        print("usuario: ", usuario,"token: ", token)
        
        if usuario!=None and token !=None:
            usuarioE = Usuario.objects.filter(usuario=usuario,tokena=token)
            res=dict()
            res["id"]=usuarioE[0].id
            res["usuario"]=usuarioE[0].usuario
            res["nombres"] = usuarioE[0].nombres+" "+usuarioE[0].apellidos
            res["token"] = usuarioE[0].tokena
            flag=True
            return JsonResponse(res, status=200)


class Token(generics.GenericAPIView):
    """
    Manejo y creación de tokens
    -------
    get(usuario)
        Permite generar un token a un usuario.
    """
    def get(self, request):
        usuario = request.GET['cliente']
        print("fuera del if",usuario)
        if usuario!=None:
            print(usuario)
            res = dict()
            user = Usuario.objects.filter(usuario=usuario)
            global segundos
            global flag
            if flag == False:
                print("El hilo es falso")
                flag = True
            if validarUsariosActivos(usuario):
                #segundos = 50
                print("Ya tiene un hilo activado")
                print("Es la bandera del hilo",flag)
                res["id"]=user[0].id
                res["usuario"]=user[0].usuario
                res["nombres"] = user[0].nombres+" "+user[0].apellidos
                res["token"] = user[0].tokena
                
                return JsonResponse(res, status=200)
            else:
                print("No tiene un hilo activado")
                print("Es la bandera del hilo",flag)
                res = generarToken(usuario)
                hilo = threading.Thread(name='hilo de actualización de token',
                                    target=autoToken, 
                                    args=(segundos,usuario))
                hilo.start()
                return JsonResponse(res, status=200)
                

    
def generarToken(usuario):
    res =dict()
    try: 
        usuarios.append(str(usuario))
        user = Usuario.objects.filter(usuario=usuario)
        tokenActual = user[0].tokena
        token = secrets.token_urlsafe()
        mensaje = "El usuario "+user[0].usuario+" ha actualizado su token. "+ str(datetime.now())
        log = TokenLog(usuario=user[0],anteriortoken=tokenActual,actualtoken=token,mensaje=mensaje)
        user.update(tokena=token)
        log.save()
        res["id"]=user[0].id
        res["usuario"]=user[0].usuario
        res["nombres"] = user[0].nombres+" "+user[0].apellidos
        res["token"] = token
    except Usuario.DoesNotExist:
        res["mensaje"] = "El usuario no existe"
    return res

    
def autoToken(segundos,usuario):
    nombre = threading.current_thread().getName()
    print("voy actualizar mi token")
    while flag:
        print("Estoy ejecutando el hilo: " , nombre," correspondiente al usuario: ",usuario)
        generarToken(usuario)
        time.sleep(segundos)
        
def validarUsariosActivos(usuarioActivo):
    global usuarios
    for usuario in usuarios:
        if str(usuario) == str(usuarioActivo):
            return True
    return False