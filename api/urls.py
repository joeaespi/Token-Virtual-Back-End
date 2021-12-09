from django.urls import path
from . import views

urlpatterns = [
    #path('usarToken/<str:usuario>/<str:token>',views.UsuarioToken.as_view(),name="usarToken"),
    path('usarToken/',views.UsuarioToken.as_view(),name="usarToken"),
    #path('generarToken/?cliente=<str:usuario>',views.UsuarioToken.as_view(),name="generarToken"),
    path('generarToken/',views.Token.as_view(),name="generarToken"),
    path('mostrarUsuarios/',views.Usuarios.as_view(),name="usuarios"),
]#