from django.db import models
from django.utils import timezone


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    handicap = models.DecimalField(max_digits=3,decimal_places=1)
    latest_handicap_change = models.DecimalField(max_digits=2,
        decimal_places=1, null=True)
    latest_game = models.DateField(null=True)
    active = models.BooleanField(default=True)
    handicap_rounded = models.IntegerField()

    @property
    def full_name_lastfirst(self):
        return ''.join(
            [self.last_name,', ', self.first_name]
            )

    @property
    def recent_game(self):
        return str(self.latest_game)

    def __str__(self):
        return self.full_name_lastfirst

    # Need to override the default save function to allow
    # the handicap_rounded field to be autopopulated based
    # on the value within handicap
    def save(self, *args, **kwargs):
        self.handicap_rounded = int(round(self.handicap))
        super(Player, self).save(*args, **kwargs)


class Game(models.Model):
    game_date = models.DateField()
    game_type = models.ForeignKey('GameType')

    def __str__(self):
        return "%s - %s" % (self.game_date, self.game_type)


class GameScore(models.Model):
    player = models.ForeignKey('Player')
    game = models.ForeignKey('Game')
    score = models.IntegerField(null=True)
    grade = models.CharField(max_length=1, null=True)
    points = models.IntegerField(null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.player, self.game, self.score)


class GameType(models.Model):
    name = models.CharField(max_length=15)
    create_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    level_4 = models.IntegerField()
    level_4_result = models.DecimalField(max_digits=2,
        decimal_places=1)
    level_3_min = models.IntegerField()
    level_3_max = models.IntegerField()
    level_3_result = models.DecimalField(max_digits=2,
        decimal_places=1)
    level_2_min = models.IntegerField()
    level_2_max = models.IntegerField()
    level_2_result = models.DecimalField(max_digits=2,
        decimal_places=1)
    level_1 = models.IntegerField()
    level_1_result = models.DecimalField(max_digits=2,
        decimal_places=1)

    def __str__(self):
        return self.name


class Grade(models.Model):
    USE3 = 3
    USE4 = 4
    USE5 = 5
    GRADE_CHOICES = (
        (USE3, '3 grades'),
        (USE4, '4 grades'),
        (USE5, '5 grades'),
    )
    grade_use = models.IntegerField(choices=GRADE_CHOICES, default=USE3)
    grade_a_min = models.IntegerField(default=0)
    grade_a_max = models.IntegerField(default=0)
    grade_b_min = models.IntegerField(default=0)
    grade_b_max = models.IntegerField(default=0)
    grade_c_min = models.IntegerField(default=0)
    grade_c_max = models.IntegerField(default=0)
    grade_d_min = models.IntegerField(default=0)
    grade_d_max = models.IntegerField(default=0)
    grade_e_min = models.IntegerField(default=0)
    grade_e_max = models.IntegerField(default=0)

    def __str__(self):
        return str(self.grade_use)
