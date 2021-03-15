from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Название")
    title_en = models.CharField(max_length=200, verbose_name="Название(анг.)", blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="Название(яп.)", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    photo = models.ImageField(upload_to="pokemons", verbose_name="Изображение", null=True)
    pre_evolution = models.ForeignKey(
        "self",
        verbose_name="Из кого эволюционировал",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="prev_pokemons"
    )
    next_evolution = models.ForeignKey(
        "self",
        verbose_name="В кого эволюционирует",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="next_pokemons"
    )


    def __str__(self):
        return f"{self.title_ru}"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name="Название", on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Появился", blank=True)
    disappeared_at = models.DateTimeField(verbose_name="Исчез", blank=True)
    level = models.IntegerField(verbose_name="Уровень", blank=True)
    health = models.IntegerField(verbose_name="Здоровье", blank=True)
    strength = models.IntegerField(verbose_name="Сила", blank=True)
    defence = models.IntegerField(verbose_name="Защита", blank=True)
    stamina = models.IntegerField(verbose_name="Выносливость", blank=True)
