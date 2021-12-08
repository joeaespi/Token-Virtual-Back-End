from rest_framework import serializers
from .models import Usuario, TokenLog


class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usuario
		fields = '__all__'

class TokenLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenLog
        fields = '__all__'