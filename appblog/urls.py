from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('login_/', views.login_, name='login_'),
    path('cadastro/' , views.cadastro, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('conf/', views.conf, name='conf'),

    path('meu_perfil/', views.perfil, name='perfil'),
    path('publicar_perfil/', views.publicar_perfil, name='publicar_perfil'),
    path('publicar_time/', views.publicar_time, name='publicar_time'),
    path('feed/', views.feed, name='time_line'),
    path('perfil_usuario/<int:usuario_id>', views.perfil_usuario, name='perfil_usuario'),

    path('delete_post_time/', views.delete_post_time, name='delete_post_time'),
    path('delete_post_perfil/', views.delete_post_perfil, name='delete_post_perfil'),

    path('comentarios/<int:id_post>', views.comentarios, name='comentarios'),
    path('comentar/', views.comentar, name='comentar'),
    
    path('delete_comentario/<int:comentario_id>', views.delete_comentario, name='delete_comentario')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
