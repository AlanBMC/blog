from django.db import models
from django.conf import settings

# Create your models here.
class Usuario(models.Model):
    nome = models.TextField()
    foto_perfil = models.ImageField(upload_to='perfil/', default='perfil/default.jpg')


class Publicacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='publicacao')
    conteudo = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    
class Comentario(models.Model):
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
