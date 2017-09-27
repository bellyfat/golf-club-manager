# Calculates whether the player placed 1st, 2nd, or 3rd, and if so allocates
# additional attendance points
import collections

from .models import Grade, Player, GameType


def get_graded_list():
    grades = Grade.objects.get(pk=1)

    grade_dict = collections.OrderedDict()
    a_dict = collections.OrderedDict()
    b_dict = collections.OrderedDict()
    c_dict = collections.OrderedDict()
    d_dict = collections.OrderedDict()
    e_dict = collections.OrderedDict()

    a_dict = {
        player.full_name_lastfirst: player.handicap_rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_a_min,
        handicap_rounded__lte = grades.grade_a_max
        ).order_by('last_name')
    }

    b_dict = {
        player.full_name_lastfirst: player.handicap_rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_b_min,
        handicap_rounded__lte = grades.grade_b_max
        ).order_by('last_name')
    }

    c_dict = {
        player.full_name_lastfirst: player.handicap_rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_c_min,
        handicap_rounded__lte = grades.grade_c_max
        ).order_by('last_name')
    }

    d_dict = {
        player.full_name_lastfirst: player.handicap_rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_d_min,
        handicap_rounded__lte = grades.grade_d_max
        ).order_by('last_name')
    }

    e_dict = {
        player.full_name_lastfirst: player.handicap_rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_e_min,
        handicap_rounded__lte = grades.grade_e_max
        ).order_by('last_name')
    }

    a_ordered = collections.OrderedDict(sorted(a_dict.items(), key=lambda t: t[0]))
    b_ordered = collections.OrderedDict(sorted(b_dict.items(), key=lambda t: t[0]))
    c_ordered = collections.OrderedDict(sorted(c_dict.items(), key=lambda t: t[0]))
    d_ordered = collections.OrderedDict(sorted(d_dict.items(), key=lambda t: t[0]))
    e_ordered = collections.OrderedDict(sorted(e_dict.items(), key=lambda t: t[0]))

    if grades.grade_use == 3:
        grade_dict['A'] = a_ordered
        grade_dict['B'] = b_ordered
        grade_dict['C'] = c_ordered
    elif grades.grade_use == 4:
        grade_dict['A'] = a_ordered
        grade_dict['B'] = b_ordered
        grade_dict['C'] = c_ordered
        grade_dict['D'] = d_ordered
    else:
        grade_dict['A'] = a_ordered
        grade_dict['B'] = b_ordered
        grade_dict['C'] = c_ordered
        grade_dict['D'] = d_ordered
        grade_dict['E'] = e_ordered

    return grade_dict


def get_player_grade(player):
    grade_dict = get_graded_list()

    if player.full_name_lastfirst in grade_dict['A']:
        return 'A'
    elif player.full_name_lastfirst in grade_dict['B']:
        return 'B'
    elif player.full_name_lastfirst in grade_dict['C']:
        return 'C'
    elif ('D' in grade_dict) and (player.full_name_lastfirst in grade_dict['D']):
        return 'D'
    elif ('E' in grade_dict) and (player.full_name_lastfirst in grade_dict['E']):
        return 'E'
    else:
        return 'F'
