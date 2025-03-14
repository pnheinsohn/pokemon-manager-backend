from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError


class BasePokemonType(models.Model):
    """Represents a Pokemon type (e.g., Fire, Water, Grass).

    Each base Pokemon can have multiple types, creating the classic
    type system that Pokemon is known for.

    Attributes:
        name (str): The unique name of the type
    """
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [models.Index(fields=['name'])]


class PokemonLevel(models.Model):
    """Manages Pokemon level and experience progression.

    Handles the level system with experience points and goals.
    Each Pokemon has exactly one level instance (one-to-one relationship).

    Attributes:
        value (int): Current level, constrained between MIN_LEVEL (1) and MAX_LEVEL (100)
        experience (int): Current experience points accumulated at this level
        experience_goal (int): Experience points needed to reach the next level

    Constants:
        MIN_LEVEL (int): Minimum possible level (1)
        MAX_LEVEL (int): Maximum possible level (100)
        BASE_EXPERIENCE (int): Starting experience points (0)
        BASE_EXPERIENCE_GOAL (int): Initial experience needed for first level up (100)
    """
    MIN_LEVEL = 1
    MAX_LEVEL = 100
    BASE_EXPERIENCE = 0
    BASE_EXPERIENCE_GOAL = 100

    value = models.IntegerField(
        default=MIN_LEVEL,
        validators=[MinValueValidator(MIN_LEVEL), MaxValueValidator(MAX_LEVEL)]
    )
    experience = models.IntegerField(default=BASE_EXPERIENCE, validators=[MinValueValidator(BASE_EXPERIENCE)])
    experience_goal = models.IntegerField(default=BASE_EXPERIENCE_GOAL, validators=[MinValueValidator(BASE_EXPERIENCE_GOAL)])

    def __str__(self):
        return f"{self.value} (exp: {self.experience} / {self.experience_goal})"


class BasePokemon(models.Model):
    """Represents a Pokemon species with its base attributes.

    This model stores the fundamental data for each Pokemon species,
    including their Pokedex information and base stats. It serves as
    a template for creating individual Pokemon instances.

    Attributes:
        types (ManyToManyField): Types this Pokemon belongs to
        name (str): Official species name
        pokedex_number (int): Unique Pokedex identifier
        base_hp (int): Base Health Points stat
        base_attack (int): Base Attack stat
        base_defense (int): Base Defense stat
        base_special_attack (int): Base Special Attack stat
        base_special_defense (int): Base Special Defense stat
        base_speed (int): Base Speed stat
    """
    types = models.ManyToManyField(BasePokemonType, related_name='base_pokemons')
    name = models.CharField(max_length=200, unique=True)
    pokedex_number = models.IntegerField(validators=[MinValueValidator(1)], unique=True)

    # Base stats
    base_hp = models.IntegerField(validators=[MinValueValidator(1)])
    base_attack = models.IntegerField(validators=[MinValueValidator(1)])
    base_defense = models.IntegerField(validators=[MinValueValidator(1)])
    base_special_attack = models.IntegerField(validators=[MinValueValidator(1)])
    base_special_defense = models.IntegerField(validators=[MinValueValidator(1)])
    base_speed = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.name} (#{self.pokedex_number})"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['pokedex_number']),
        ]


class Pokemon(models.Model):
    """Represents an individual Pokemon instance.

    Each Pokemon is based on a BasePokemon species but has its own
    level, nickname, and current stats. This model represents the
    actual Pokemon that trainers would own and battle with.

    Attributes:
        base_pokemon (ForeignKey): Reference to the Pokemon species
        level (OneToOneField): Pokemon's current level information
        nickname (str): Custom name given to this Pokemon
        hp (int): Current Health Points
        attack (int): Current Attack stat
        defense (int): Current Defense stat
        special_attack (int): Current Special Attack stat
        special_defense (int): Current Special Defense stat
        speed (int): Current Speed stat
    """
    base_pokemon = models.ForeignKey(BasePokemon, on_delete=models.CASCADE, related_name='instances')
    level = models.OneToOneField(PokemonLevel, on_delete=models.CASCADE, related_name='pokemon')
    nickname = models.CharField(max_length=200)

    # Current stats
    hp = models.IntegerField(validators=[MinValueValidator(1)])
    attack = models.IntegerField(validators=[MinValueValidator(1)])
    defense = models.IntegerField(validators=[MinValueValidator(1)])
    special_attack = models.IntegerField(validators=[MinValueValidator(1)])
    special_defense = models.IntegerField(validators=[MinValueValidator(1)])
    speed = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        if self.nickname != self.base_pokemon.name:
            return f"{self.nickname} ({self.base_pokemon.name})"
        return self.nickname

    class Meta:
        indexes = [models.Index(fields=['nickname'])]
