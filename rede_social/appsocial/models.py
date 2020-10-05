from django.db import models


class Usuario(models.Model):
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=12)
    dt_nascimento = models.DateField()

    def __str__(self):
        return self.email


class Perfil(models.Model):
    nome = models.CharField(max_length=50)
    usuario = models.CharField(max_length=20)
    contatos = models.ManyToManyField(
        'self', related_name='contatos', blank=True)

    def timeline(self):
        return Postagem.objects.filter(perfil=self)

    def __str__(self):
        return self.usuario


class Postagem(models.Model):
    texto = models.CharField(max_length=200)
    data = models.DateField(auto_now_add=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    def len_reacao(self):
        return Reacao.objects.annotate(
            len_reacao=(models.Count('tipo') * models.F('peso'))
        ).filter(postagem=self)

    def __str__(self):
        return self.texto


class Comentario(models.Model):
    texto = models.CharField(max_length=200)
    data = models.DateField(auto_now_add=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto


class tipoReacao(models.TextChoices):
    curtir = 'Curtir'
    amar = 'Amar'
    rir = 'Rir'
    impressionar = 'Impressionar'
    triste = 'Triste'
    irritar = 'Irritar'


class Reacao(models.Model):
    tipo = models.CharField('Tipo', max_length=20, choices=tipoReacao.choices)
    data = models.DateField(auto_now_add=True)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    peso = models.IntegerField('Peso')

    def __str__(self):
        return self.tipo
