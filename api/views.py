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




class Usuarios(generics.GenericAPIView):
    """
    Manejas a los usuarios dentro del sistema
    -------
    get(usuario)
        Muestra todos los usuarios del sistema.

    """
    def get(self, request):
        res = dict()
        usuarios = Usuario.objects.all()
        print(usuarios[0],len(usuarios))
        for usuario in usuarios:
            tmp = dict()
            tmp["usuario"] = usuario.usuario
            tmp["nombres"] = usuario.nombres+" "+usuario.apellidos
            tmp["token"] = usuario.tokena
            res[usuario.id]=tmp 
        return JsonResponse(res, status=200)
    

class UsuarioToken(generics.GenericAPIView):
    """
    Manejo de los usuario con respecto a su token.
    Methods
    -------
    get(usuario)
        Obtiene la información del usuario junto a su token.
    post(usuario)
        Permite generar un token con respecto al usuario
        asociado.
    """
    #def get(self, request, usuario,token):
    def get(self, request):
        usuario = request.GET['cliente']
        token = request.GET['token']
        if usuario!=None and token !=None:
            print(usuario,token)
            usuarioE = Usuario.objects.filter(usuario=usuario,tokena=token)
            res=dict()
            res["id"]=usuarioE[0].id
            res["usuario"]=usuarioE[0].usuario
            res["nombres"] = usuarioE[0].nombres+" "+usuarioE[0].apellidos
            res["token"] = usuarioE[0].tokena
            print("usuarioE",usuarioE[0].usuario)
            return JsonResponse(res, status=200)


class Token(generics.GenericAPIView):
    """
    Manejo y creación de tokens
    -------
    get(usuario)
        Permite generar un token a un usuario.
    """
    #def get(self, request, usuario,token):
    def get(self, request):
        usuario = request.GET['cliente']
        if usuario!=None:
            print(usuario)
            res = generarToken(usuario)
            usuarioE = Usuario.objects.filter(usuario=usuario,tokena=token)
            hilo = threading.Thread(name='hilo de actualización de token',
                                target=autoToken, 
                                args=(20,usuario))
            hilo.start()
            #return Response(usuarioE)
            return JsonResponse(res, status=200)

    
def generarToken(usuario):
    res =dict()
    try: 
        user = Usuario.objects.filter(usuario=usuario)
        print("este es mi usuario",user[0].usuario)
        tokenActual = user[0].tokena
        token = secrets.token_urlsafe()
        print("Este es mi antiguo token",tokenActual,"Este es mi nuevo token",token)
        mensaje = "El usuario "+user[0].usuario+" ha actualizado su token. "+ str(datetime.now())
        log = TokenLog(usuario=user[0],anteriortoken=tokenActual,actualtoken=token,mensaje=mensaje)
        user.update(tokena=token)
        print("he actualizado mi token")
        log.save()
        print("he guardado un registro de mi token")
        res["id"]=user[0].id
        res["usuario"]=user[0].usuario
        res["nombres"] = user[0].nombres+" "+user[0].apellidos
        res["token"] = token
    #return Response(token.key)
        #return 
    except Usuario.DoesNotExist:
        #return Response("El usuario no existe")
        res["mensaje"] = "El usuario no existe"
    return res

    

def autoToken(segundos,usuario):
    inicial = time.time()
    print("valor de variable inicial: ",inicial)
    limite = inicial + segundos
    print("Valor de variable llimite: ",limite)
    nombre = threading.current_thread().getName()
    #print("Valor de variable nombre: " , nombre)
    while inicial <= limite:
        inicial = time.time()
        generarToken(usuario)
        #print(nombre, contador)
    print("He alcanzado el lite de ",segundos,"segundos")