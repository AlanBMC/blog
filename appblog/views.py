from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from .models import Usuario, Publicacao, Comentario
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# -------------------- login, logout, conf -------------------

@login_required(login_url="/blog/login_/")
def conf(request):
    """
    View de configuração do perfil para atualizar a imagem de perfil do usuário.

    Esta view permite que os usuários autenticados atualizem a imagem de perfil.
    Se uma nova imagem de perfil for enviada através do formulário de postagem,
    a imagem de perfil do usuário será atualizada. Caso contrário, uma mensagem
    de erro será exibida informando que nenhuma imagem foi fornecida.

    Parâmetros:
    - request: HttpRequest object que contém metadados sobre a requisição.

    Retorna um redirecionamento para a própria página de configuração ('conf')
    após a tentativa de atualização da imagem, ou renderiza 'conf.html' se o
    método da requisição for GET.

    Utiliza o decorador @login_required para assegurar que apenas usuários
    autenticados possam acessar esta view. O parâmetro `login_url` especifica
    para onde o usuário será redirecionado caso não esteja autenticado.
    """
    if request.method == 'POST':
        img = request.FILES.get('imagem_de_perfil', None)
        user_instance = request.user

        # Atualiza a imagem de perfil no modelo Usuario, se fornecida
        if img:
            # Supondo que 'nome' é único e corresponde ao username do usuário autenticado
            perfil_usuario = Usuario.objects.get(nome=user_instance.username)
            perfil_usuario.foto_perfil = img
            perfil_usuario.save()
            messages.success(
                request, 'Imagem de perfil atualizada com sucesso!')
        else:
            messages.error(request, 'Nenhuma imagem foi fornecida.')

        return redirect('conf')
    else:
        return render(request, 'conf.html')


@login_required(login_url="/blog/login_/")
def logout_view(request):
    """
    Realiza o logout do usuário atual.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponseRedirect: Redireciona para a página de login após fazer logout.

    Requer:
        O usuário deve estar logado.

    Exemplo:
        @login_required(login_url="/blog/login_/")
        def alguma_view(request):
            ...
            return logout_view(request)
    """
    logout(request)
    return redirect('login_')


def login_(request):
    if request.method == 'POST':
        nome = request.POST.get('uname')
        senha = request.POST.get('psw')
        user = authenticate(username=nome, password=senha)
        if user:
            login_django(request, user)
            usuario = Usuario.objects.get(nome=nome)
            print(usuario.nome)
            return redirect('time_line')
    else:
        return render(request, 'login.html')


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('uname')
        senha = request.POST.get('psw')
        img = request.FILES.get('imagem_de_perfil')
        if User.objects.filter(username=nome).exists():
            # Usar mensagens para enviar feedback ao usuário
            return render(request, 'login.html', {'error_message': 'Nome de usuário já existe. Por favor, escolha outro nome.'})
        else:
            user = User.objects.create_user(
                username=nome, password=senha)
            user.save()
            usuario = Usuario(nome=nome, foto_perfil=img)
            usuario.save()

            return redirect('login_')
    else:
        return render(request, 'cadastro.html')


# ---------------- end login, logout, cadastro ---------------------------


# ---------------- deletes ---------------------------

    # -------------deletes post -----------------------

def delete_post_time(request):
    if request.method == 'POST':
        id_post = request.POST.get('post_delete')
        post = Publicacao.objects.filter(id=id_post)
        post.delete()
        return redirect('time_line')


def delete_post_perfil(request):
    if request.method == 'POST':
        id_post = request.POST.get('post_delete')
        post = Publicacao.objects.filter(id=id_post)
        post.delete()
        return redirect('perfil')

# ---------------- end deletes posts -------------------

    # -------------- deletes comentarios --------------


def delete_comentario(request, comentario_id):
    comentario_id = request.POST.get('id_comentario')
    comentario = get_object_or_404(Comentario, id=comentario_id)
    comentario.delete()
    messages.success(request, "Comentário deletado com sucesso.")
    id_post = request.POST.get('id_post')
    return redirect('comentarios', id_post)

    # -------------- end deletes comentarios --------------


