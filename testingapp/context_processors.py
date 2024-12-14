def theme(request):
    if 'is_dark_theme' in request.session:
        is_dark_theme = request.session.get('is_dark_theme')
        return {'is_dark_theme':is_dark_theme}
    return {'is_dark_theme': False}

def colortheme(request):
    if 'color_theme' in request.session:
        color_theme = request.session.get('color_theme')
        return {'color_theme':color_theme}
    return {'color_theme': False}

def defaulttheme(request):
    if 'original_theme' in request.session:
        original_theme = request.session.get('original_theme')
        return {'original_theme':original_theme}
    return {'original_theme': False}

from django.contrib.auth.models import User
from .models import post,BlogHistory,searchedRecipesRanking
from django.db.models import Count
import datetime


import re
from itertools import product

def search_autocomplete_data(request):
    titlesn = post.objects.all()
    userprofile = User.objects.all()

    titles = [tlist.title for tlist in titlesn]
    user_profiles = [profile.get_full_name() for profile in userprofile]

    # Define category, cuisine, type, and difficulty lists
    category = ['Veg', 'Non Veg']
    cuisine = ['Indian', 'American', 'Italian']
    type = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']
    difficulty = ['easy', 'medium', 'hard']

    # Timing pattern for queries like "under 10 mins" or "ready in 20 mins"
    timing_pattern = r'\b(?:under|ready\s*in)?\s*(\d+)\s*(?:minutes|min|mins)?\b'

    # Generate unique combinations
    category_type_combinations = [f"{cat.lower()} {typ.lower()} recipes" for cat, typ in product(category, type)]
    cuisine_difficulty_combinations = [f"{cuisine.lower()} cuisine {dif.lower()} recipes" for cuisine, dif in product(cuisine, difficulty)]
    category_cuisine_combinations = [f"{cat.lower()} {cuisine.lower()} recipes" for cat, cuisine in product(category, cuisine)]
    difficulty_type_combinations = [f"{dif.lower()} {typ.lower()} recipes" for dif, typ in product(difficulty, type)]

    # Combine all phrases into one list, ensuring distinct phrases
    combined_suggestions = list(set(category_type_combinations + cuisine_difficulty_combinations + category_cuisine_combinations + difficulty_type_combinations))

    # Add general phrases
    category_phrases = [f"{cat.lower()} recipes" for cat in category]
    cuisine_phrases = [f"{cuisine.lower()} cuisine recipes" for cuisine in cuisine]
    type_phrases = [f"{typ.lower()} recipes" for typ in type]
    difficulty_phrases = [f"cooking difficulty {dif.lower()}" for dif in difficulty]

    # Merge all suggestions
    autocomplete_suggestions = titles + user_profiles + combined_suggestions + category_phrases + cuisine_phrases + type_phrases + difficulty_phrases

    # Include user history if authenticated
    if request.user.is_authenticated:
        history_data = BlogHistory.objects.filter(user=request.user)
        history = [history.blog_post.title for history in history_data]
        autocomplete_list = {
            'suggestions': autocomplete_suggestions,
            'history': history
        }
    else:
        autocomplete_list = {
            'suggestions': autocomplete_suggestions
        }

    return {'autocomplete_list': autocomplete_list}


from notifications.models import Notification

def message_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user)
    else:
        notifications = [] 
    return {'notifications': notifications}


def most_searched_recipes(request):
    if request.user.is_authenticated:
        global_rankings = searchedRecipesRanking.objects.values('recipe').annotate(total_searches=Count('user')).order_by('-total_searches')[:5]  # Top 10
        recipes_rankings = post.objects.filter(id__in=[ranking['recipe'] for ranking in global_rankings]).annotate(search_count=Count('recipe_rankings')).order_by('-search_count', '-hit_count_generic__hits','-date_post')
    else:
        recipes_rankings = []
    return {'recipes_rankings':recipes_rankings}

def todays_date(request):
    todays_date = datetime.date.today()
    return {'todays_date':todays_date}