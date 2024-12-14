import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def summarize_text(text):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=text,
            max_tokens=150,  # Adjust as needed
            temperature=0.4,  # Adjust as needed
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error in text summarization: {e}")
        return text 
    

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import post

def get_recommendations(recipe_id, num_recommendations=50):

    recipe = post.objects.get(id=recipe_id)
    
    recipes = list(post.objects.all())
    
    descriptions = [recipe.content for recipe in recipes]
    ingredients = [recipe.ingredients for recipe in recipes]
    
    combined_features = [
        f"{desc} {ingre}"
        for desc, ingre in zip(descriptions, ingredients)
    ]
    
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_features)
    
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    recipe_index = recipes.index(recipe)
    
    similarity_scores = cosine_similarities[recipe_index]
    similar_indices = similarity_scores.argsort()[-(num_recommendations + 1):-1][::-1]
    
    recommended_recipes = [recipes[int(index)] for index in similar_indices]
    
    return recommended_recipes

import requests
from bs4 import BeautifulSoup

API_KEY = settings.SPOONACULAR_API_KEY

def clean_ingredients(html_ingredients):
    soup = BeautifulSoup(html_ingredients, "html.parser")
    cleaned_ingredients = soup.get_text(separator="\n").strip()
    ingredients_list = cleaned_ingredients.splitlines()
    
    formatted_ingredients = "\n".join([ingredient.strip() for ingredient in ingredients_list if ingredient.strip()])
    
    return formatted_ingredients


def get_recipe_nutrition_widget(ingredients):
    cleaned_ingredients = clean_ingredients(ingredients)
    
    url = f"https://api.spoonacular.com/recipes/visualizeNutrition"
    data = {
        'ingredientList': cleaned_ingredients,
        'apiKey': API_KEY,
        'defaultCss': True  
    }

    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None