# ------------ end deletes ----------------------


# ---------------- comentarios -------------------

def comentarios(request, id_post):
    post_id1 = request.POST.get('id_post')
    publicacao = get_object_or_404(Publicacao, id=id_post)
    comentarios = publicacao.comentarios.all()
    return render(request, 'comentarios.html', {'publicacao': publicacao, 'comentarios': comentarios})


def comentar(request):
    comentario = request.POST.get('comentar')
    id_post = request.POST.get('id_post')
    user = request.user.username
    usuario = get_object_or_404(Usuario, nome=user)
    publicacao = get_object_or_404(Publicacao, id=id_post)
    comentario_novo = Comentario(
        publicacao=publicacao, usuario=usuario, texto=comentario)
    comentario_novo.save()
    return redirect("comentarios", id_post)


# ----------------------- end  comentarios -------------------------


# -------------------- publicar post ------------------------------
@login_required(login_url="/blog/login_/")
def publicar_perfil(request):
    if request.method == 'POST':
        publicacao = request.POST.get('publicacao')
        usuario_atual = request.user.username
        try:
            usuario = Usuario.objects.get(nome=usuario_atual)
        except Usuario.DoesNotExist:
            return HttpResponse("Usuário não encontrado")
        if usuario:
            nova_publicacao = Publicacao(conteudo=publicacao, usuario=usuario)
            nova_publicacao.save()
            return redirect('perfil')
    else:
        return render(request, 'meu_perfil.html')


@login_required(login_url="/blog/login_/")
def publicar_time(request):
    if request.method == 'POST':
        publicacao = request.POST.get('publicacao')
        usuario_atual = request.user.username
        try:
            usuario = Usuario.objects.get(nome=usuario_atual)
        except Usuario.DoesNotExist:
            return HttpResponse("Usuário não encontrado")
        if usuario:
            nova_publicacao = Publicacao(conteudo=publicacao, usuario=usuario)
            nova_publicacao.save()
            return redirect('time_line')
    else:
        return render(request, 'meu_perfil.html')

# -------------------- end publicar post ------------------------------


# -------------------- renderiza conteudo principal ------------------------------


@login_required(login_url="/blog/login_/")
def perfil(request):
    nome_do_usuario_atual = request.user.username
    usuarios = Usuario.objects.get(nome=nome_do_usuario_atual)
    publicacoes_do_usuario = Publicacao.objects.filter(usuario=usuarios).select_related(
        'usuario').prefetch_related('comentarios').order_by('-data_hora')
    contexto = {'publicacoes': publicacoes_do_usuario,
                'foto_perfil': usuarios.foto_perfil.url}
    return render(request, 'meu_perfil.html', contexto)


@login_required(login_url="/blog/login_/")
def feed(request):
    # publicacoes = Publicacao.objects.all().select_related('usuario').prefetch_related('comentarios').order_by('data_hora')
    nome_do_usuario_atual = request.user.username
    usuarios = Usuario.objects.get(nome=nome_do_usuario_atual)
    publicacoes = Publicacao.objects.all().select_related(
        'usuario').prefetch_related('comentarios').order_by('-data_hora')
    contexto = {'publicacoes': publicacoes,
                'foto_perfil': usuarios.foto_perfil.url}
    # for publicacao in publicacoes:
    # print(publicacao.usuario.nome)
    return render(request, 'time_line.html', contexto)

    # -------------------- renderiza perfil de outros usuarios --------------------------


@login_required(login_url="/blog/login_/")
def perfil_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    nome_do_usuario_atual = usuario.nome
    usuarios = Usuario.objects.get(nome=nome_do_usuario_atual)
    publicacoes_do_usuario = Publicacao.objects.filter(
        usuario=usuarios).select_related('usuario').prefetch_related('comentarios')
    contexto = {'publicacoes': publicacoes_do_usuario}
    return render(request, 'meu_perfil.html', contexto)

    # --------------------end renderiza perfil de outros usuarios --------------------------


# -------------------- end renderiza conteudo ------------------------------
