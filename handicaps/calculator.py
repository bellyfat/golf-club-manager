# This is where the magic happens to update a player's handicap
from decimal import Decimal
from .models import Player, Game, GameType, GameScore

def handicap_calculator(player, score, gametype):
    # Initialize values
    handicap = player.handicap

    if score >= gametype.level_4:
        # Checks if the handicap should be increased or decreased to ensure
        # that the updated handicap never exceeds 44.5
        if gametype.level_4_result > 0:
            if handicap + gametype.level_4_result >= Decimal(44.5):
                new_handicap = Decimal(44.5)
            else:
                new_handicap = handicap + gametype.level_4_result
        else:
            new_handicap = handicap + gametype.level_4_result
    elif gametype.level_3_min <= score <= gametype.level_3_max:
        new_handicap = handicap + gametype.level_3_result
    elif gametype.level_2_min <= score <= gametype.level_2_max:
        new_handicap = handicap + gametype.level_2_result
    elif gametype.level_1 >= score:
        if gametype.level_1_result > 0:
            if handicap + gametype.level_1_result >= Decimal(44.5):
                new_handicap = Decimal(44.5)
            else:
                new_handicap = handicap + gametype.level_1_result
        else:
            new_handicap = handicap + gametype.level_1_result

    handicap_change = new_handicap - handicap

    return new_handicap, handicap_change
