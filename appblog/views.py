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


def buscar_usuarios(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        resultados = Usuario.objects.filter(nome__icontains=query)
    return render(request, 'time_line.html', {'resultados': resultados, 'query': query})


def cadastro(request):
    """
    Registra um novo usuário.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponseRedirect ou HttpResponse: Redireciona para a página de login após o cadastro bem-sucedido,
        ou renderiza a página de cadastro.

    Exemplo:
        Para acessar a página de cadastro:
        http://localhost:8000/blog/cadastro/

    """
    if request.method == 'POST':
        nome = request.POST.get('uname')
        senha = request.POST.get('psw')
        img = request.FILES.get('imagem_de_perfil', None)  # Ajuste para permitir cadastro sem imagem
        if User.objects.filter(username=nome).exists():
            # Usar mensagens para enviar feedback ao usuário
            messages.error(request, 'Nome de usuário já existe. Por favor, escolha outro nome.')
            return redirect('cadastro')  # Redireciona de volta para a página de cadastro
        else:
            user = User.objects.create_user(username=nome, password=senha)
            user.save()
            usuario = Usuario(nome=nome)
            if img:
                usuario.foto_perfil = img
            usuario.save()
            messages.success(request, 'Cadastro realizado com sucesso! Por favor, faça o login.')
            return redirect('login_')
    else:
        return render(request, 'cadastro.html')


# ---------------- end login, logout, cadastro ---------------------------


# ---------------- deletes ---------------------------

    # -------------deletes post -----------------------

def delete_post_time(request):
    """
    Exclui uma publicação da linha do tempo.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponseRedirect: Redireciona de volta para a linha do tempo após excluir a publicação.

    Exemplo:
        Suponha que a página de linha do tempo esteja acessível em:
        http://localhost:8000/blog/time_line/
        e o formulário de exclusão de post seja submetido.

    """
    if request.method == 'POST':
        id_post = request.POST.get('post_delete')
        post = Publicacao.objects.filter(id=id_post)
        post.delete()
        return redirect('time_line')


def delete_post_perfil(request):
    """
    Exclui uma publicação do perfil do usuário.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponseRedirect: Redireciona de volta para o perfil após excluir a publicação.

    Exemplo:
        Suponha que a página de perfil esteja acessível em:
        http://localhost:8000/blog/perfil/
        e o formulário de exclusão de post seja submetido.

    """
    if request.method == 'POST':
        id_post = request.POST.get('post_delete')
        post = Publicacao.objects.filter(id=id_post)
        post.delete()
        return redirect('perfil')

# ---------------- end deletes posts -------------------

    # -------------- deletes comentarios --------------


def delete_comentario(request, comentario_id):
    """
    Exclui um comentário.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        comentario_id (int): O ID do comentário a ser excluído.

    Returns:
        HttpResponseRedirect: Redireciona de volta para a página de comentários após excluir o comentário.

    Exemplo:
        Suponha que a página de comentários esteja acessível em:
        http://localhost:8000/blog/comentarios/1/
        e o formulário de exclusão de comentário seja submetido.

    """
    comentario = get_object_or_404(Comentario, id=comentario_id)
    comentario.delete()
    messages.success(request, "Comentário deletado com sucesso.")
    id_post = request.POST.get('id_post')
    return redirect('comentarios', id_post)

    # -------------- end deletes comentarios --------------


# ------------ end deletes ----------------------





# -------------------- publicar post ------------------------------
@login_required(login_url="/blog/login_/")
def publicar_perfil(request):
    """
    Publica uma nova postagem no perfil do usuário.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponseRedirect ou HttpResponse: Redireciona de volta para o perfil após publicar a postagem,
        ou renderiza a página do perfil.

    Exemplo:
        Suponha que a página do perfil esteja acessível em:
        http://localhost:8000/blog/perfil/
        e um novo post seja enviado via formulário.

    """
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
    """
    Publica uma nova postagem na linha do tempo.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponseRedirect ou HttpResponse: Redireciona de volta para a linha do tempo após publicar a postagem,
        ou renderiza a página do perfil.

    Exemplo:
        Suponha que a página da linha do tempo esteja acessível em:
        http://localhost:8000/blog/time_line/
        e um novo post seja enviado via formulário.

    """
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
    """
    Exibe o perfil do usuário logado.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página do perfil do usuário logado.

    Exemplo:
        Suponha que o perfil esteja acessível em:
        http://localhost:8000/blog/perfil/

    """
    nome_do_usuario_atual = request.user.username
    usuarios = Usuario.objects.get(nome=nome_do_usuario_atual)
    publicacoes_do_usuario = Publicacao.objects.filter(usuario=usuarios).select_related(
        'usuario').prefetch_related('comentarios').order_by('-data_hora')
    contexto = {'publicacoes': publicacoes_do_usuario,
                'foto_perfil': usuarios.foto_perfil.url}
    return render(request, 'meu_perfil.html', contexto)


@login_required(login_url="/blog/login_/")
def feed(request):
    """
    Exibe o feed de publicações.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página de feed com as publicações.

    Exemplo:
        Suponha que o feed esteja acessível em:
        http://localhost:8000/blog/feed/

    """
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

#arrumar
@login_required(login_url="/blog/login_/")
def perfil_usuario(request, usuario_id):
    """
    Exibe o perfil de um usuário específico.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        usuario_id (int): O ID do usuário cujo perfil está sendo visualizado.

    Returns:
        HttpResponse: Renderiza a página do perfil do usuário específico.

    Exemplo:
        Suponha que o perfil de usuário esteja acessível em:
        http://localhost:8000/blog/perfil/1/

    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    nome_do_usuario_buscado = usuario.nome
    nome_do_usuario_logado = request.user.username
    usuarios_logado = Usuario.objects.get(nome=nome_do_usuario_logado)
    usuarios = Usuario.objects.get(nome=nome_do_usuario_buscado)
    publicacoes_do_usuario = Publicacao.objects.filter(
        usuario=usuarios).select_related('usuario').prefetch_related('comentarios')
    contexto = {'publicacoes': publicacoes_do_usuario, 'foto_perfil': usuarios_logado.foto_perfil.url}
    return render(request, 'meu_perfil.html', contexto)

    # --------------------end renderiza perfil de outros usuarios --------------------------

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
            messages.error(request, 'Nome de usuário ou senha inválidos.')

            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
# -------------------- end renderiza conteudo ------------------------------
# ---------------- comentarios -------------------

def comentarios(request, id_post):
    """
    Exibe os comentários de uma publicação.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        id_post (int): O ID da publicação.

    Returns:
        HttpResponse: Renderiza a página de comentários com os comentários da publicação.

    Exemplo:
        Suponha que a página de comentários esteja acessível em:
        http://localhost:8000/blog/comentarios/1/

    """
    nome_do_usuario_atual = request.user.username
    usuarios = Usuario.objects.get(nome=nome_do_usuario_atual)    
    publicacao = get_object_or_404(Publicacao, id=id_post)
    comentarios = publicacao.comentarios.all()
    
    return render(request, 'comentarios.html', {'publicacao': publicacao, 'comentarios': comentarios, 'foto_perfil': usuarios.foto_perfil.url})


def comentar(request):
    """
    Adiciona um novo comentário a uma publicação.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponseRedirect: Redireciona de volta para a página de comentários após adicionar o comentário.

    Exemplo:
        Suponha que a página de comentários esteja acessível em:
        http://localhost:8000/blog/comentarios/1/
        e um novo comentário seja enviado via formulário.

    """
    comentario = request.POST.get('comentar')
    id_post = request.POST.get('id_post')
    user = request.user.username
    usuario = get_object_or_404(Usuario, nome=user)
    publicacao = get_object_or_404(Publicacao, id=id_post)
    comentario_novo = Comentario(publicacao=publicacao, usuario=usuario, texto=comentario)
    comentario_novo.save()
    return redirect("comentarios", id_post)

# ----------------------- end  comentarios -------------------------