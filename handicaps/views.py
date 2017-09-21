from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.db import IntegrityError, transaction


from .models import Player, GameType, GameScore, Game, Grade
from .forms import NewGameTypeForm, NewPlayerForm, NewGameForm, \
    NewGameScoreForm, EditPlayerForm, GradeForm
from .calculator import handicap_calculator
from .grade import get_graded_list, get_player_grade


@login_required
def player_list(request):
    players = Player.objects.filter(active=True).order_by('last_name')

    context = {
        'players': players,
    }

    return render(request, 'handicaps/player_list.html', context)

@login_required
def game(request):
    players = Player.objects.filter(active=True).order_by('last_name')

    GameScoreFormSet = formset_factory(NewGameScoreForm, extra=0)

    if request.method == "POST":
        game_form = NewGameForm(request.POST)
        score_formset = GameScoreFormSet(request.POST)

        if game_form.is_valid() and score_formset.is_valid():
            # Save game info
            game = game_form.save()

            # Save the data for each player and score in the formset
            new_scores = []

            for score_form in score_formset:
                player = score_form.cleaned_data.get('player')
                score = score_form.cleaned_data.get('score')

                if player and score:
                    if score == 0:
                        break
                    else:
                        current_grade = get_player_grade(player)

                        new_scores.append(
                            GameScore(
                                player=player,
                                game=game,
                                score=score,
                                grade=current_grade,
                                points=1
                            )
                        )

                        # Get new handicap values
                        calc_result = handicap_calculator(player, score,
                            game.game_type)

                        player.handicap = calc_result[0]
                        player.latest_handicap_change = calc_result[1]
                        player.latest_game = game.game_date

                        player.save()

            try:
                with transaction.atomic():
                    GameScore.objects.bulk_create(new_scores)
                    messages.success(request, 'New game saved.')
                    return redirect('player_list')

            except IntegrityError: # If the transaction failed
                messages.error(request,
                    'There was an error saving the game.')
                return redirect('game')
        else:
            messages.error(request,
                'There was an error in the data provided.')
            return redirect('game') # Temp to identify fail point
    else:
        new_game_form = NewGameForm()
        score_formset = GameScoreFormSet(initial=[{'player': player, 'score': 0}
            for player in players
        ])

        context = {
            'game_form': new_game_form,
            'score_formset': score_formset,
        }

        return render(request, 'handicaps/game.html', context)

@login_required
def settings(request):
    gametypes = GameType.objects.filter(active=True).order_by(
        'create_date')
    context = {
        'gametypes': gametypes,
    }

    return render(request, 'handicaps/settings.html', context)

@login_required
def new_game_type(request):
    if request.method == "POST":
        form = NewGameTypeForm(request.POST)
        if form.is_valid():
            gametype = form.save()
            gametype.create_date = timezone.now()
            gametype.active = True
            return redirect('settings')
    else:
        new_game_type_form = NewGameTypeForm()
        context = {
            'form': new_game_type_form,
        }

        return render(request, 'handicaps/new_game_type.html',
            context)

@login_required
def edit_game_type(request, pk):
    gametype = get_object_or_404(GameType, pk=pk)

    if request.method == "POST":
        form = NewGameTypeForm(request.POST, instance=gametype)
        if form.is_valid():
            gametype = form.save()
            return redirect('settings')
        # else:
        #     return redirect('settings')
    else:
        edit_game_type_form = NewGameTypeForm(instance=gametype)
        context = {
            'form': edit_game_type_form,
        }

        return render(request, 'handicaps/edit_game_type.html', context)

@login_required
def new_player(request):
    if request.method == "POST":
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            return redirect('player_list')
    else:
        new_player_form = NewPlayerForm()
        context = {
            'form': new_player_form,
        }

        return render(request, 'handicaps/new_player.html', context)

@login_required
def edit_player(request, pk):
    player = get_object_or_404(Player, pk=pk)

    if request.method == "POST":
        form = EditPlayerForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save()
            return redirect('player_list')
    else:
        edit_player_form = EditPlayerForm(instance=player)
        context = {
            'form': edit_player_form,
        }

        return render(request, 'handicaps/edit_player.html', context)

@login_required
def game_list(request):
    games = Game.objects.order_by('-game_date')

    return render(request, 'handicaps/game_list.html', {'games': games})

@login_required
def inactive_players(request):
    players = Player.objects.filter(active=False).order_by('last_name')

    context = {
        'players': players,
    }

    return render(request, 'handicaps/inactive_players.html', context)

@login_required
def grade(request):
    grade_dict = get_graded_list()
    context = {
        'grade_dict': grade_dict,
    }

    return render(request, 'handicaps/grade.html', context)

@login_required
def config_grade(request):
    grade = Grade.objects.get(pk=1)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save()
            return redirect('grade')
    else:
        grade_form = GradeForm(instance=grade)

        context = {
            'form': grade_form,
        }

        return render(request, 'handicaps/config_grade.html', context)

@login_required
def expand_player(request, pk):
    player = get_object_or_404(Player, pk=pk)
    game_history = GameScore.objects.filter(player=pk).order_by('-game__game_date')
    context = {
        'player': player,
        'game_history': game_history,
    }
    return render(request, 'handicaps/expand_player.html', context)
