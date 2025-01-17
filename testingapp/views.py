from email import message
from itertools import product
from multiprocessing import context
from re import T
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect,Http404,HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse
from requests import request
from testingapp.forms import registration_form,post_form,ImageGenerationForm,comment_form, Updatepro,FileModelForm,Updateview,LocationForm,AIRecipeGenerationForm,AIcolorCodeGenerationForm,UseColorFromImageForm,YearlyGoalForm
from .models import comments, profile,RedeemedCredit,CreditHistory,CreditSpentHistory,Follow
from django.views.generic import ListView,DetailView,TemplateView,UpdateView,DeleteView
from django.views.generic.edit import DeleteView
from django.views import generic
from django.db.models import Q
from django.views.decorators.cache import cache_control
from hitcount.views import HitCountDetailView,HitCountMixin
from hitcount.models import HitCount
import datetime
from datetime import date, timedelta
from django.utils import timezone
import math
import json
import urllib.request
from django.core.paginator import Paginator
from .models import post,photo,UserProfile,BlogHistory,Favorite,profile,UserLocation,Feedback,searchedRecipesRanking
from django.http import FileResponse
import io
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.forms import modelformset_factory
import calendar
from django.views.decorators.cache import never_cache
from django.db.models import Count
from decimal import Decimal, InvalidOperation
from django.db.models import Avg, Max, Min, Sum
from hitcount.models import Hit
from django.http.response import JsonResponse
from django.core import serializers
import json
from hitcount.models import HitCount
from django.db.models import Sum
from django.views.generic.edit import CreateView
import calendar
from django.db.models.functions import TruncMonth, TruncYear
from .forms import EmailNotificationForm,FeedbackForm,PreferencesForm,YearlyGoal
from django.utils.translation import activate
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from collections import Counter
from django.core.mail import send_mail
from .forms import SearchForm
from chartjs.views.lines import BaseLineChartView
from .models import post
from django.db.models.functions import Extract
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import ExtractMonth
from translate import Translator
from functools import reduce
from operator import or_
from random import *
from django.contrib.messages import get_messages
from notifications.signals import notify
from notifications.models import Notification
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from allauth.socialaccount.models import SocialAccount
from openai.error import RateLimitError, APIError, InvalidRequestError
from django.contrib.staticfiles import finders
import pdfkit
import qrcode
from qrcode import make, QRCode
from .utils import get_recommendations,get_recipe_nutrition_widget
import re
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from allauth.socialaccount.views import SignupView
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from io import BytesIO
from gtts import gTTS
import os
from pathlib import Path
from django.template.defaultfilters import striptags
import base64
from bs4 import BeautifulSoup
from django.contrib.sessions.models import Session
from PIL import Image
from collections import Counter
import openai
import requests
from django.core.files.base import ContentFile
from urllib import parse
from django.core.files.storage import default_storage
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from b2sdk.v1 import *
from tempfile import NamedTemporaryFile
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import boto3
import time
import google.generativeai as genai

def handling_404(request, exception):
    return render(request, 'testingapp/404.html') 

def extract_colors_from_recipe_image(request, post_photos):

    profile = request.user.userprofile

    if profile.use_colors_from_image:
        extracted_colors = []

        for i, photo_instance in enumerate(post_photos, 1):
            image_path = photo_instance.image.path
            colors = extract_dominant_colors(image_path)
            extracted_colors.extend(colors)

        return extracted_colors if extracted_colors else []
    else:
        return []

# You can define any additional views or logic here if needed for your project

class CustomPasswordResetView(PasswordResetView):
    # Customization for Password Reset View
    template_name = 'testingapp/password_reset_form.html'
    email_template_name = 'testingapp/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    # Customization for Password Reset Done View
    template_name = 'testingapp/password_reset_done.html'
    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    # Customization for Password Reset Confirm View
    template_name = 'testingapp/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'testingapp/password_reset_complete.html'  # Update with your template path

    def get(self, request, *args, **kwargs):
        # Add any additional logic you need here before rendering the view
        return render(request, self.template_name, self.get_context_data())

# You can define any other views or logic specific to your project below


def landingpg(request):
    return render(request,'testingapp/landingpg.html')



@never_cache
@login_required(login_url='login')
def appearance(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':

        if request.POST.get("form_type") == 'colorform':
            primary_color = request.POST.get('primary_color')
            theme = request.POST.get('custom_primary_color')
            user_profile.theme = theme
            user_profile.primary_color = primary_color

            neutral_primary = request.POST.get('neutral_primary')
            user_profile.neutral_primary = neutral_primary

            neutral_secondary = request.POST.get('neutral_secondary')
            user_profile.neutral_secondary = neutral_secondary

            user_profile.save()
            return redirect('appearance')

        elif request.POST.get("form_type") == 'colorform2':
            secondary_color = request.POST.get('secondary_color')
            theme = request.POST.get('custom_secondary_color')
            user_profile.theme = theme
            user_profile.secondary_color = secondary_color

            hover_color = request.POST.get('hover_color')
            user_profile.hover_color = hover_color
            
            active_link_color = request.POST.get('active_link_color')
            user_profile.active_link_color = active_link_color

            user_profile.save()
            return redirect('appearance')
        
        elif request.POST.get("form_type") == 'colorform3':
            tertiary_colors = request.POST.get('tertiary_color')
            theme = request.POST.get('custom_tertiary_color')
            user_profile.theme = theme
            user_profile.tertiary_color = tertiary_colors
            user_profile.save()
            return JsonResponse({'color': tertiary_colors})
            # return redirect('appearance')
        
        if request.POST.get("color_description") == 'colorcode':
            try:

                image_generation_form = AIcolorCodeGenerationForm(request.POST)

                if image_generation_form.is_valid():
                    # Get the title from the image generation form
                    title = image_generation_form.cleaned_data['title']
                    # print(title)

                    # Generating colors paletts using OpenAI API

                    # openai.api_key = settings.OPENAI_API_KEY
                    
                    # color_prompt = f"Convert the following verbal description of a color palette into a set of 2 different palettes with list of 4 hexadecimal color code starting with primary color for cards (this color should be light) , secondary color for background (should be lighter), tertiary color for text (this color should be extremely dark), active link color (this color should be different), additionally generate 3 more color's with first fpr hovering the links (this color should be light), while others should be contrasty first being primary neutral (should be medium light), second being neutral secondary (should be moderately light) : {title}."

                    # # Generate an image based on the user's input
                    # response = openai.Completion.create(
                    #     engine="gpt-3.5-turbo-instruct",
                    #     prompt=color_prompt,  # Use the title as the prompt
                    #     max_tokens=400,
                    #     temperature=0.7,
                    # )

                    # generated_colors = response.choices[0].text.strip()
                    # # print(generated_colors)

                    # if hex_codes:
                    #     return JsonResponse({"generated_colors": hex_codes})

                    '''----------------------------------------------------------------'''

                    # Generating colors paletts using Gemini API
                    genai.configure(api_key=settings.GEMINI_API_KEY)

                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(
                        f"Create four distinct color palettes for a UI design system, with each palette containing at least seven different colors for the following elements: Primary Color (for cards, buttons, etc.), which should be light and stand out against the background; Secondary Color (for the foreground, background on the body, and bootstrap modal), which should be lighter than the primary color and suitable for larger background areas; Tertiary Color (for text color), which should be most darkest to ensure excellent readability against lighter backgrounds; Active Link Color (background color for active links), which should be distinct and different from the primary, secondary, and tertiary colors; Hover Color (for hovering over links, cards, buttons, etc.), which should be light and provide clear visual feedback on interaction; Neutral Primary (a contrasting, punchy color for specific UI elements), which should be medium-light and complement the other colors; and Neutral Secondary (a lighter contrasting color), which should be moderately light and distinct from the neutral primary, ideal for subtle highlights or less dominant UI elements. Each palette should ensure the colors work harmoniously together for a balanced, aesthetically pleasing design suitable for web or app interfaces."
                        f": {title}."
                    )
                    hex_codes = extract_hex_codes(response.text)
                    if hex_codes:
                        return JsonResponse({"generated_colors": ''.join(hex_codes)})
                    else:
                        return JsonResponse({"error": "No hex codes found in the response."})


            except Exception as e:
                error = str(e)
                # print(error)
                return JsonResponse({"error": error})
            
    form = AIcolorCodeGenerationForm()

    user = request.user

    profile = request.user.profile
    if request.method == 'POST':
        form = UseColorFromImageForm(request.POST)
        if form.is_valid():
            use_colors_from_image = form.cleaned_data.get('use_colors_from_image', False)
            # Update the user's email notification preference in the database
            request.user.userprofile.use_colors_from_image = use_colors_from_image
            request.user.userprofile.save()
            return redirect('appearance')
    
    image_color_form = UseColorFromImageForm()

        # elif request.POST.get("dark_form_type") == 'darkform':
        #     primarycolor = request.POST.get('dark_primary_color')
        #     user_profile.primary_color = primarycolor

        #     secondarycolor = request.POST.get('dark_secondary_color')
        #     user_profile.secondary_color = secondarycolor
        
        #     tertiarycolors = request.POST.get('dark_tertiary_color')
        #     user_profile.tertiary_color = tertiarycolors

        #     activelink_color = request.POST.get('dark_active_link_color')
        #     user_profile.active_link_color = activelink_color

        #     hovercolor = request.POST.get('dark_hover_color')
        #     user_profile.hover_color = hovercolor

        #     neutralprimary_color = request.POST.get('dark_neutral_primary')
        #     user_profile.neutral_primary = neutralprimary_color

        #     neutralsecondary_color = request.POST.get('dark_neutral_secondary')
        #     user_profile.neutral_primary = neutralsecondary_color

        #     theme = request.POST.get('dark_theme')
        #     user_profile.theme = theme
        #     user_profile.save()

            # return redirect('appearance')

        # return redirect('appearance')

    return render(request, 'testingapp/appearance.html', {'user_profile': user_profile,'form':form,
                            'image_color_form':image_color_form})
  

def reset_colors(request):
    user_profile = UserProfile.objects.get(user=request.user)
   
    if request.method == 'POST':
        if request.POST.get("default_form_type") == 'defaultform':
            defaultprimary_color = request.POST.get('default_primary_color')
            # print(defaultprimary_color)
            user_profile.primary_color = defaultprimary_color

            defaultsecondary_color = request.POST.get('default_secondary_color')
            user_profile.secondary_color = defaultsecondary_color

            defaulttertiary_color = request.POST.get('default_tertiary_color')
            user_profile.tertiary_color = defaulttertiary_color

            defaultactivelink_color = request.POST.get('default_activelink_color')
            user_profile.active_link_color = defaultactivelink_color

            defaulthover_color = request.POST.get('default_hover_color')
            user_profile.hover_color = defaulthover_color

            defaultneutral_primary = request.POST.get('default_neutral_primary')
            user_profile.neutral_primary = defaultneutral_primary

            defaultneutral_secondary = request.POST.get('default_neutral_secondary')
            user_profile.neutral_secondary = defaultneutral_secondary

            theme = request.POST.get('default_theme')
            user_profile.theme = theme
            # print(theme)
            user_profile.save()

            return JsonResponse({'defaultprimary_color': defaultprimary_color,'defaultsecondary_color':defaultsecondary_color,'theme': theme,
            'defaulttertiary_color':defaulttertiary_color,'defaultactivelink_color':defaultactivelink_color,'defaulthover_color':defaulthover_color})
    
        return render(request, 'testingapp/appearance.html')

    else:
        # these colors are set by default using models.py not by these mentioned below
        user_profile.primary_color = "#DBCBBD"
        user_profile.secondary_color = "#F0ECE3"
        user_profile.tertiary_color = "#221e20"
        user_profile.active_link_color = "#9F8772"
        user_profile.hover_color = "#9C938B"
        user_profile.neutral_primary = "#DFBB9D"
        user_profile.neutral_secondary = "#DBD7CB"
        user_profile.theme = "default_theme"
        user_profile.save()

        return redirect('appearance')


def reset_dark_theme(request):
    user_profile = UserProfile.objects.get(user=request.user)
   
    if request.method == 'POST':
        if request.POST.get("default_dark_form_type") == 'defaultdarkform':
            defdarkprimary_color = request.POST.get('def_dark_primary_color')
            user_profile.primary_color = defdarkprimary_color

            defdarksecondary_color = request.POST.get('def_dark_secondary_color')
            user_profile.secondary_color = defdarksecondary_color

            defdarktertiary_color = request.POST.get('def_dark_tertiary_color')
            user_profile.tertiary_color = defdarktertiary_color

            defdarkactivelink_color = request.POST.get('def_dark_activelink_color')
            user_profile.active_link_color = defdarkactivelink_color

            defdarkhover_color = request.POST.get('def_dark_hover_color')
            user_profile.hover_color = defdarkhover_color

            defdarkneutral_primary = request.POST.get('def_dark_neutral_primary')
            user_profile.neutral_primary = defdarkneutral_primary

            defdarkneutral_secondary = request.POST.get('def_dark_neutral_secondary')
            user_profile.neutral_secondary = defdarkneutral_secondary

            theme = request.POST.get('default_dark_theme')
            user_profile.theme = theme
            # print(theme)
            user_profile.save()

            # return redirect('appearance')


            return JsonResponse({'defdarkprimary_color': defdarkprimary_color,'defdarksecondary_color':defdarksecondary_color,'theme': theme,
            'defdarktertiary_color':defdarktertiary_color,'defdarkactivelink_color':defdarkactivelink_color,'defdarkhover_color':defdarkhover_color})
        
        # return render(request, 'testingapp/appearance.html')

    else:

        user_profile.primary_color = "#414141" 
        user_profile.secondary_color = "#4e4e4e"
        user_profile.tertiary_color = "#D9D9D9"
        user_profile.active_link_color = "#1A5F7A"
        user_profile.hover_color = "#526D82"
        user_profile.neutral_primary = "#4a5eab"
        user_profile.neutral_secondary = "#689ec8"
        user_profile.theme = "default_dark_theme"
        user_profile.save()

        return redirect('appearance')

    
    # user_profile = UserProfile.objects.get(user=request.user)
    # user_profile.primary_color = "#343434"
    # user_profile.secondary_color = "#464646"
    # user_profile.tertiary_color = "#D9D9D9"
    # user_profile.active_link_color = "#6d3b47"
    # user_profile.hover_color = "#766b65"
    # user_profile.theme = "Dark theme"
    # user_profile.save()
    # return redirect('appearance')


def default_color_palette1(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.POST.get("dcp_form_type") == 'dcpcolorform1':
            dcpprimary_color = request.POST.get('dcp_primary_color')
            user_profile.primary_color = dcpprimary_color

            dcpsecondary_color = request.POST.get('dcp_secondary_color')
            user_profile.secondary_color = dcpsecondary_color

            dcptertiary_color = request.POST.get('dcp_tertiary_color')
            user_profile.tertiary_color = dcptertiary_color

            dcpactivelink_color = request.POST.get('dcp_activelink_color')
            user_profile.active_link_color = dcpactivelink_color

            dcphover_color = request.POST.get('dcp_hover_color')
            user_profile.hover_color = dcphover_color

            dcpneutral_primary1 = request.POST.get('dcp_neutral_primary1')
            user_profile.neutral_primary = dcpneutral_primary1

            dcpneutral_secondary1 = request.POST.get('dcp_neutral_secondary1')
            user_profile.neutral_secondary = dcpneutral_secondary1

            theme = request.POST.get('color_scheme_1')
            user_profile.theme = theme
            # print(theme)
            user_profile.save()

            return JsonResponse({'dcpprimary_color': dcpprimary_color,'dcpsecondary_color':dcpsecondary_color,'theme': theme,
            'dcptertiary_color':dcptertiary_color,'dcpactivelink_color':dcpactivelink_color,'dcphover_color':dcphover_color})
    
        elif request.POST.get("dcp_form_type") == 'dcpcolorform2':
            dcpprimary_color2 = request.POST.get('dcp_primary_color2')
            user_profile.primary_color = dcpprimary_color2

            dcpsecondary_color2 = request.POST.get('dcp_secondary_color2')
            user_profile.secondary_color = dcpsecondary_color2

            dcptertiary_color2 = request.POST.get('dcp_tertiary_color2')
            user_profile.tertiary_color = dcptertiary_color2

            dcpactivelink_color2 = request.POST.get('dcp_activelink_color2')
            user_profile.active_link_color = dcpactivelink_color2

            dcphover_color2 = request.POST.get('dcp_hover_color2')
            user_profile.hover_color = dcphover_color2

            dcpneutral_primary2 = request.POST.get('dcp_neutral_primary2')
            user_profile.neutral_primary = dcpneutral_primary2

            dcpneutral_secondary2 = request.POST.get('dcp_neutral_secondary2')
            user_profile.neutral_secondary = dcpneutral_secondary2

            theme_two = request.POST.get('color_scheme_2')
            user_profile.theme = theme_two

            user_profile.save()

            return JsonResponse({'dcpprimary_color2': dcpprimary_color2,'dcpsecondary_color2':dcpsecondary_color2,'dcptertiary_color2':dcptertiary_color2,
            'dcpactivelink_color2':dcpactivelink_color2,'dcphover_color2':dcphover_color2,'theme_two': theme_two})
        
        elif request.POST.get("dcp_form_type") == 'dcpcolorform3':
            dcpprimary_color3 = request.POST.get('dcp_primary_color3')
            user_profile.primary_color = dcpprimary_color3

            dcpsecondary_color3 = request.POST.get('dcp_secondary_color3')
            user_profile.secondary_color = dcpsecondary_color3

            dcptertiary_color3 = request.POST.get('dcp_tertiary_color3')
            user_profile.tertiary_color = dcptertiary_color3

            dcpactivelink_color3 = request.POST.get('dcp_activelink_color3')
            user_profile.active_link_color = dcpactivelink_color3

            dcphover_color3 = request.POST.get('dcp_hover_color3')
            user_profile.hover_color = dcphover_color3

            dcpneutral_primary3 = request.POST.get('dcp_neutral_primary3')
            user_profile.neutral_primary = dcpneutral_primary3

            dcpneutral_secondary3 = request.POST.get('dcp_neutral_secondary3')
            user_profile.neutral_secondary = dcpneutral_secondary3

            theme = request.POST.get('color_scheme_3')
            user_profile.theme = theme

            user_profile.save()

            return JsonResponse({'dcpprimary_color3': dcpprimary_color3,'dcpsecondary_color3':dcpsecondary_color3,'theme':theme,
            'dcptertiary_color3':dcptertiary_color3,'dcpactivelink_color3':dcpactivelink_color3,'dcphover_color3':dcphover_color3})
        
        elif request.POST.get("dcp_form_type") == 'dcpcolorform4':
            dcpprimary_color4 = request.POST.get('dcp_primary_color4')
            user_profile.primary_color = dcpprimary_color4

            dcpsecondary_color4 = request.POST.get('dcp_secondary_color4')
            user_profile.secondary_color = dcpsecondary_color4

            dcptertiary_color4 = request.POST.get('dcp_tertiary_color4')
            user_profile.tertiary_color = dcptertiary_color4

            dcpactivelink_color4 = request.POST.get('dcp_activelink_color4')
            user_profile.active_link_color = dcpactivelink_color4

            dcphover_color4 = request.POST.get('dcp_hover_color4')
            user_profile.hover_color = dcphover_color4

            user_profile.save()

            return JsonResponse({'dcpprimary_color4': dcpprimary_color4,'dcpsecondary_color4':dcpsecondary_color4,
            'dcptertiary_color4':dcptertiary_color4,'dcpactivelink_color4':dcpactivelink_color4,'dcphover_color4':dcphover_color4})




        elif request.POST.get("dark_form_type1") == 'darkform1':
            darkprimary_color = request.POST.get('dark_primary_color')
            user_profile.primary_color = darkprimary_color

            darksecondary_color = request.POST.get('dark_secondary_color')
            user_profile.secondary_color = darksecondary_color

            darktertiary_color = request.POST.get('dark_tertiary_color')
            user_profile.tertiary_color = darktertiary_color

            darkactivelink_color= request.POST.get('dark_activelink_color')
            user_profile.active_link_color = darkactivelink_color

            darkhover_color = request.POST.get('dark_hover_color')
            user_profile.hover_color = darkhover_color

            darkneutral_primary = request.POST.get('dark_neutral_primary')
            user_profile.neutral_primary = darkneutral_primary

            darkneutral_secondary = request.POST.get('dark_neutral_secondary')
            user_profile.neutral_secondary = darkneutral_secondary

            theme = request.POST.get('dark_theme1')
            user_profile.theme = theme

            user_profile.save()

            return JsonResponse({'darkprimary_color': darkprimary_color,'darksecondary_color':darksecondary_color,'theme':theme,
            'darktertiary_color':darktertiary_color,'darkactivelink_color':darkactivelink_color,'darkhover_color':darkhover_color})
    



        # ai colors
        elif request.POST.get("ai_color_palette").startswith('aiform'):
            # 7 colors in each form palette
            for i in range(1, 8):
                color_key = f'ai_color{i}'
                color_value = request.POST.get(color_key)

                # Handle each color_value as needed, for example:
                if color_key == 'ai_color1':
                    user_profile.primary_color = color_value
                elif color_key == 'ai_color2':
                    user_profile.secondary_color = color_value
                elif color_key == 'ai_color3':
                    user_profile.tertiary_color = color_value
                elif color_key == 'ai_color4':
                    user_profile.active_link_color = color_value
                elif color_key == 'ai_color5':
                    user_profile.hover_color = color_value
                elif color_key == 'ai_color6':
                    user_profile.neutral_primary = color_value
                elif color_key == 'ai_color7':
                    user_profile.neutral_secondary = color_value

            theme = request.POST.get('ai_theme')
            user_profile.theme = theme


            user_profile.save()

        
        elif request.POST.get("ai_color_palette") == 'saved_ai_form':
            aiprimary_color = request.POST.get('ai_primary_color')
            user_profile.primary_color = aiprimary_color

            aisecondary_color = request.POST.get('ai_secondary_color')
            user_profile.secondary_color = aisecondary_color

            aitertiary_color = request.POST.get('ai_tertiary_color')
            user_profile.tertiary_color = aitertiary_color

            aiactivelink_color= request.POST.get('ai_activelink_color')
            user_profile.active_link_color = aiactivelink_color

            aihover_color = request.POST.get('ai_hover_color')
            user_profile.hover_color = aihover_color

            aineutral_primary = request.POST.get('ai_neutral_primary')
            user_profile.neutral_primary = aineutral_primary

            aineutral_secondary = request.POST.get('ai_neutral_secondary')
            user_profile.neutral_secondary = aineutral_secondary

            theme = request.POST.get('ai_color_scheme')
            user_profile.theme = theme

            user_profile.save()
            return JsonResponse({'theme':theme})
        


    return render(request, 'testingapp/appearance.html')
        

def recipes_ranking(recipe, user):
    # Get or create the ranking for this recipe and user
    ranking_exists = searchedRecipesRanking.objects.filter(recipe=recipe, user=user).exists()
    
    if not ranking_exists:
        searchedRecipesRanking.objects.create(recipe=recipe, user=user)

import operator
# Search recipes 
def searchresults_view(request):
    
    # form = SearchForm(request.GET)
    # query = form['query'].value() if 'query' in form else ''

    query = request.GET.get('query', '').strip().lower().replace("non veg", "non-veg")
    all_recipes = post.objects.filter().all()
    recipe_results = None

    type_filter = request.GET.get('type', '').strip()
    cuisine_filter = request.GET.get('cuisine', '').strip()
    category_filter = request.GET.get('category', '').strip()
    timing_filter = request.GET.get('timing', '').strip()
    difficulty_filter = request.GET.get('difficulty', '').strip()
    servings_filter = request.GET.get('servings', '').strip()

    filter_values = {
        'type': request.GET.get('type', ''),
        'cuisine': request.GET.get('cuisine', ''),
        'timing': request.GET.get('timing', ''),
        'category': request.GET.get('category', ''),
        'difficulty': request.GET.get('difficulty', ''),
        'servings': request.GET.get('servings', '')
    }

    pages = {
        "new recipe": 'createpost',
        "liked recipes": 'liked_recipes',
        "disliked recipes": 'disliked_recipes',
        "home": 'home',
        "profile": 'profile',
        "trending": 'trending',
        "dashboard": 'dashboard',
        "credits": 'credits',
        "explore": 'explore',
        "timeline": 'timeline',
        "favourites": 'favourites',
        "history": 'blog_history',
        "appearance": 'appearance',
        "account settings": 'account_settings',
        "update profile": 'updateprofile',
        "views": 'total_views',
        "network": 'connections',
        "kitchenai": 'generate_recipe'
    }
    
    for key, url in pages.items():
        if query.startswith(key.lower()):
            return redirect(url)

    if query:
        
        cuisines = ['Indian', 'American', 'Italian']

        timing_match = re.search(r'\b(?:under|ready\s*in)?\s*(\d+)\s*(?:minutes|min|mins)?\b', query, re.IGNORECASE)
        category_match = re.search(r'\b(veg|non-veg|nonveg|vegetarian|nonvegetarian)\b', query, re.IGNORECASE)
        cuisine_match = re.search(r'\b(' + '|'.join(cuisines) + r')\b', query, re.IGNORECASE)

        filter_conditions = Q()

        if type_filter or cuisine_filter or category_filter or timing_filter or difficulty_filter or servings_filter:

            if type_filter:
                filter_conditions &= Q(type__iexact=type_filter.capitalize())
            
            if cuisine_filter:
                filter_conditions &= Q(cuisine__iexact=cuisine_filter.capitalize())
            
            if category_filter:
                filter_conditions &= Q(category__iexact=category_filter.capitalize())

            if timing_filter:
                try:
                    timing_value = int(timing_filter)
                    filter_conditions &= Q(timing__lte=timing_value)
                except ValueError:
                    pass  

            if difficulty_filter:
                filter_conditions &= Q(difficulty__iexact=difficulty_filter.capitalize())
            
            if servings_filter:
                try:
                    servings_value = int(servings_filter)
                    filter_conditions &= Q(servings__lte=servings_value)
                except ValueError:
                    pass
            
            recipe_results = post.objects.filter(filter_conditions)
        else:
            # if "cuisine" or "cuisines" at the end of the query
            if cuisine_match:
                cuisine_value = cuisine_match.group(1).capitalize()
                if query.strip().lower().endswith('cuisines'):
                    cuisine_value = f"{cuisine_value} cuisine"

                elif not query.strip().lower().endswith('cuisine'):
                    cuisine_value = f"{cuisine_value} cuisine"
                
                elif query.strip().lower().endswith('cuisine'):
                    cuisine_value = f"{cuisine_value} cuisine"
            else:
                cuisine_value = None 

            if timing_match and category_match:
                timing_value = int(timing_match.group(1))

                category_value = category_match.group(1).replace("vegetarian", "veg").replace("nonvegetarian", "non-veg").replace("nonveg", "non-veg").capitalize()
                recipe_results = post.objects.filter(
                    Q(category__iexact=category_value) & Q(timing__lte=timing_value)
                )

            elif category_match and cuisine_value:
                category_value = category_match.group(1).replace("vegetarian", "veg").replace("nonvegetarian", "non-veg").replace("nonveg", "non-veg").capitalize()

                recipe_results = post.objects.filter(
                    Q(category__iexact=category_value) & Q(cuisine__iexact=cuisine_value)
                )

            elif timing_match and cuisine_value:
                timing_value = int(timing_match.group(1))

                recipe_results = post.objects.filter(
                    Q(cuisine__iexact=cuisine_value) & Q(timing__lte=timing_value)
                )

            elif timing_match and category_match and cuisine_value:
                timing_value = int(timing_match.group(1))
                category_value = category_match.group(1).replace("vegetarian", "veg").replace("nonvegetarian", "non-veg").replace("nonveg", "non-veg").capitalize()

                recipe_results = post.objects.filter(
                    Q(category__iexact=category_value) & Q(cuisine__iexact=cuisine_value) & Q(timing__lte=timing_value)
                )

            elif cuisine_match:
                recipe_results = post.objects.filter(Q(cuisine__iexact=cuisine_value))

            elif timing_match:
                timing_value = int(timing_match.group(1))
                if "under" in query.lower() or "ready in" in query.lower():
                    recipe_results = post.objects.filter(timing__lte=timing_value)
                else:
                    recipe_results = post.objects.filter(timing=timing_value)

            elif query in ["veg", "veg recipe", "veg recipes"]:
                recipe_results = post.objects.filter(Q(category__iexact='Veg'))

            elif query in ["non-veg", "non-veg recipe", "non-veg recipes"]:
                recipe_results = post.objects.filter(Q(category__iexact='Non-Veg'))

            elif any(term in query for term in ["Snacks recipes", "snacks"]):
                recipe_results = post.objects.filter(Q(type__icontains='Evening Snack'))

            elif query.startswith("cooking difficulty"):
                difficulty_level = query.replace("cooking difficulty", "").strip()
                recipe_results = post.objects.filter(Q(difficulty__icontains=difficulty_level))

            else:
                common_words = {"recipe", "recipes", "food"}
                normalized_query = query.lower().replace("non veg", "non-veg")
                terms = [term for term in normalized_query.split() if term not in common_words]

                q_objects = []

                for term in terms:
                    clean_term = term.replace("-", "").replace(" ", "").lower()

                    if clean_term in ["veg", "vegetarian"]:
                        q_objects.append(Q(category__iexact="Veg"))
                        
                    elif clean_term in ["nonveg", "nonvegetarian"]:
                        q_objects.append(Q(category__iexact="Non-Veg"))

                    elif term in ["breakfast", "lunch", "dinner", "evening snack"]:
                        q_objects.append(Q(type__iexact=term.capitalize()))
                    
                    elif term in ["easy", "medium", "hard"]:
                        q_objects.append(Q(difficulty__iexact=term))

                if q_objects:
                    recipe_results = post.objects.filter(reduce(operator.and_, q_objects))

        if recipe_results is None:
            # Perform search query on the Recipe model
            recipe_results = post.objects.filter(
                reduce(or_, [
                    Q(title__icontains=query),
                    # Q(ingredients__icontains=query),
                    # Q(content__icontains=query),
                    Q(author__username__icontains=query),
                    Q(cuisine__iexact=query),
                    Q(cuisine__icontains=query),
                    Q(type__icontains=query),
                    Q(difficulty__icontains=query),
                    Q(author__first_name__icontains=query),
                    Q(author__last_name__icontains=query)
                ])
            ).annotate(search_count=Count('recipe_rankings')).order_by('-search_count', '-hit_count_generic__hits','-date_post')

        profile_results = User.objects.filter(
            reduce(or_, [
                Q(email__icontains=query) | 
                Q(first_name__icontains=query.split()[0]) | 
                Q(last_name__icontains=query.split()[-1])
            ])
        )

        is_following = {}
        for user in profile_results:
            if request.user.is_authenticated:
                user_exists = Follow.objects.filter(follower=request.user, following=user).exists()
                is_following[user.username] = user_exists

        # Combine the results from both models
        results = list(recipe_results) + list(profile_results)

        # Update the search ranking for each recipe found
        for recipe in recipe_results:
            if request.user.is_authenticated:
                recipes_ranking(recipe, request.user)

   
    else:
        # recipe_results = []
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request,'testingapp/searchresults.html',{'results': results, 'recipe_results':recipe_results,
    "query":query,'all_recipes':all_recipes,'profile_results': profile_results,'is_following':is_following,'filter_values':filter_values})


from urllib.parse import urljoin
@login_required(login_url='login')
def customer_render_pdf_view(request,feed,pk, *args, **kwargs):    
    recipes = get_object_or_404(post,title=feed)

    recipe_images = photo.objects.filter(feed=recipes)

    if settings.ENVIRONMENT == 'True':
        if recipe_images.exists():
            pdf_recipe_image_url = recipe_images.first().image.url
        else:
            pdf_recipe_image_url = None

        if recipes.author and recipes.author.profile.profile_img:
            profile_image_path = recipes.author.profile.profile_img.url
            pdf_profile_image_url = urljoin('file://', profile_image_path)
        else:
            pdf_profile_image_url = None 
    else:
            if recipe_images.exists():
                pdf_recipe_image_url = recipe_images.first().image.path
            else:
                pdf_recipe_image_url = None

            if recipes.author and recipes.author.profile.profile_img:
                profile_image_path = recipes.author.profile.profile_img.path
                pdf_profile_image_url = urljoin('file://', profile_image_path)
            else:
                pdf_profile_image_url = None 

    nutrition_info = None

    query = recipes.title

    if query:

        try:
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
            api_request =  requests.get(api_url + query, headers = {'X-Api-Key': settings.NUTRITION_API_KEY})
            api_data = json.loads(api_request.content)
            
            if api_request.status_code == 200:
                nutrition_info = api_data
                
            else:
                nutrition_info_error = 'Error occurred'

        except ConnectionError:
            nutrition_info_error = 'Could not connect to Api'

        except Exception as e:
            api = "Error occured"
            nutrition_info_error = 'Error'

    html_content = render_to_string('testingapp/viewpdf.html', {'recipes': recipes,'pdf_recipe_image_url':pdf_recipe_image_url,
    'nutrition_info':nutrition_info,'pdf_profile_image_url':pdf_profile_image_url})

    css = finders.find('testingapp/pdf_recipe.css')
    
    # path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'

    # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    options = {
        'enable-local-file-access': None
    }
    
    pdf = pdfkit.from_string(html_content, False, options=options, css=[css])
   
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="recipe.pdf"'
    
    return response



def aa_view(request, api_key, location):

    curmonth = datetime.datetime.today().month

    if request.method == 'POST':
        city = request.POST['location']
        
        location = city.replace(' ', '+')
        api_key = settings.OPENWEATHERMAP_API_KEY
        
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+location+'&mode=json&units=metric&appid='+api_key).read()
        json_data = json.loads(res)

    
        data = {
            "temp" : int(json_data['main']['temp']),
            "des" : str(json_data['weather'][0]['main']), #"des" : str(json_data['weather'][0]['description']),
            "location": str(json_data['name']),
            "wind_speed": int(json_data['wind']['speed']),
            "feels_like": int(json_data['main']['feels_like']),
            "min" : int(json_data['main']['temp_min']),
            "max" : int(json_data['main']['temp_max']),
            "icon": str(json_data['weather'][0]['icon']),
            # "country_code" : str(json_data['sys']['country']),
            # "coordinate" : str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
            # "cld" : str(json_data['clouds']['all']),
            # "pressure" : str(json_data['main']['pressure']),
            "humidity" : str(json_data['main']['humidity']),
        }  
        
    else:
        
        data = {} 

    return data




def save_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            api_key = settings.OPENWEATHERMAP_API_KEY

            # Update the user's location in the database
            user_profile, created = UserLocation.objects.get_or_create(user=request.user)
            user_profile.location = location
            user_profile.save()

            # Update the weather data for the user's location
            weather_data = aa_view(request, api_key, location)  # Pass the location parameter
            if weather_data:
                user_profile.weather_data = weather_data
                user_profile.save()


            response_data = {
            'form': form,
            'weather_data': weather_data,  
            'user': request.user
            }
        
            return JsonResponse({'weather_data': weather_data})
    else:
        form = LocationForm()

    return render(request, 'testingapp/home.html', {'form': form})




def login_view(request):
    user = request.user

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request,username = email,password = password)
        if user is not None:
            login(request,user = user)
            if user.is_authenticated:

                last_login_date = user.last_login.date()
                current_date = datetime.date.today()
                dates_diff = last_login_date + timedelta(days=15)
                
                if current_date >= dates_diff:
                    messages.success(request, 'Welcome back, {}'.format(user.first_name), extra_tags='welcome-back-message')
                    
            return redirect('home')

        elif email is None: 
            messages.error(request,"Invalid username")

        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')

    return render(request,'testingapp/login.html')     


# redirecting user to login page if singing up using email which already exists
User = get_user_model()

class CustomSocialSignupView(SignupView):
    def dispatch(self, request, *args, **kwargs):
        sociallogin = self.request.session.get('socialaccount_sociallogin')
        if sociallogin:
            email = sociallogin['user']['email']
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                request.session['existing_user_first_name'] = existing_user.first_name
                request.session['existing_user_email'] = existing_user.email
                return redirect(reverse('login'))
        
        return super().dispatch(request, *args, **kwargs)


# clearing the session variable
class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        request.session.pop('existing_user_fullname', None)
        request.session.pop('existing_user_email', None)

        return super().get(request, *args, **kwargs)



def topostlogin(request,pk):
    recipes = post.objects.get(pk=pk)

    img = recipes.photo_set.first()

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request,username = email,password = password)
        if user is not None:
            login(request,user = user)
            return redirect('viewpost',pk)

        elif email is None: 
            messages.error(request,"Invalid username")

        else:
            messages.error(request,"Invalid username or password")
            return redirect('topostlogin',pk)

    return render(request,'testingapp/topostlogin.html',{'recipes':recipes,'img':img})    




# def send_welcome_email(email, name):
#     subject = 'Welcome to Yummy Recipes'
#     message = f'Hi {name}, welcome to Yummy Recipes! We are excited to have you on board.'
#     from_email = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [email]

#     send_mail(subject, message, from_email, recipient_list)

def send_welcome_email(request, email, name):
    subject = 'Welcome to Yummy Recipes'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    context = {
        'name': name,
    }

    html_content = render_to_string('testingapp/welcome_email.html', context)

    email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")

    email.send()



def signup_view(request):
    form = registration_form()

    if request.method == "POST":
        form = registration_form(request.POST)
        if form.is_valid():
            if not form.user_exit():
                form.save()
                
                email = form.cleaned_data['email']
                name = form.cleaned_data['fname']

                # Send the welcome email with the user's name (uncomment below line to send email)
                send_welcome_email(request, email, name)

                
                return redirect('login')
            else:
                messages.set_level(request,messages.DEBUG)
                messages.error(request,"username already exists!!!!")

                return redirect('signup')

    return render(request,'testingapp/signup.html',{'form':form})
    



@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    return redirect('login')



class postListView(HitCountMixin,ListView):
    model = post
    template_name = 'testingapp/explore.html'
    ordering = ['-date_post']
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(postListView, self).get_context_data(**kwargs)

        tot_posts_byuser = 0
        all_recipes = post.objects.filter().all()           

        if self.request.user.is_authenticated:
            all = post.objects.all().order_by('-date_post')
            brkfst = post.objects.filter(type ='Breakfast').order_by('-date_post')
            lnch = post.objects.filter(type ='Lunch').order_by('-date_post')
            snack = post.objects.filter(type ='Evening Snack').order_by('-date_post')
            dnr = post.objects.filter(type ='Dinner').order_by('-date_post')
            
            veg = post.objects.filter(category='Veg').order_by('-date_post')
            vegbrkfst = post.objects.filter(category='Veg',type='Breakfast').order_by('-date_post')
            veglnch = post.objects.filter(category='Veg',type='Lunch').order_by('-date_post')
            vegsnck  = post.objects.filter(category='Veg',type='Evening Snack').order_by('-date_post')
            vegdnr = post.objects.filter(category='Veg',type='Dinner').order_by('-date_post')


            non_veg = post.objects.filter(category='Non-Veg').order_by('-date_post')
            non_vegbrkfst = post.objects.filter(category='Non-Veg',type='Breakfast').order_by('-date_post')
            non_veglnch = post.objects.filter(category='Non-Veg',type='Lunch').order_by('-date_post')
            non_vegsnck  = post.objects.filter(category='Non-Veg',type='Evening Snack').order_by('-date_post')
            non_vegdnr = post.objects.filter(category='Non-Veg',type='Dinner').order_by('-date_post')


            counts = post.objects.order_by('-hit_count_generic__hits')
            titles = post.objects.all()

            user = self.request.user    

            tot_posts_byuser = post.objects.filter(author=user).all().count()

            allrecipes = post.objects.all().order_by('-date_post').all().count()

            blog_history = BlogHistory.objects.filter(user=user)

            blog_posts = [(entry.pk ,entry.blog_post) for entry in blog_history]

            post_count = []

            for pk,history in blog_posts:
                post_count.append(history.pk)

            historys_pk = [*set(post_count)]
        
        else:
            all = post.objects.all().order_by('-date_post')
            brkfst = post.objects.filter(type ='Breakfast').order_by('-date_post')
            lnch = post.objects.filter(type ='Lunch').order_by('-date_post')
            snack = post.objects.filter(type ='Evening Snack').order_by('-date_post')
            dnr = post.objects.filter(type ='Dinner').order_by('-date_post')
            
            veg = post.objects.filter(category='Veg').order_by('-date_post')
            vegbrkfst = post.objects.filter(category='Veg',type='Breakfast').order_by('-date_post')
            veglnch = post.objects.filter(category='Veg',type='Lunch').order_by('-date_post')
            vegsnck  = post.objects.filter(category='Veg',type='Evening Snack').order_by('-date_post')
            vegdnr = post.objects.filter(category='Veg',type='Dinner').order_by('-date_post')


            non_veg = post.objects.filter(category='Non-Veg').order_by('-date_post')
            non_vegbrkfst = post.objects.filter(category='Non-Veg',type='Breakfast').order_by('-date_post')
            non_veglnch = post.objects.filter(category='Non-Veg',type='Lunch').order_by('-date_post')
            non_vegsnck  = post.objects.filter(category='Non-Veg',type='Evening Snack').order_by('-date_post')
            non_vegdnr = post.objects.filter(category='Non-Veg',type='Dinner').order_by('-date_post')

            counts = post.objects.order_by('-hit_count_generic__hits')
            titles = post.objects.all()

            
            allrecipes = post.objects.all().order_by('-date_post').all().count()

            historys_pk = 0

            
        
        trnposts = post.objects.order_by('-hit_count_generic__hits') [0:4]


        


        jan = post.objects.filter(date_post__month='01')
        feb = post.objects.filter(date_post__month='02')
        mar = post.objects.filter(date_post__month='03')
        apr = post.objects.filter(date_post__month='04')
        may = post.objects.filter(date_post__month='05')
        june = post.objects.filter(date_post__month='06')
        july = post.objects.filter(date_post__month='07')
        aug = post.objects.filter(date_post__month='08')
        sep = post.objects.filter(date_post__month='09')
        oct = post.objects.filter(date_post__month='10')
        nov = post.objects.filter(date_post__month='11')
        dec = post.objects.filter(date_post__month='12')


        context = {"all":all,"all_recipes":all_recipes,"brkfst": brkfst,"lnch": lnch,"snack":snack,"dnr":dnr,
        "counts":counts,"titles":titles,"veg":veg,"non_veg":non_veg,
        "vegbrkfst":vegbrkfst,"veglnch":veglnch,"vegsnck":vegsnck,"vegdnr":vegdnr,
        "non_vegbrkfst":non_vegbrkfst,"non_veglnch":non_veglnch,"non_vegsnck":non_vegsnck,"non_vegdnr":non_vegdnr,
        "tot_posts_byuser":tot_posts_byuser,"allrecipes":allrecipes,"trnposts":trnposts,
        'jan':jan,'feb':feb,'mar':mar,'apr':apr,'may':may,'june':june,
        'july':july,'aug':aug,'sep':sep,'oct':oct,'nov':nov,'dec':dec,'historys_pk':historys_pk}
        return context


def scroll(request):
    return render(request, 'testingapp/scroll.html')


def recipe_recommendations(title, cosine_sim, indices, posts_df):
    indx = indices[title]
    sim_scores = list(enumerate(cosine_sim[indx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:10]  # Get top 10 recommendations
    post_indices = [i[0] for i in sim_scores]
    return posts_df.iloc[post_indices]


from hitcount.models import HitCount, Hit
class dashpostview(LoginRequiredMixin, ListView):
    model = post
    template_name = 'testingapp/home.html'
    ordering = ['-date_post']
    context_object_name = 'posts'
    count_hit = True


    def get_queryset(self):
        user = self.request.user
        return post.objects.filter(author=user)
    
    def get_context_data(self, **kwargs):
        context = super(dashpostview, self).get_context_data(**kwargs)
        user = self.request.user

        all_urecipe = post.objects.all().order_by('-date_post','-hit_count_generic__hits')

        hour = datetime.datetime.now().hour

        brkfst = post.objects.filter(type ='Breakfast').order_by('-hit_count_generic__hits','-date_post')
        lnch = post.objects.filter(type ='Lunch').order_by('-hit_count_generic__hits','-date_post')
        evesnack = post.objects.filter(type ='Evening Snack').order_by('-hit_count_generic__hits','-date_post')
        dnr = post.objects.filter(type ='Dinner').order_by('-hit_count_generic__hits','-date_post')


        end_date = datetime.datetime.now()
        start_date = end_date - timedelta(days=7)
        
        user = self.request.user
        feed = self.request.user

        # Check if there is a success message in the session (for successful recipe form submission)
        success_text = self.request.session.pop('success_message', None)

        # context['liked_message'] = get_messages(self.request)

        # stored_message = self.request.session.get('stored_messages', [])
        # print(stored_message)  

        # notifications = Notification.objects.filter(recipient=user)
        # print(notifications)

        joined = user.date_joined.date()
        today = datetime.date.today()

        curyear = datetime.datetime.today().year

        # all = post.objects.filter(author=user).all().order_by('-date_post')[0:3] #showing recipes posted by specific user (remove author=user) to show all recipes posted by all users
        
        all = post.objects.filter(author=user).order_by('-date_post')

        blog_history = BlogHistory.objects.filter(user=user)

        blog_posts = [(entry.pk ,entry.blog_post) for entry in blog_history]

        post_count = []

        for pk,history in blog_posts:
            post_count.append(history.pk)

        historys_pk = [*set(post_count)]

        item_counts = Counter(post_count)

        l = []
        for item, count in item_counts.items():
            if count > 1:
                l.append(f"{item}: {count}")

        date = datetime.date.today()
        day = datetime.date.today().day
        month = datetime.date.today().month

        spotlight_list = []
        
        for count,i in enumerate(all,1):
            if i.date_post.day == date.day and i.date_post.month == date.month:
                spotlight_list.append(i)
                
                # if date_post.day == date.day and date_post.month == date.month

        all_recipes = post.objects.filter().all()

        tot_post_byuser = post.objects.filter(author=user).all().count()

        year_recap = post.objects.filter(author=user,date_post__year = curyear).all()

        next_day_brkfst = post.objects.filter(type ='Breakfast').order_by('-date_post','-hit_count_generic__hits')

        similar_rice_recipes = post.objects.all().order_by('-date_post','-hit_count_generic__hits')

        rice_recipe_list = []
        panner_recipe_list = []

        for i in similar_rice_recipes:
            if 'rice' in i.title:
                rice_recipe_list.append(i)
            
            elif 'panner' in i.title:
                panner_recipe_list.append(i)

        
        # brkfst = post.objects.filter(type ='Breakfast').order_by('-hit_count_generic__hits','-date_post')
        # lnch = post.objects.filter(type ='Lunch').order_by('-hit_count_generic__hits','-date_post')
        # evesnack = post.objects.filter(type ='Evening Snack').order_by('-hit_count_generic__hits','-date_post')
        # dnr = post.objects.filter(type ='Dinner').order_by('-hit_count_generic__hits','-date_post')

        brkfst_count = post.objects.filter(type ='Breakfast').count()
        lnch_count = post.objects.filter(type ='Lunch').count()
        evesnack_count = post.objects.filter(type ='Evening Snack').count()
        dnr_count = post.objects.filter(type ='Dinner').count()



        test = post.objects.filter(title = 'Dosa').order_by('-hit_count_generic__hits','-date_post')

        titles = post.objects.all()

        #getting current date,time,hour, month in integer, month in string
        date = datetime.date.today()
        time = datetime.datetime.now().time
        hour = datetime.datetime.now().hour
        sec = timezone.now()
        monthint = datetime.datetime.today().month
        mmonth = datetime.date.today()
        monthstr = mmonth.strftime('%B')

        lastrecipe = post.objects.filter(author=user).last()

        diff = 0
        seconds = 0
        minutes = 0
        days = 0
        hours = 0
        months = 0
        years = 0
        

        if lastrecipe:
            diff = sec - lastrecipe.date_post

            if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                seconds = diff.seconds
        
            if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes = math.floor(diff.seconds/60)

            if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours = math.floor(diff.seconds/3600)

            if diff.days >= 1 and diff.days < 30:
                days = diff.days
            
            if diff.days >= 30 and diff.days < 365:
                months = math.floor(diff.days/30)
            
            if diff.days >= 365:
                years= math.floor(diff.days/365)
        
        # Popular recipe of the week
            
        today = timezone.now()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)

        # Filter hits within the current week
        hits_this_week = Hit.objects.filter(created__range=[start_of_week, end_of_week])

        # Get the postID and their hit counts within the week
        post_hit_counts = (
            HitCount.objects
            .filter(hit__in=hits_this_week)
            .values('object_pk')
            .annotate(hit_count=Count('pk'))
        )

        # recipes by hit count in descending order
        sorted_post_ids = sorted(post_hit_counts, key=lambda x: x['hit_count'], reverse=True)

        popular_recipe = []
        for item in sorted_post_ids:
            post_id = item['object_pk']
            popular_post = post.objects.get(pk=post_id)
            hits_on_popular_post = (popular_post, item['hit_count'])
            # print(hits_on_popular_post)
            popular_recipe.append((popular_post))

        pks = post.objects.all().order_by('-date_post','-hit_count_generic__hits').values_list('pk', flat=True)
        
        if pks:
            random_pk = choice(pks)
            random_obj = post.objects.get(pk=random_pk)
        else:
            random_obj = None

        #paginator

        #Breakfast (auth = user)    
        brkfst_pagint = Paginator(brkfst, 10)
        brkfst_p = self.request.GET.get('breakfastpage')
        breakfastpage = brkfst_pagint.get_page(brkfst_p)

        tbrkfst = breakfastpage.paginator.num_pages

        #Lunch
        lnch_pagint = Paginator(lnch, 10)
        lnch_p = self.request.GET.get('lunchpage')
        lunchpage = lnch_pagint.get_page(lnch_p)

        tlnch = lunchpage.paginator.num_pages

        #Evening snack
        evesnack_pagint = Paginator(evesnack, 10)
        evesnack_p = self.request.GET.get('eveningsnackupage')
        eveningsnackupage = evesnack_pagint.get_page(evesnack_p)

        tevesnack = eveningsnackupage.paginator.num_pages


        # Dinner 
        dnr_pagint = Paginator(dnr, 10)
        dnr_p = self.request.GET.get('dinnerpage')
        dinnerpage = dnr_pagint.get_page(dnr_p)

        tdnr = dinnerpage.paginator.num_pages


        # all recipes by all users
        recipe_paginator = Paginator(all_urecipe, 4) #4 is no. of recipes showing at a time
        page_num = self.request.GET.get('allusrrecipe')
        allusrrecipe = recipe_paginator.get_page(page_num)
        
        total_p = allusrrecipe.paginator.num_pages

         # total_p = "1" * page.paginator.num_pages  #for for loop to work    

        trending_recipes = post.objects.order_by('-hit_count_generic__hits')

        tot_posts_byuser = post.objects.filter(author=user).all().count()
        allrecipes = post.objects.all().order_by('-date_post').all().count()
        trnposts = post.objects.order_by('-hit_count_generic__hits') [0:4]
        
        form = SearchForm(self.request.GET)
        
        current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

        # recipe recommendations
        recipes = post.objects.filter().all()
        
        posts_df = pd.DataFrame(list(recipes.values('id', 'title', 'type', 'cuisine', 'category', 'difficulty', 'content', 'ingredients', 'servings', 'timing')))
        
        if not posts_df.empty:
            posts_df['content'] = posts_df[['type', 'cuisine', 'category', 'difficulty', 'content', 'ingredients']].apply(lambda x: ' '.join(x), axis=1)

            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(posts_df['content'])

            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

            indices = pd.Series(posts_df.index, index=posts_df['title']).drop_duplicates()
            most_viewed_recipe = post.objects.order_by('-hit_count_generic__hits').first()
            recommended_recipes = recipe_recommendations(title=most_viewed_recipe.title, cosine_sim=cosine_sim, indices=indices, posts_df=posts_df)
            recommended_recipes_list = recommended_recipes.to_dict('records')

            for recipe in recommended_recipes_list:
                recipe_id = recipe['id']
                image = photo.objects.filter(feed_id=recipe_id).first()
                recipe_post = post.objects.get(id=recipe_id)
                author_profile = profile.objects.get(user_id=recipe_post.author_id)
                
                if image:
                    recipe['image_url'] = image.image.url

                recipe['pk'] = recipe_id
                recipe['author'] = recipe_post.author.get_full_name
                recipe['whenpublished'] = recipe_post.whenpublished()
                recipe['read_time'] = recipe_post.read_time()
                recipe['hit_count'] = HitCount.objects.get_for_object(recipe_post).hits
                recipe['author_profile_img'] = author_profile.profile_img.url
        
        else:
            recommended_recipes_list = []

        # Getting recipes only from following users which current user follows
        following_user_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)

        following_user_posts = {}

        if following_user_ids:
            for user_id in following_user_ids:
                user_posts = post.objects.filter(author_id=user_id).order_by('-date_post')[:5]
                if user_posts.exists():
                    following_user_posts[User.objects.get(id=user_id)] = user_posts


        user_profile = self.request.user.profile
        type_preference = user_profile.preference_type
        category_preference = user_profile.preference_category
        cuisine_preference = user_profile.preference_cuisine

        if type_preference is not None and category_preference == 'Select' and cuisine_preference == 'Select':
            preference_choice_type = type_preference[:-8]
            recipes_preference = post.objects.filter(type=preference_choice_type).order_by('-hit_count_generic__hits','-date_post')


        elif category_preference is not None and type_preference == 'Select' and cuisine_preference == 'Select':
            preference_choice_category = category_preference[:-8]
            recipes_preference = post.objects.filter(category=preference_choice_category).order_by('-hit_count_generic__hits','-date_post')

        
        elif cuisine_preference is not None and type_preference == 'Select' and category_preference == 'Select' :
            recipes_preference = post.objects.filter(cuisine=cuisine_preference).order_by('-hit_count_generic__hits','-date_post')


        elif type_preference is not None and category_preference is not None and cuisine_preference == 'Select':
            preference_choice_type = type_preference[:-8]
            preference_choice_category = category_preference[:-8]

            recipes_preference = post.objects.filter(type=preference_choice_type,category=preference_choice_category).order_by('-hit_count_generic__hits','-date_post')
            # print(recipes_preference,'type & category')


        elif type_preference is not None and cuisine_preference is not None and category_preference == 'Select':
            preference_choice_type = type_preference[:-8]

            recipes_preference = post.objects.filter(type=preference_choice_type,cuisine=cuisine_preference).order_by('-hit_count_generic__hits','-date_post')
            # print(recipes_preference,'type & cuisine')


        elif category_preference is not None and cuisine_preference is not None and type_preference == 'Select':
            preference_choice_category = category_preference[:-8]

            recipes_preference = post.objects.filter(category=preference_choice_category,cuisine=cuisine_preference).order_by('-hit_count_generic__hits','-date_post')
            # print(recipes_preference,'category & cuisine')

        
        elif type_preference is not None and category_preference is not None and cuisine_preference is not None:
            preference_choice_type = type_preference[:-8]
            preference_choice_category = category_preference[:-8]
            
            recipes_preference = post.objects.filter(type=preference_choice_type,category=preference_choice_category,cuisine=cuisine_preference).order_by('-hit_count_generic__hits','-date_post')
            # print(recipes_preference,'type , category, cuisine')
        
        else:
            recipes_preference = []

        context = {"all":all,"all_recipes":all_recipes,"all_urecipe":all_urecipe,"brkfst": brkfst,"test":test,"historys_pk":historys_pk,
        "lnch": lnch,"evesnack":evesnack,"dnr":dnr,"l":l,"form":form,"spotlight_list":spotlight_list,'brkfst_count':brkfst_count,'lnch_count':lnch_count,
        'evesnack_count':evesnack_count,'dnr_count':dnr_count,"titles":titles,"date":date,"time":time,"hour":hour,"sec":sec,"diff":diff,"seconds":seconds,
        "minutes":minutes,"hours":hours,"days":days,"months":months,"years":years,"monthint":monthint,"monthstr":monthstr,"lastrecipe":lastrecipe,
        "allusrrecipe":allusrrecipe,"total_p":total_p,"breakfastpage":breakfastpage,"tbrkfst":tbrkfst,"lunchpage":lunchpage,"tlnch":tlnch,
        "eveningsnackupage":eveningsnackupage,"tevesnack":tevesnack,"dinnerpage":dinnerpage,"tdnr":tdnr,"trending_recipes":trending_recipes,"tot_posts_byuser":tot_posts_byuser,
        "allrecipes":allrecipes,"trnposts":trnposts,"joined":joined,"today":today,"tot_post_byuser":tot_post_byuser,"year_recap":year_recap,
        "next_day_brkfst":next_day_brkfst,"rice_recipe_list":rice_recipe_list,"panner_recipe_list":panner_recipe_list,'success_text': success_text,'current_time':current_time,
        'popular_recipe':popular_recipe,'pks':pks,'random_obj':random_obj,'recommended_recipes_list':recommended_recipes_list,'following_user_posts':following_user_posts,
        'type_preference':type_preference,'category_preference':category_preference,'cuisine_preference':cuisine_preference,'recipes_preference':recipes_preference}
        return context  
    

def compare_recipes(request,pk):
    titles = post.objects.all()
    recipe1 = get_object_or_404(post, pk=pk)
    photo1 = get_object_or_404(photo, feed=recipe1)

    if request.method == 'POST':
        recipe_id1 = request.POST.get('recipe1')
        recipe_id2 = request.POST.get('recipe2')
        
        if recipe_id1 and recipe_id2:
            return redirect('compare_view', recipe_id1=recipe_id1, recipe_id2=recipe_id2)

    # getting nutrition info from api
    query = recipe1.title

    nutrition_widget1 = get_recipe_nutrition_widget(recipe1.ingredients)

    nutrition_info_error,nutrition_info = None,None

    if query:

        try:
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
            api_request =  requests.get(api_url + query, headers = {'X-Api-Key': settings.NUTRITION_API_KEY})
            api_data = json.loads(api_request.content)
            
            if api_request.status_code == 200:
                nutrition_info = api_data
            else:
                nutrition_info_error = 'Error occurred'

        except ConnectionError:
            nutrition_info_error = 'Could not connect to Api'

        except Exception as e:
            api = "Error occured"
            nutrition_info_error = 'Error'

    # return redirect('recipe_compare_form')
    return render(request, 'testingapp/compare_recipes.html',{'titles':titles,'pk':pk,'recipe1':recipe1,
    'photo1':photo1,'nutrition_info':nutrition_info,'nutrition_info_error':nutrition_info_error,'nutrition_widget1':nutrition_widget1})

def compare_recipes_new(request):

    if request.method == 'POST':
        recipe_id1 = request.POST.get('recipe1')
        recipe_id2 = request.POST.get('recipe2')

        if recipe_id1 and recipe_id2:
            return redirect('compare_view', recipe_id1=recipe_id1, recipe_id2=recipe_id2)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def compare_view(request, recipe_id1, recipe_id2):
    recipe1 = get_object_or_404(post, pk=recipe_id1)
    recipe2 = get_object_or_404(post, pk=recipe_id2)
    
    photo1 = get_object_or_404(photo, feed=recipe1)
    photo2 = get_object_or_404(photo, feed=recipe2)

    titles = post.objects.all()

    user = request.user

    if user.is_authenticated and not request.session.get(f'viewed_post_{recipe_id2}', False):
        
        if user.profile.credits >= 1:
            user.profile.credits -= 1
            user.profile.credits_spent += 1

            CreditSpentHistory.objects.create(user=user, recipename=recipe2, amount=1)

            user.profile.save()
            request.session[f'viewed_post_{recipe_id2}'] = True
        else:
            error_msg = "Not enough credits to compare recipe"
            messages.error(request, error_msg , extra_tags='no-more-credits')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    nutrition_widget1 = get_recipe_nutrition_widget(recipe1.ingredients)
    nutrition_widget2 = get_recipe_nutrition_widget(recipe2.ingredients)

    # getting nutrition info from api
    query1 = recipe1.title
    query2 = recipe2.title

    nutrition_info_error1,nutrition_info1 = None,None
    nutrition_info_error2,nutrition_info2 = None,None

    if query1:

        try:
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
            api_request =  requests.get(api_url + query1, headers = {'X-Api-Key': settings.NUTRITION_API_KEY})
            api_data = json.loads(api_request.content)
            
            if api_request.status_code == 200:
                nutrition_info1 = api_data
            else:
                nutrition_info_error1 = 'Error occurred'

        except ConnectionError:
            nutrition_info_error1 = 'Could not connect to Api'

        except Exception as e:
            api = "Error occured"
            nutrition_info_error1 = 'Error'

    if query2:

        try:
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
            api_request =  requests.get(api_url + query2, headers = {'X-Api-Key': settings.NUTRITION_API_KEY})
            api_data = json.loads(api_request.content)
            
            if api_request.status_code == 200:
                nutrition_info2 = api_data
            else:
                nutrition_info_error2 = 'Error occurred'

        except ConnectionError:
            nutrition_info_error2 = 'Could not connect to Api'

        except Exception as e:
            api = "Error occured"
            nutrition_info_error2 = 'Error'
    
    context = {
        'recipe1': recipe1,
        'recipe2': recipe2,
        'photo1': photo1,
        'photo2': photo2,
        'titles':titles,
        'nutrition_info1':nutrition_info1,
        'nutrition_info_error1':nutrition_info_error1,
        'nutrition_info2':nutrition_info2,
        'nutrition_info_error2':nutrition_info_error2,
        'nutrition_widget1':nutrition_widget1,
        'nutrition_widget2':nutrition_widget2
    }
    return render(request, 'testingapp/compare_recipes.html', context)


from django.views.decorators.http import require_POST

@login_required
@require_POST
def remove_notification(request):
    notification_id = request.POST.get('notification_id')
    # print(notification_id)
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.delete()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification does not exist or you do not have permission to delete it'})


# Deleting all notifications for current user (request.user)
def clear_all_notifications(request):
    Notification.objects.filter(recipient=request.user).delete()
    return JsonResponse({'message': 'All notifications cleared successfully'})


def custom_cards(request,slug):

    try:
        all_recipes = post.objects.filter().all()
        veg_recipes = None
        nonveg_recipes = None
        new_recipes = None
        under_10_minutes = None

        end_date = datetime.datetime.now()
        start_date = end_date - timedelta(days=7)
        current_recipes = []

        if slug == 'veg_recipes':
            veg_recipes = post.objects.filter(category='Veg').order_by('-date_post')
            current_recipes = veg_recipes

        elif slug == 'nonveg_recipes':
            nonveg_recipes = post.objects.filter(category='Non-Veg').order_by('-date_post')
            current_recipes = nonveg_recipes

        elif slug == 'new_recipes':
            new_recipes = post.objects.filter(date_post__range=[start_date, end_date])
            current_recipes = new_recipes

        elif slug == 'under_10_minutes':
            under_10_minutes = post.objects.filter(timing__lte=10)
            current_recipes = under_10_minutes
                
        return render(request, 'testingapp/custom_cards.html', {'slug':slug,'veg_recipes': veg_recipes, 'all_recipes': all_recipes,
            'nonveg_recipes': nonveg_recipes,'new_recipes':new_recipes,'under_10_minutes':under_10_minutes})
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render(request, 'testingapp/custom_cards.html', {'error_message': 'An error occurred'})



def cuisines(request,slug):
    
    try:
        all_recipes = post.objects.filter().all()
        indian_cuisine = None
        american_cuisine = None
        italian_cuisine = None

        end_date = datetime.datetime.now()
        start_date = end_date - timedelta(days=7)

        if slug == 'Indian Cuisine':
            indian_cuisine = post.objects.filter(cuisine='Indian cuisine').order_by('-date_post')

        elif slug == 'American Cuisine':
            american_cuisine = post.objects.filter(cuisine='American cuisine').order_by('-date_post')

        elif slug == 'Italian Cuisine':
            italian_cuisine = post.objects.filter(cuisine='Italian cuisine').order_by('-date_post')

        return render(request, 'testingapp/cuisines.html', {'slug':slug,'indian_cuisine': indian_cuisine, 'all_recipes': all_recipes,
            'american_cuisine': american_cuisine,'italian_cuisine':italian_cuisine})
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render(request, 'testingapp/cuisines.html', {'error_message': 'An error occurred'})


@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account
        user = request.user
        user.delete()
        return redirect('login') 
    
    return render(request, 'testingapp/delete_account.html')




# Trending recipes
class trendingview(HitCountMixin, ListView):
    model = post
    template_name = 'testingapp/trending.html'
    # ordering = ['-date_post']
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(trendingview, self).get_context_data(**kwargs)
        user = self.request.user

        hour = datetime.datetime.now().hour

        counts = post.objects.order_by('-hit_count_generic__hits')     
         
        trnposts = post.objects.order_by('-hit_count_generic__hits') [0:4]

        all_recipes = post.objects.filter().all()

        allrecipes = post.objects.all().order_by('-date_post').all().count()

        tot_posts_byuser = 0

        historys_pk = None

        if self.request.user.is_authenticated:

            blog_history = BlogHistory.objects.filter(user=user)

            blog_posts = [(entry.pk ,entry.blog_post) for entry in blog_history]

            post_count = []

            for pk,history in blog_posts:
                post_count.append(history.pk)

            historys_pk = [*set(post_count)]
        
        if self.request.user.is_authenticated:
            tot_posts_byuser = post.objects.filter(author=user).all().count()   
        
        context = {"all_recipes":all_recipes,"hour":hour,"counts":counts,"tot_posts_byuser":tot_posts_byuser,"allrecipes":allrecipes,
        "trnposts":trnposts,"historys_pk":historys_pk}
        return context


# Update Recipe
def Updaterecipeview(request,title,pk, *args, **kwargs):
    recipes = post.objects.get(title=title,pk=pk)
    ImageFormset = modelformset_factory(photo, fields=('image',),extra=1,max_num=2)

    if recipes.author != request.user:
        raise Http404
        
    if request.method == 'POST':
        form = post_form(request.POST or None, instance=recipes)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        
        if form.is_valid() and formset.is_valid():
            form.save()

            data = photo.objects.filter(feed=recipes)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        pho = photo(feed=recipes, image=f.cleaned_data.get('image'))
                        pho.save()
                    elif f.cleaned_data['image'] is False:
                        pho = photo.objects.get(pk=request.POST.get('form-' + str(index) + '-pk'))
                        pho.delete()
                    else:
                        pho = photo(feed=recipes, image=f.cleaned_data.get('image'))
                        d = photo.objects.get(pk=data[index].pk)
                        d.image = pho.image
                        d.save()

            request.session['update_recipe_message'] = title
            
            return redirect('dashboard')
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
    else:
        form = post_form(instance=recipes)
        formset = ImageFormset(queryset=photo.objects.filter(feed=recipes))

    # Get existing images
    existing_images = photo.objects.filter(feed=recipes)

    # Generate a list of forms for each existing image with a delete button
    image_forms = []
    for existing_image in existing_images:
        image_form = ImageFormset(initial=[{'image': existing_image.image}], prefix=f'form-{existing_image.pk}')
        image_forms.append({
            'form': image_form,
            'image': existing_image,
        })


    return render(request,'testingapp/updaterecipe.html',{'form':form,'formset':formset,'recipes':recipes,"image_forms":image_forms})




def delete_image(request, image_pk):
    image = get_object_or_404(photo, pk=image_pk)
    
    image.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # return redirect('updaterecipe')  




# Delete recipe
class Deletepost(DeleteView):
    model = post
    template_name = 'testingapp/delete.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response_data = {'success': False}

        try:
            self.object = self.get_object()

            # Check if the post belongs to the logged-in user
            if self.object.author == self.request.user:
                
                if self.request.user.profile.earned_credits >= 2 and self.request.user.profile.credits <= 2:
                    self.request.user.profile.earned_credits -= 2

                elif self.request.user.profile.earned_credits <= 2 and self.request.user.profile.credits >= 2:
                    self.request.user.profile.credits -= 2

                # elif self.request.user.profile.earned_credits <= 2 and self.request.user.profile.credits <= 2:
                #     return redirect('dashboard')

                self.request.user.profile.save()

                # Record the credit redemption in CreditHistory
                CreditHistory.objects.create(user=self.request.user, credit_action='deleted', amount=-2)

                recipe_title = self.object.title

                # Call the parent form_valid method to delete the post
                response = super().form_valid(form)

                # Check if the post was successfully deleted
                if response.status_code == 302:
                    response_data['success'] = True
                    response_data['title'] = recipe_title
                else:
                    response_data['error'] = 'An error occurred during deletion'

            else:
                # Handle the case where the post doesn't belong to the logged-in user
                response_data['error'] = "You can't delete the post"

        except Exception as e:
            # Log the exception or handle it as needed
            # print(str(e))
            response_data['error'] = 'An error occurred during deletion'

        return JsonResponse(response_data)

# class Deletepost(DeleteView):
#     model = post
#     template_name = 'testingapp/delete.html'
#     success_url = reverse_lazy('dashboard')

#     def form_valid(self, form):
#         self.object = self.get_object()

#         # Check if the post belongs to the logged-in user
#         if self.object.author == self.request.user:
            
#             if self.request.user.profile.earned_credits >= 2 and self.request.user.profile.credits <= 2:
#                 self.request.user.profile.earned_credits -= 2

#             elif self.request.user.profile.earned_credits <= 2 and self.request.user.profile.credits >= 2:
#                 self.request.user.profile.credits -= 2

#             elif self.request.user.profile.earned_credits <= 2 and self.request.user.profile.credits <= 2:
#                 return redirect('dashboard')

#             self.request.user.profile.save()

#             # Record the credit redemption in CreditHistory
#             CreditHistory.objects.create(user=self.request.user,credit_action='deleted', amount=-2)

#         # Calling the parent form_valid method to delete the post
#         return super().form_valid(form)


from .utils import summarize_text
from django.utils.html import strip_tags
from django.utils.safestring import SafeString

def summarize_content(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        
        # If OpenAI API is available
        if settings.OPENAI_API_KEY:
            try:
                summarized_content, status_code  = summarize_text(content)
        
                # uncomment below line if not using typing simulation in the template
                # safe_summarized_content = SafeString(summarized_content) 

                safe_summarized_content = strip_tags(summarized_content)

                return JsonResponse({'summarizedContent': safe_summarized_content,'status_code':status_code})
            
            except Exception as e:
                return JsonResponse({'error': str(e)})
            
        # Else use GEMINI API
        else:
            try:
                post_content = striptags(content)
                genai.configure(api_key=settings.GEMINI_API_KEY)

                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    f"Summarize the recipe instructions {post_content}"
                )
                return JsonResponse({'summarizedContent': response.text})

            except Exception as e:
                return JsonResponse({'error': str(e)})


    return JsonResponse({'error': 'Invalid request method'}, status=400)


def summarize_text(text):
    api_key = settings.OPENAI_API_KEY
    api_endpoint = 'https://api.openai.com/v1/engines/gpt-3.5-turbo-instruct/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        'prompt': text,
        'max_tokens': 100,
    }

    response = requests.post(api_endpoint, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()['choices'][0]['text'], response.status_code
    else:
        a = response.status_code
        return None, response.status_code


def extract_dominant_colors(image_path, num_colors=7):
    # Open the image
    image = Image.open(image_path)

    # Create a full-size thumbnail for faster processing
    thumbnail_size = image.size
    image.thumbnail(thumbnail_size)

    # Convert the image to the paletted mode with an adaptive palette
    paletted = image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)

    # Get the color palette of the paletted image
    palette = paletted.getpalette()


    # Convert palette RGB values to hexadecimal format
    dominant_colors_hex = [
        "#{:02x}{:02x}{:02x}".format(palette[i], palette[i + 1], palette[i + 2])
        for i in range(0, len(palette), 3)
    ]

    return dominant_colors_hex

# LoginRequiredMixin (removed to allow unauthenticated users to view any 2 recipes after that it requires login)
class postDetailView(HitCountDetailView):
    model = post
    template_name = 'testingapp/postdetail.html'
    context_object_name = 'post'
    # slug_field = 'slug'
    count_hit = True

    def extract_colors(self, post_photos):
        user = self.request.user
        if user.is_authenticated:
            profile = user.userprofile

            if profile.use_colors_from_image:
                extracted_colors = []
                
                for i, photo_instance in enumerate(post_photos, 1):
                    image_path = photo_instance.image.path
                    colors = extract_dominant_colors(image_path)
                    # colors = extract_dominant_colors(image_path, thumbnail_size=(100, 100))

                    # Print all extracted colors for the current photo
                    # for j, color_hex in enumerate(colors, 1):
                        # print(f"Color {i}-{j} (Hex): {color_hex}")

                    extracted_colors.extend(colors)  # Add colors to the list
                # print(extracted_colors)
                return extracted_colors if extracted_colors else []
            
            else:
                return []
        
        else:
            return []
    
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # Check if the user is authenticated and hasn't viewed the page yet
        if user.is_authenticated and not request.session.get(f'viewed_post_{self.get_object().pk}', False):
            # Check if the user has enough credits
            if user.profile.credits >= 1:
                
                # Deduct 1 credit from the user's account
                user.profile.credits -= 1

                # Update the credits_spent field in the user's profile
                user.profile.credits_spent += 1

                # Create a new entry in CreditSpentHistory to record the credit spent
                CreditSpentHistory.objects.create(user=user, recipename=self.get_object(), amount=1)

                user.profile.save()
                # messages.success(request, "You have successfully viewed the page. 1 credit deducted.")

                # Set a session variable to track that the user has viewed the page
                request.session[f'viewed_post_{self.get_object().pk}'] = True
            else:
                error_msg = "Not enough credits!"
                messages.error(request, error_msg , extra_tags='no-more-credits')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                # return redirect('home')
            
        # Allowing unauthenticated user to view upto 5 recipes (any)
        elif not request.user.is_authenticated:
            request.session.setdefault('viewed_recipes', [])
            viewed_recipes = request.session['viewed_recipes']
            if len(viewed_recipes) >= 5:
                return redirect('topostlogin',self.get_object().pk)

            viewed_recipes.append(self.get_object().pk)
            request.session['viewed_recipes'] = viewed_recipes[:5]  # Limit to 5 recipes
            
        post_instance = self.get_object()  # Get the post instance
        post_photos = post_instance.photo_set.all()  # Retrieve related photos
        colors_response = self.extract_colors(post_photos)

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self,pk=post.id, **kwargs):

        context = super().get_context_data(**kwargs)

        postrecipe = self.get_object()
        post_photos = postrecipe.photo_set.all()

        # getting nutrition info from api
        query = postrecipe.title

        if query:

            try:
                api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
                api_request =  requests.get(api_url + query, headers = {'X-Api-Key': settings.NUTRITION_API_KEY})
                api_data = json.loads(api_request.content)
                
                if api_request.status_code == 200:
                    context['nutrition_info'] = api_data
                else:
                    context['nutrition_info_error'] = 'Error occurred'

            except ConnectionError:
                context['nutrition_info_error'] = 'Could not connect to Api'

            except Exception as e:
                api = "Error occured"
                context['nutrition_info_error'] = api

        recipe_id=self.kwargs['pk']
        # Check if the recipe exists
        if not post.objects.filter(id=recipe_id).exists():
            raise ValueError(f"Recipe with {recipe_id} not found.")
        
        recommended_recipes = get_recommendations(recipe_id)
        context['recommended_recipes'] = recommended_recipes

        context['comments'] = comments.objects.filter(post_super=self.get_object()).order_by('date_comment')
        context['comments_count'] = comments.objects.filter(post_super=self.get_object()).count()

        form = comment_form()
        context['form'] = form

        post_content = striptags(self.get_object().content)
        # recipe_title = self.get_object().title

        # gtts library for audio
        audio_file_path = f'{self.get_object().title}.mp3'

        # if the audio file is not downloaded
        # if not default_storage.exists(audio_file_path):
        #     text_to_speak = post_content
        #     tts = gTTS(text=text_to_speak, lang='en',tld='co.in')
        #     file_path = os.path.join(settings.MEDIA_ROOT, audio_file_path)
        #     tts.save(file_path)

        context['audio_file_new'] = default_storage.url(audio_file_path)
        


        # openai.api_key = settings.OPENAI_API_KEY

        # Get the audio data from the OpenAI API
        # response = openai.audio.speech.create(
        #     model="tts-1",
        #     voice="alloy",
        #     input=post_content,
        # )

        # # Save the audio data to a file
        # file_name = f'recipe_title_{self.get_object().id}.mp3'
        # file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        # with open(file_path, "wb") as f:
        #     f.write(response.content)

        # # Save the file to Django's default storage
        # with open(file_path, 'rb') as f:
        #     default_storage.save(file_name, f)

        # # Set context['audio_file_name'] to the URL of the audio file
        # context['audio_file_name'] = default_storage.url(file_name)

        




        # original_content = strip_tags(self.get_object().content)
        # summarized_content = summarize_text(original_content)

        # context['original_content'] = original_content
        # context['summarized_content'] = summarized_content

        post_author = context['post']
        author_name = post_author.author.username

        author = User.objects.get(username=author_name)
        context['author_recipes'] = post.objects.filter(author=author)
        
        context['hour'] = datetime.datetime.now().hour
        context['breakfast'] = post.objects.filter(type="Breakfast").all()
        context['lunch'] = post.objects.filter(type="Lunch").all()
        context['evesnack'] = post.objects.filter(type="Evening Snack").all()
        context['dinner'] = post.objects.filter(type="Dinner").all()
        context['all_recipes'] = post.objects.filter().all()
        context['trending_recipes'] = post.objects.order_by('-hit_count_generic__hits') [0:10]

        # context['recipe_img'] = recipe_img

        hit_count = self.request.META.get('REMOTE_ADDR')
        context['hit_count'] = hit_count

        trending_list = []

        recipe_name = []

        index_val = []

        trending_recipes = post.objects.order_by('-hit_count_generic__hits') [0:10]

        get_recipe = post.objects.filter(title=self.object.title)  
        for i in trending_recipes:
            trending_list.append(i.title)

        for i in get_recipe:
            recipe_name.append(i.title)

        for i in recipe_name:
            for j in trending_list:

                if i == j:
                    a = trending_list.index(j) + 1
                    index_val.append(a)

        recipes_by_author = self.object

        total_recipes_by_author = post.objects.filter(author=recipes_by_author.author).count()

        context['total_recipes_by_author'] = total_recipes_by_author

        pk=self.kwargs['pk']
        user = self.request.user

        # Create BlogHistory instance if the user is authenticated
        if user.is_authenticated:
            blog_post = get_object_or_404(post, id=pk)

            # Check if the blog_post already exists in BlogHistory for the user
            if not BlogHistory.objects.filter(user=user, blog_post=blog_post).exists():
                blog_history = BlogHistory(user=user, blog_post=blog_post)

            else:
                # If blog_history exists then update the timestamp 
                blog_history = BlogHistory.objects.filter(user=user, blog_post=blog_post).first()
                blog_history.timestamp = timezone.now()  
            blog_history.save()
        

        if user.is_authenticated:
            context['tot_posts_byuser'] = post.objects.filter(author=user).all().count()
            
        
        context['allrecipes'] = post.objects.all().order_by('-date_post').all().count()
        context['trnposts'] = post.objects.order_by('-hit_count_generic__hits') [0:4]

        context['check'] = index_val
        context['fetched_recipe'] = recipe_name
        context['top_10_trend_recipes'] = trending_list

        recipe_author = post_author.author.id
        followers_count = Follow.objects.filter(following=recipe_author).count()
        context['followers'] = followers_count

        recipe_author_username = post_author.author
        results = User.objects.filter(
            reduce(or_, [
                Q(username__icontains=recipe_author_username),
            ])
        )
        
        if user.is_authenticated:
            is_following = []
            user_results = []
            for user in results:
                user_exists = Follow.objects.filter(follower=self.request.user, following=user).exists()
                is_following.append(user_exists)
                user_results.append(user)

            context['is__following'] = is_following
            context['user__results'] = user_results


        user_profiles = profile.objects.all()

        context['user_profiles'] = user_profiles


        recipe = self.get_object()

        nutrition_widget = get_recipe_nutrition_widget(recipe.ingredients)

        context['nutrition_widget'] = nutrition_widget


        # for shopping list
        recipe_object = self.get_object()
    
        recipe_ingredients = recipe_object.ingredients
        
        soup = BeautifulSoup(recipe_ingredients, 'html.parser')
        text = soup.get_text(separator='\n').strip()

        cleaned_ingredients = []
        pattern = re.compile(r'^\d*(\d+\.?\d*)\s*([a-zA-Z]+)?\s*(.*)$')
        
        for ingredient in text.split('\n'):
            ingredient = ingredient.strip()
            match = pattern.match(ingredient)
            if match:
                item = match.group(3).strip()
                cleaned_ingredients.append({
                    'item': item
                })

        context['list'] = cleaned_ingredients

        # QR code generation
        post_url = get_object_or_404(post, pk=self.kwargs['pk'])
        recipe_url = self.request.build_absolute_uri(post_url.get_recipe_url())

        qr = qrcode.QRCode(
            version=1,
            box_size=7,
            border=0,
        )
        qr.add_data(recipe_url)
        qr.make(fit=True)
        
        if user.is_authenticated:
            fill_color = self.request.user.userprofile.neutral_primary
            back_color = self.request.user.userprofile.secondary_color
        else:
            fill_color = '#000000'
            back_color = '#FFFFFF'

        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Saving the image in memory
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        img_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
      
        context['img_data'] = img_data
        return context

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        return reverse('compare_recipes', kwargs={'pk': pk})


    def strip_tags(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()


    def translate_content(self, post_content):
        openai.api_key = settings.OPENAI_API_KEY

        stripped_content = self.strip_tags(post_content)

        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Translate the following English text to Hindi: '{stripped_content}'",
                max_tokens=300
            )
            translated_text = response.choices[0].text.strip()
            return JsonResponse({'translated_text': translated_text})

        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
        # response = openai.Completion.create(
        #     engine="gpt-3.5-turbo-instruct",
        #     prompt=f"Translate the following English text to Hindi: '{stripped_content}'",
        #     max_tokens=300
        # )

        # translated_text = response.choices[0].text.strip()
        # print(stripped_content)
        # return JsonResponse({'translated_text': translated_text})


    def post(self,request,*args,**kwargs):
        # print(request.POST)
        if 'comt' in request.POST:
            com = comments.objects.create(post_super=self.get_object(),comment_user=request.user,comment=request.POST['comt'])
            # Notify the author of the post
            comment_text = request.POST['comt']
            if self.request.user != self.get_object().author:
                notify.send(
                    sender=self.request.user,
                    recipient=self.get_object().author,
                    verb='commented',
                    action_object=self.get_object(),
                    description=comment_text, 
                )
            cmt = serializers.serialize('json', [ com, ], fields=('comment', 'date_comment'))
            return JsonResponse({'cmt':cmt},safe=False)
        
            # Handling translation
        if 'translate_content' in request.POST and 'post_content' in request.POST:
            post_content = request.POST['post_content']
            return self.translate_content(post_content)



def shopping_list_pdf(request,title,pk, *args, **kwargs):

    recipe_object = get_object_or_404(post,title=title)
    
    recipe_ingredients = recipe_object.ingredients
    
    soup = BeautifulSoup(recipe_ingredients, 'html.parser')
    text = soup.get_text(separator='\n').strip()

    cleaned_ingredients = []
    pattern = re.compile(r'^\d*(\d+\.?\d*)\s*([a-zA-Z]+)?\s*(.*)$')
    
    for ingredient in text.split('\n'):
        ingredient = ingredient.strip()
        match = pattern.match(ingredient)
        if match:
            item = match.group(3).strip()
            cleaned_ingredients.append({
                'item': item
            })

    recipe_title = recipe_object.title

    html_content = render_to_string('testingapp/shopping_list.html', {'cleaned_ingredients': cleaned_ingredients,
    'recipe_object':recipe_object})
    file_name = f"{recipe_title}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{file_name}"'

    pisa_status = pisa.CreatePDF(html_content,dest=response)

    return response

# def strip_tags(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     return soup.get_text()


@login_required(login_url='login')
def blog_history(request):

 
    blog_history = BlogHistory.objects.filter(user=request.user).order_by('-timestamp')
    all = BlogHistory.objects.filter(user=request.user)

    todays_date = datetime.date.today()

    blog_posts = [(entry.pk ,entry.blog_post, entry.timestamp) for entry in blog_history]
    
    todays_date = datetime.date.today()
    yesterday = todays_date - datetime.timedelta(days=1)
    previous_7_days = todays_date - datetime.timedelta(days=7)

    today_posts = [(entry.pk, entry.blog_post, entry.timestamp) for entry in blog_history if entry.timestamp.date() == todays_date]
    yesterday_posts = [(entry.pk, entry.blog_post, entry.timestamp) for entry in blog_history if entry.timestamp.date() == yesterday]
    previous_7_days_posts = [(entry.pk, entry.blog_post, entry.timestamp) for entry in blog_history if previous_7_days <= entry.timestamp.date() < todays_date]


    return render(request, 'testingapp/blog_history.html', {'blog_posts': blog_posts,"blog_history":blog_history,"all":all,"todays_date":todays_date,
    "yesterday":yesterday,"previous_7_days":previous_7_days,"today_posts":today_posts,'yesterday_posts': yesterday_posts,
        'previous_7_days_posts': previous_7_days_posts,})



def delete_entry(request,pk):
    entry = BlogHistory.objects.get(pk=pk)
    entry.delete()
    print(entry)

    return redirect('blog_history')


def bulk_delete_blogs(request):
    entry_ids = request.POST.getlist('blog_ids')
    print(entry_ids)
    BlogHistory.objects.filter(id__in=entry_ids,user=request.user).delete()
    return redirect('blog_history')
    

def delete_all_blog_history(request):
    if request.method == 'POST':
        a = BlogHistory.objects.all().delete()
        print(a)
        return redirect('blog_history') 
    return redirect('blog_history') 


@login_required(login_url='login')
def dashboard(request):

    user = request.user
    all_recipes = post.objects.filter().all()        

    all = post.objects.all().filter(author=user).order_by('-date_post')
    brkfst = post.objects.filter(author=user,type ='Breakfast').order_by('-date_post')
    lnch = post.objects.filter(author=user,type ='Lunch').order_by('-date_post')
    snack = post.objects.filter(author=user,type ='Evening Snack').order_by('-date_post')
    dnr = post.objects.filter(author=user,type ='Dinner').order_by('-date_post')
    veg_recipe = post.objects.filter(author=user,category='Veg').order_by('-date_post')
    non_veg = post.objects.filter(author=user,category='Non-Veg').order_by('-date_post')

    tot_posts_byuser = post.objects.filter(author=user).all().count()
    breakfast = post.objects.filter(author=request.user,type ='Breakfast').count()
    lunch = post.objects.filter(author=request.user,type ='Lunch').count()
    evesnack = post.objects.filter(author=request.user,type ='Evening Snack').count()
    dinner = post.objects.filter(author=request.user,type ='Dinner').count()
    veg = post.objects.filter(author=request.user,category ='Veg').count()
    nonveg = post.objects.filter(author=request.user,category ='Non-Veg').count()

    last_recipe = post.objects.filter(author=request.user).last()

    last_viewed_recipe = BlogHistory.objects.filter(user=request.user).order_by('-timestamp').first()

    last_comment = comments.objects.filter(comment_user=request.user).order_by('-date_comment').first()
    
    if last_comment:
        commented_post = last_comment.post_super
    else:
        commented_post = ''

    top_performing_recipes = post.top_performing_recipes(request.user)

    last_liked_recipe = post.objects.filter(likes=user.profile).order_by('-date_modified').first()

    # success message for updating the recipe 
    update_recipe_text = request.session.pop('update_recipe_message', None)

    current_year = date.today().year

    user_profile = request.user.profile

    recipes_uploaded = post.objects.filter(author=request.user, date_post__year=current_year).count()

    # goals set for current year
    goal_for_year = YearlyGoal.objects.filter(profile=user_profile, year=current_year).first()
    goal_for_year_value = goal_for_year.goal if goal_for_year else 0

    # recipes uploaded in current year not counting the previous years recipes
    recipes_uploaded = post.objects.filter(author=request.user, date_post__year=current_year).count()
    
    # Calculating progress percentage
    progress_percentage = (
        (recipes_uploaded / goal_for_year_value) * 100
        if goal_for_year_value > 0 else 0
    )

    return render(request,'testingapp/dashboard.html',{"all_recipes":all_recipes,"all":all, "brkfst": brkfst,"lnch": lnch,
    "snack":snack,"dnr":dnr,"veg_recipe":veg_recipe,"non_veg":non_veg,"tot_posts_byuser":tot_posts_byuser,"breakfast":breakfast,
    "lunch":lunch,"evesnack":evesnack,"dinner":dinner,"veg":veg,"nonveg":nonveg,'last_recipe':last_recipe,
    'last_viewed_recipe':last_viewed_recipe,'last_comment':last_comment,'commented_post':commented_post,
    'last_liked_recipe':last_liked_recipe,'top_performing_recipes':top_performing_recipes,'update_recipe_text':update_recipe_text,
    'recipes_uploaded':recipes_uploaded,'goal_for_year':goal_for_year,"progress_percentage": int(progress_percentage)})




# user_profile_dashboard
def userchannel(request,first,pk,last=None):
    
    user = request.user

    user_profiles = profile.objects.all()

    if last is not None:

        try:
            # profile_details = User.objects.get(first_name=first, last_name=last)

            # searching the user channel with their full name from url with case insensitive
            # profile_details = User.objects.get(Q(first_name__iexact=first) & Q(last_name__iexact=last))
            profile_details = User.objects.get(pk=pk)

            user_profiles = profile.objects.all()
            total_user_recipes = post.objects.filter(author=profile_details).order_by('-date_post').all()
            all_recipes = post.objects.filter().all()
            brkfst_recipes = post.objects.filter(author=profile_details,type='Breakfast').all()
            lnch_recipes = post.objects.filter(author=profile_details,type='Lunch').all()
            evesnack_recipes = post.objects.filter(author=profile_details,type='Evening Snack').all()
            dnr_recipes = post.objects.filter(author=profile_details,type='Dinner').all()

        except Exception as e:
            error_message = str(e)
            return render(request,'testingapp/userchannelpage.html', {'error_message': error_message})

    else:
        try:
            return redirect(reverse('searchresults') + f'?query={first}')

        except Exception as e:
            error_message = str(e)
            return render(request,'testingapp/userchannelpage.html')

    all_recipes = post.objects.filter().all()

    query = request.GET.get('follow_user')
    # results = User.objects.filter(
    #     reduce(or_, [
    #         Q(first_name__icontains=first),
    #         Q(last_name__icontains=last),
    #     ])
    # )
    
    results = User.objects.filter(pk=pk)

    # profile_details = User.objects.get(Q(first_name__iexact=first) & Q(last_name__iexact=last))
    profile_details = User.objects.get(pk=pk)

    user_profiles = profile.objects.all()
    total_user_recipes = post.objects.filter(author=profile_details).order_by('-date_post').all()
    all_recipes = post.objects.filter().all()
    brkfst_recipes = post.objects.filter(author=profile_details,type='Breakfast').all()
    lnch_recipes = post.objects.filter(author=profile_details,type='Lunch').all()
    evesnack_recipes = post.objects.filter(author=profile_details,type='Evening Snack').all()
    dnr_recipes = post.objects.filter(author=profile_details,type='Dinner').all()

    user_total_views = post.objects.filter(author=profile_details).annotate(total_hits=Sum('hit_count_generic__hits')).aggregate(total=Sum('total_hits'))['total']

    user_followers_count = Follow.objects.filter(following=profile_details).count()

    # user profile social media links
    user_social_links = profile.objects.get(user_id=profile_details)

    bio = profile_details.profile
    user_bio = bio.bio
    date_joined = profile_details.date_joined.date()

    absolute_url = request.build_absolute_uri()

    if request.user.is_authenticated:
        is_following = []
        for user in results:
            user_exists = Follow.objects.filter(follower=request.user, following=user).exists()
            is_following.append(user_exists)

        return render(request,'testingapp/userchannelpage.html',{"profile_details":profile_details,
        "user_profiles":user_profiles,"all_recipes":all_recipes,"total_user_recipes":total_user_recipes,
        "brkfst_recipes":brkfst_recipes,
        "lnch_recipes":lnch_recipes,
        "evesnack_recipes":evesnack_recipes,
        "dnr_recipes":dnr_recipes,
        'results': results, 'query': query,'is_following':is_following,'user_total_views':user_total_views,
        'user_followers_count':user_followers_count,'user_social_links':user_social_links,'user_bio':user_bio,'date_joined':date_joined,
        'absolute_url':absolute_url})

    else:
        return render(request,'testingapp/userchannelpage.html',{"profile_details":profile_details,
        "user_profiles":user_profiles,"all_recipes":all_recipes,"total_user_recipes":total_user_recipes,
        "brkfst_recipes":brkfst_recipes,
        "lnch_recipes":lnch_recipes,
        "evesnack_recipes":evesnack_recipes,
        "dnr_recipes":dnr_recipes,'user_total_views':user_total_views,
        'user_followers_count':user_followers_count,'user_social_links':user_social_links,'user_bio':user_bio,'date_joined':date_joined,
        'absolute_url':absolute_url})

    # return render(request,'testingapp/userchannelpage.html',{"profile_details":profile_details,
    # "user_profiles":user_profiles,"all_recipes":all_recipes,"total_user_recipes":total_user_recipes,
    # "brkfst_recipes":brkfst_recipes,
    # "lnch_recipes":lnch_recipes,
    # "evesnack_recipes":evesnack_recipes,
    # "dnr_recipes":dnr_recipes})
        

def like_view(request):
    user = request.user
    if request.method == 'POST':
        try:
            post_id = request.POST.get('post_id')
            post_obj = post.objects.get(id=post_id)
            profiles = profile.objects.get(user=user)

            # Check if the user has already disliked the recipe
            if profiles in post_obj.dislikes.all():
                # If the user has disliked, remove the dislike first
                post_obj.dislikes.remove(profiles)

            if profiles in post_obj.likes.all():
                post_obj.likes.remove(profiles)
                action = 'remove'
                if user != post_obj.author:
                    post_obj.author.profile.earned_credits -= 1
                    post_obj.author.profile.save()
                profiles.earned_credits -= 1
                profiles.save()

            else:
                post_obj.likes.add(profiles)
                action = 'added'
                if user != post_obj.author:
                    post_obj.author.profile.earned_credits += 1
                    post_obj.author.profile.save()
                profiles.earned_credits += 1
                profiles.save()

                # Notify the author of the post
                if user != post_obj.author:
                    notify.send(
                        sender=user,
                        recipient=post_obj.author,
                        verb='liked',
                        action_object=post_obj,
                    )

            removefromdislike = []
            if profiles in post_obj.dislikes.all():
                b = 'exists'
                removefromdislike.append(b)

            # Ensure that the author does not receive 1 credit if the author liked their own post
            if user == post_obj.author:
                post_obj.author.profile.earned_credits = max(Decimal('0'), post_obj.author.profile.earned_credits)
                post_obj.author.profile.save()

            post_obj.save()
            
            # Call the method to get the actual value of total_likes
            total_likes = post_obj.total_likes()
            total_dislikes = post_obj.total_dislikes()

            # Return JSON response with updated like count
            return JsonResponse({'total_likes': total_likes,'total_dislikes':total_dislikes,'removefromdislike':removefromdislike,'action':action})
            # return redirect('viewpost',post_id)

        except Exception as e:
            return JsonResponse({'error': str(e)})
        
    else:
        
        return JsonResponse({'error': 'Invalid request!'})
    # return redirect('home')

def dislike_view(request):
    user = request.user
    if request.method == 'POST':
        try:
            post_id = request.POST.get('post_id')
            post_obj = post.objects.get(id=post_id)
            profiles = profile.objects.get(user=user)

            # print('dislike',post_obj)
            
            # Check if the user has already liked the recipe
            if profiles in post_obj.likes.all():
                # If the user has liked, remove the like first
                post_obj.likes.remove(profiles)

            removefromlike = []
            if profiles in post_obj.dislikes.all():
                b = 'exists'
                removefromlike.append(b)

            if profiles in post_obj.dislikes.all():
                r = post_obj.dislikes.remove(profiles)
                action = 'remove'

            else:
                a = post_obj.dislikes.add(profiles)
                action = 'added'

                # Notify the author of the post
                if user != post_obj.author:
                    notify.send(
                        sender=user,
                        recipient=post_obj.author,
                        verb='disliked',
                        action_object=post_obj,
                    )
                

            post_obj.save()

            # Call the method to get the actual value of total_likes
            total_dislikes = post_obj.total_dislikes()
            total_likes = post_obj.total_likes()

            # Return JSON response with updated like count
            return JsonResponse({'total_dislikes': total_dislikes,'total_likes':total_likes,'removefromlike':removefromlike,'action':action})
        
        except Exception as e:
            return JsonResponse({'error': str(e)})

    else:    
        return JsonResponse({'error': 'Invalid request!'})
    # return redirect('viewpost',post_id)


def extract_hex_codes(text):
    return re.findall(r'#[a-fA-F0-9]{6}', text)


@login_required(login_url='login')
def post_post_view(request):
    post_count = post.objects.filter(author=request.user).count() 
    request.session['count'] = post_count

    user = request.user

    tot_posts_byuser = post.objects.filter(author=user).all().count()
    allrecipes = post.objects.all().order_by('-date_post').all().count()
    trnposts = post.objects.order_by('-hit_count_generic__hits') [0:4]
    

    if request.method == 'POST':
        
        if request.POST.get("img_type") == 'mainimage':
            try:
                # This is the submission of the imageGenerationForm
                image_generation_form = ImageGenerationForm(request.POST)

                if image_generation_form.is_valid():
                    # Get the title from the image generation form
                    title = image_generation_form.cleaned_data['title']
                    # print(title)
                    # Generate an image based on the user's input
                    openai.api_key = settings.OPENAI_API_KEY  
                    
                    prompt = title  # Use the title as the prompt
                    response = openai.Image.create(
                        prompt=prompt,
                        n=1,
                        size="256x256"
                    )

                    try:
                        # Download the generated image
                        image_url = response.data[0].url
                        # print(image_url)
                    except (AttributeError, KeyError):
                        image_url = None

                    if image_url:
                        return JsonResponse({"image_url": image_url,"title":title})
                    
            except Exception as e:
                # print(f"An error occurred: {str(e)}")
                error = str(e)
                # print(error)
                return JsonResponse({"error": error})
        
        elif 'title' in request.POST:
            # This is the submission of myForm with recipe details
            form = post_form(request.POST, request.FILES)
            files = request.FILES.getlist('image')

            if form.is_valid():
                # Handle the recipe details form submission
                # Save the post instance
                post_instance = form.save(commit=False)
                post_instance.author = request.user



                post_instance.save()
                form.save_m2m()

                # Retrieve the image URL from the hidden input
                image_url = request.POST.get('image_url')

                for f in files:
                    file_instance = photo(image=f, feed=post_instance)
                    file_instance.save()

                    image_name = f'{post_instance.title}.jpg'  
                    image_content = ContentFile(f.read())
                    default_storage.save(f'images/{image_name}', image_content)

                # Add 4 credits to the user's account
                if request.user.is_authenticated:
                    request.user.profile.earned_credits += 4
                    request.user.profile.save()

                    # Record the credit in CreditHistory
                    CreditHistory.objects.create(user=request.user,credit_action='new_recipe', amount=4)

                # Create a new 'photo' instance and save the image (for saving images generated using openai api)
                if image_url:
                    photo_instance = photo(feed=post_instance)
                    img_name = request.POST.get('api_image_title')
                    original_image_name = f'{img_name}.jpg'  
                    api_image_name = original_image_name.replace(' ', '_') 
                    photo_instance.image.save(api_image_name, ContentFile(requests.get(image_url).content))

                    # api_image_content = ContentFile(requests.get(image_url).content)
                    # default_storage.save(f'images/{api_image_name}', api_image_content)


                profile = request.user.profile
                title = post_instance.title
                name = user.first_name
                date_posted = post_instance.date_post.date()
                post_instance.date_posted = datetime.datetime.now()
                post_timing = post_instance.date_posted.strftime('%I:%M %p')
                uploaded_image = request.FILES.get('image')

                if profile.send_email:  # Check if the user has opted in
                    subject = f'{title}'
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [user.email]

                    context = {'uploaded_image': uploaded_image, 'name': name, 'title': title, 'date_posted': date_posted, 'post_timing':post_timing}

                    if settings.ENVIRONMENT == 'True':
                        # If the image was generated using OpenAI
                        if image_url:
                            
                            get_img_name = request.POST.get('api_image_title')
                            main_image_name = f'{get_img_name}.jpg'
                            file_name = main_image_name.replace(' ', '_')

                            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

                            try:
                                response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key='images/' + file_name)
                                image_data = response['Body'].read()
                            except Exception as e:
                                return HttpResponse(f'Failed to download file: {str(e)}')

                            context = {'file_name': file_name, 'name': name, 'title': title, 'date_posted': date_posted, 'post_timing': post_timing}

                            html_message = render_to_string('testingapp/email_template.html', context)
                            html_message = html_message.replace('cid:file_name', 'cid:{}'.format(file_name))

                            plain_message = strip_tags(html_message)

                            email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
                            email.attach_alternative(html_message, "text/html")

                            img = MIMEImage(image_data, 'jpeg')
                            img.add_header('Content-ID', '<{}>'.format(file_name))
                            email.attach(img)

                            email.send()


                        else: # If image uploaded by user (in production)
                            
                            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

                            image_attachments = []

                            # If more than one image
                            for f in files:
                                file_name = f.name.replace(' ', '_')

                                try:
                                    response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key='images/' + file_name)
                                    image_data = response['Body'].read()
                                except Exception as e:
                                    error = str(e)
                                    # print(error)
                                    return HttpResponse(f'Failed to download file: {str(e)}')

                                
                                post_url = reverse('viewpost', kwargs={'pk': post_instance.pk})
                                context = {'file_name': file_name, 'name': name, 'title': title, 'date_posted': date_posted, 'post_url': post_url, 'post_timing': post_timing}

                                
                                html_message = render_to_string('testingapp/email_template.html', context)
                                html_message = html_message.replace('cid:file_name', 'cid:{}'.format(file_name))

                                plain_message = strip_tags(html_message)

                                email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
                                email.attach_alternative(html_message, "text/html")

                                img = MIMEImage(image_data, 'jpeg')
                                img.add_header('Content-ID', '<{}>'.format(file_name))
                                email.attach(img)

                                image_attachments.append(img)

                           
                            email.send()      

                    else: # If environment is false
                        
                        # If the image was generated using OpenAI 
                        if image_url:
                            img_data = requests.get(image_url).content
                            
                            get_img_name = request.POST.get('api_image_title')
                            main_image_name = f'{get_img_name}.jpg'
                            file_name = main_image_name.replace(' ', '_')                           
                            
                            context = {'file_name': file_name, 'name': name, 'title': title, 'date_posted': date_posted, 'post_timing':post_timing}

                            html_message = render_to_string('testingapp/email_template.html', context)
                            html_message = html_message.replace('cid:file_name', 'cid:{}'.format(file_name))

                            
                            plain_message = strip_tags(html_message)
                            email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
                            email.attach_alternative(html_message, "text/html")

                            image_path = os.path.join(settings.MEDIA_ROOT, 'images', f"{file_name}")
                            # print(image_path, 'image path')
                            if os.path.exists(image_path):
                                with open(image_path, 'rb') as image_file:
                                    img_data = image_file.read()

                            img = MIMEImage(img_data, 'jpeg')
                            img.add_header('Content-ID', '<{}>'.format(file_name))
                            email.attach(img)

                            email.send()

                        else: # If image is uploaded by user
                            
                            main_image_name = f'{uploaded_image.name}'
                            file_name = main_image_name.replace(' ', '_')

                            html_message = render_to_string('testingapp/email_template.html', context)
                            html_message = html_message.replace('cid:uploaded_image', 'cid:{}'.format(file_name))
                            
                            plain_message = strip_tags(html_message)
                            email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
                            email.attach_alternative(html_message, "text/html")

                            
                            image_path = os.path.join(settings.MEDIA_ROOT, 'images', f"{file_name}")
                            print(image_path,'check image')
                            if os.path.exists(image_path):
                                with open(image_path, 'rb') as image_file:
                                    img_data = image_file.read()

                            
                            img = MIMEImage(img_data, 'jpeg')
                            img.add_header('Content-ID', '<{}>'.format(file_name))
                            email.attach(img)

                           
                            email.send()

                 


                successText = post_instance.title
                # sending success message to home page for showing successful form submission
                request.session['success_message'] = successText
                
                # formsubmitted = True
                # context['form_submitted'] = formsubmitted
                request.session['is_form_submitted'] = True
                return redirect('home')
            
            else:
                form = post_form(request.POST, request.FILES)
                newrecipe_error_message = 'Error submitting form'
                return render(request,'testingapp/createpost.html',{'form':form,'newrecipe_error_message':newrecipe_error_message})

            
        else:
            
            form_error = 'Invalid form submission'
            return JsonResponse({'form_error':form_error})


    form = post_form()

    return render(request,'testingapp/createpost.html',{"post_count":post_count,
    "tot_posts_byuser":tot_posts_byuser,"allrecipes":allrecipes,"trnposts":trnposts,"form":form})


def email_template(request):
    return render(request,'testingapp/email_template.html')


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    last_login = user.last_login
    date_joined = user.date_joined

    profile = request.user.profile
    if request.method == 'POST':
        form = EmailNotificationForm(request.POST)
        if form.is_valid():
            send_email = form.cleaned_data.get('send_email', False)
            # Update the user's email notification preference in the database
            request.user.profile.send_email = send_email
            request.user.profile.save()
            return redirect('profile')


    
    form = EmailNotificationForm(initial={'send_email': profile.send_email})

    tot_posts_byuser = post.objects.filter(author=user).all().count()
    allrecipes = post.objects.all().order_by('-date_post').all().count()
    trnposts = post.objects.order_by('-hit_count_generic__hits') [0:4]

    user = request.user
    posts = post.objects.filter(author=user)
    total_hits = posts.aggregate(total=Sum('hit_count_generic__hits'))['total']
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    pass_success = request.session.pop('pass_success', None)

    return render(request,'testingapp/profile.html',{'user':user,'last_login':last_login,
    "tot_posts_byuser":tot_posts_byuser,"allrecipes":allrecipes,"trnposts":trnposts,'form': form,
    'total_hits':total_hits,'is_following':is_following,'pass_success':pass_success})   


@login_required(login_url='login')
def acc_settings(request):
    profile = request.user.profile
    current_year = date.today().year

    yearly_goal, created = YearlyGoal.objects.get_or_create(profile=profile, year=current_year)

    if request.method == 'POST':
        if 'email_form' in request.POST:
            form = EmailNotificationForm(request.POST)
            if form.is_valid():
                send_email = form.cleaned_data.get('send_email', False)

                # Update the user's email notification preference in the database
                request.user.profile.send_email = send_email
                request.user.profile.save()
                return redirect('account_settings')
            
        if 'preference_form' in request.POST:
            preference_form = PreferencesForm(request.POST, instance=request.user.profile)
            if preference_form.is_valid():
                preference_form.save()
                messages.success(request, 'Welcome back', extra_tags='preference-set-message')
                return redirect('account_settings') 
            
            else:
                preference_form = PreferencesForm(instance=request.user.profile)
        
        if 'recipes_goal' in request.POST:
            goal_form = YearlyGoalForm(request.POST, instance=yearly_goal)
            if goal_form.is_valid():
                goal_form.save()
                messages.success(request, 'Recipes goal', extra_tags='recipes-goal-message')
                return redirect('account_settings')

    user_profile = request.user.profile

    # goals set for current year
    goal_for_year = YearlyGoal.objects.filter(profile=user_profile, year=current_year).first()
    goal_for_year_value = goal_for_year.goal if goal_for_year else 0

    # recipes uploaded in current year not counting the previous years recipes
    recipes_uploaded = post.objects.filter(author=request.user, date_post__year=current_year).count()
    
    # Calculate progress percentage
    progress_percentage = (
        (recipes_uploaded / goal_for_year_value) * 100
        if goal_for_year_value > 0 else 0
    )

    form = EmailNotificationForm(initial={'send_email': profile.send_email})
    preference_form = PreferencesForm(instance=request.user.profile)
    goal_form = YearlyGoalForm(instance=yearly_goal)

    all_goals = profile.yearly_goals.order_by('-year')
    return render(request,'testingapp/acc_settings.html',{'form': form,'preference_form':preference_form,
    'goal_form':goal_form,'all_goals':all_goals,'current_year':current_year,
           "recipes_uploaded": recipes_uploaded,
        "goal_for_year": goal_for_year_value,
        "progress_percentage": int(progress_percentage)})



def UpdateProfile(request):
    update_profile = Updatepro(request.POST or None, instance=request.user)
    update_view = Updateview(request.POST or None, request.FILES, instance=request.user.profile)
    if request.method == 'POST':
        
        # print(update_view)
        if update_profile.is_valid() or update_view.is_valid():
            pro = update_profile.save(commit = False)
            view = update_view.save(commit = False)
            pro.save()
            view.save()
                
            return redirect('profile')

        else:
            update_profile = Updatepro(instance=request.user)
            update_view = Updateview(instance=request.user.profile)

    return render(request,'testingapp/updateprofile.html',{'update_profile':update_profile,'update_view':update_view,
    'gender_choices': profile.GENDER_CHOICES,})


from django.contrib.auth import update_session_auth_hash
def UpdatePassword(request):
    user = request.user
    social_account_signup = SocialAccount.objects.filter(user=user).exists()

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get('new_password1')
            if user.check_password(new_password):
                form_error_msg = "The new password cannot be the same as the old password."
                messages.error(request, form_error_msg , extra_tags='form_error_msg')
            
            else:
                form.save()
                update_session_auth_hash(request, form.user)
                pass_success = 'Your password has been updated!'
                request.session['pass_success'] = pass_success
                return redirect('profile')


    else:
        form = SetPasswordForm(user)

    return render(request, 'testingapp/updatepassword.html', {'form': form, 'social_account_signup': social_account_signup})
    

def liked_recipes(request):

    user = request.user

    all_liked_recipes = post.objects.filter(likes__user=request.user).annotate(num_likes=Count('likes')).order_by('-num_likes')
    total_likes = post.objects.filter(likes__user=request.user).count()

    recipes_with_likes = post.objects.filter(author=request.user, likes__isnull=False).annotate(num_likes=Count('likes')).order_by('-num_likes').distinct()
    total_recipes_with_likes = post.objects.filter(author=request.user, likes__isnull=False).distinct().count()

    top_liked_recipe = post.objects.filter(author=user).annotate(num_likes=Count('likes')).order_by('-num_likes')[0:1]
    top_likes = post.objects.filter(author=request.user).annotate(num_likes=Count('likes')).aggregate(most_likes=Max('num_likes'))['most_likes']

    if top_likes is None:
        top_likes = 0


    historys_pk = None

    if request.user.is_authenticated:

        blog_history = BlogHistory.objects.filter(user=user)

        blog_posts = [(entry.pk ,entry.blog_post) for entry in blog_history]

        post_count = []

        for pk,history in blog_posts:
            post_count.append(history.pk)

        historys_pk = [*set(post_count)]

    all_recipes = post.objects.filter().all()

    return render(request,'testingapp/liked_recipes.html',{"all_liked_recipes":all_liked_recipes,"all_recipes":all_recipes,
    "total_likes":total_likes,'recipes_with_likes':recipes_with_likes,'total_recipes_with_likes':total_recipes_with_likes,
    'top_liked_recipe':top_liked_recipe,'top_likes':top_likes,'historys_pk':historys_pk})    

def disliked_recipes(request):
    
    user = request.user

    all_recipes = post.objects.filter().all()

    all_disliked_recipes = post.objects.filter(dislikes__user=request.user).annotate(num_dislikes=Count('dislikes')).order_by('-num_dislikes')
    total_dislikes = post.objects.filter(dislikes__user=request.user).count()

    recipes_with_dislikes = post.objects.filter(author=request.user, dislikes__isnull=False).annotate(num_dislikes=Count('dislikes')).order_by('-num_dislikes').distinct()
    total_recipes_with_dislikes = post.objects.filter(author=request.user, dislikes__isnull=False).distinct().count()

    top_disliked_recipe = post.objects.filter(author=user).annotate(num_dislikes=Count('dislikes')).order_by('-num_dislikes')[0:1]
    top_dislikes = post.objects.filter(author=request.user).annotate(num_dislikes=Count('dislikes')).aggregate(most_dislikes=Max('num_dislikes'))['most_dislikes']

    if top_dislikes is None:
        top_dislikes = 0

    historys_pk = None

    if request.user.is_authenticated:

        blog_history = BlogHistory.objects.filter(user=user)

        blog_posts = [(entry.pk ,entry.blog_post) for entry in blog_history]

        post_count = []

        for pk,history in blog_posts:
            post_count.append(history.pk)

        historys_pk = [*set(post_count)]

    return render(request,'testingapp/disliked_recipes.html',{"all_recipes":all_recipes,"all_disliked_recipes":all_disliked_recipes,"total_dislikes":total_dislikes,
    "total_dislikes":total_dislikes,'recipes_with_dislikes':recipes_with_dislikes,'total_recipes_with_dislikes':total_recipes_with_dislikes,'top_disliked_recipe':top_disliked_recipe,
    'top_dislikes':top_dislikes,'historys_pk':historys_pk})    



@login_required(login_url='login')
def timeline(request):

    user = request.user

    main = post.objects.filter(author=user).all()

    all_recipes = post.objects.filter().all()     

    monthnum = []

    for x in range(1,13):
        monthnum.append(x)

    nowmonth = datetime.date.today().month
    Jan1 = monthnum[0]
    Feb2 = monthnum[1]
    Mar3 = monthnum[2]
    Apr4 = monthnum[3]
    May5 = monthnum[4]
    June6 = monthnum[5]
    July7 = monthnum[6]
    Aug8 = monthnum[7]
    Sep9 = monthnum[8]
    Oct10 = monthnum[9]
    Nov11 = monthnum[10]
    Dec12 = monthnum[11]

    get_month = datetime.date.today()
    currmonth = get_month.strftime('%B')

    curyear = datetime.datetime.today().year
    
    b = datetime.datetime.today().year

    posts = []
    stryear = [] 
    trecipes = []

    # cur_year_posts = []
    # cur_year_posts = 0
    # this_year_posts = 0

    prev_years = 0
    prev_jan = 0
    prev_total_jan_posts =0 
    prev_janfamrecipe = 0
    prev_feb = 0
    prev_total_feb_posts = 0
    prev_febfamrecipe = 0
    prev_mar = 0
    prev_total_mar_posts = 0
    prev_marfamrecipe = 0
    prev_apr = 0
    prev_total_apr_posts = 0
    prev_aprfamrecipe = 0
    prev_may = 0
    prev_total_may_posts = 0
    prev_mayfamrecipe = 0
    prev_june = 0
    prev_total_june_posts = 0
    prev_junefamrecipe = 0
    prev_july = 0
    prev_total_july_posts = 0
    prev_julyfamrecipe = 0
    prev_aug = 0
    prev_total_aug_posts = 0
    prev_augfamrecipe = 0
    prev_sep = 0
    prev_total_sep_posts = 0
    prev_sepfamrecipe = 0
    prev_oct = 0
    prev_total_oct_posts = 0
    prev_octfamrecipe = 0
    prev_nov = 0
    prev_total_nov_posts = 0
    prev_novfamrecipe = 0
    prev_dec = 0
    prev_total_dec_posts = 0
    prev_decfamrecipe = 0
    
    prev_brkfsts = 0
    prev_lnch = 0
    prev_evesnck = 0
    prev_dnr = 0

    totalrecipes = post.objects.filter(author=user,date_post__year = curyear).all().count()    

    date_list = post.objects.filter(author=user).dates('date_post', 'year')
    joined = user.date_joined.date().year

    # prev_years = post.objects.filter(author=user,date_post__year = joined).count()

    year_list = []

    prev_recipe_counts = [0] * 12  # Initialize prev_recipe_counts with zeros for all months
    prev_chart_data = 0
    recipe_counts = [0] * 12  # Initialize recipe_counts with zeros for all months
    
    for i in range(joined,curyear+1):
        year_list.append(i)

        # posts = post.objects.filter(author=user,date_post__year = i)
        
        prev_months = [calendar.month_name[i] for i in range(1, 13)]  # List of all month names

        if i != curyear:
            prev_years = post.objects.filter(author=user,date_post__year = i).count()
            # print(prev_years)

            prev_jan = post.objects.filter(author=user,date_post__year = i,date_post__month='01')
            prev_total_jan_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='01').count()
            prev_janfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='01').order_by('hit_count_generic__hits').last()

            prev_feb = post.objects.filter(author=user,date_post__year = i,date_post__month='02')
            prev_total_feb_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='02').count()
            prev_febfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='02').order_by('hit_count_generic__hits').last()

            prev_mar = post.objects.filter(author=user,date_post__year = i,date_post__month='03')
            prev_total_mar_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='03').count()
            prev_marfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='03').order_by('hit_count_generic__hits').last()

            prev_apr = post.objects.filter(author=user,date_post__year = i,date_post__month='04')
            prev_total_apr_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='04').count()
            prev_aprfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='04').order_by('hit_count_generic__hits').last()

            prev_may = post.objects.filter(author=user,date_post__year = i,date_post__month='05')
            prev_total_may_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='05').count()
            prev_mayfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='05').order_by('hit_count_generic__hits').last()
            
            prev_june = post.objects.filter(author=user,date_post__year = i,date_post__month='06')
            prev_total_june_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='06').count()
            prev_junefamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='06').order_by('hit_count_generic__hits').last()

            prev_july = post.objects.filter(author=user,date_post__year = i,date_post__month='07')
            prev_total_july_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='07').count()
            prev_julyfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='07').order_by('hit_count_generic__hits').last()

            prev_aug = post.objects.filter(author=user,date_post__year = i,date_post__month='08')
            prev_total_aug_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='08').count()
            prev_augfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='08').order_by('hit_count_generic__hits').last()

            prev_sep = post.objects.filter(author=user,date_post__year = i,date_post__month='09')
            prev_total_sep_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='09').count()
            prev_sepfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='09').order_by('hit_count_generic__hits').last()

            prev_oct = post.objects.filter(author=user,date_post__year = i,date_post__month='10')
            prev_total_oct_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='10').count()
            prev_octfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='10').order_by('hit_count_generic__hits').last()

            prev_nov = post.objects.filter(author=user,date_post__year = i,date_post__month='11')
            prev_total_nov_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='11').count()
            prev_novfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='11').order_by('hit_count_generic__hits').last()

            prev_dec = post.objects.filter(author=user,date_post__year = i,date_post__month='12')
            prev_total_dec_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='12').count()
            prev_decfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='12').order_by('hit_count_generic__hits').last()

            prev_brkfsts = post.objects.filter(author=user,date_post__year = i,type='Breakfast').order_by('hit_count_generic__hits').all()
            prev_lnch = post.objects.filter(author=user,date_post__year = i,type='Lunch').order_by('hit_count_generic__hits').all()
            prev_evesnck = post.objects.filter(author=user,date_post__year = i,type='Evening Snack').order_by('hit_count_generic__hits').all()
            prev_dnr = post.objects.filter(author=user,date_post__year = i,type='Dinner').order_by('hit_count_generic__hits').all()

            prev_recipe_data = post.objects.annotate(month=Extract('date_post',lookup_name='month')).values('month').annotate(recipe_count=Count('id')).order_by('month').filter(author=user,date_post__year = i)

            # data for the chart
            prev_months = [calendar.month_name[i] for i in range(1, 13)]  # List of all month names
            # prev_recipe_counts = [0] * 12  # Initialize recipe counts with zeros for all months

            # Update the recipe counts for the corresponding months
            for data in prev_recipe_data:
                month_index = data['month'] - 1  # Adjust month index to match list indices (starting from 0)
                prev_recipe_counts[month_index] = data['recipe_count']

            prev_chart_data = {
                'prev_months': prev_months,
                'recipeCounts': prev_recipe_counts
            }

        this_year_posts = post.objects.filter(author=user,date_post__year = curyear).count()


        if i == curyear:
            cur_year_posts = post.objects.filter(author=user,date_post__year = i).count()
            
            jan = post.objects.filter(author=user,date_post__year = i,date_post__month='01')
            total_jan_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='01').count()
            janfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='01').order_by('hit_count_generic__hits').last()

            feb = post.objects.filter(author=user,date_post__year = i,date_post__month='02')
            total_feb_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='02').count()
            febfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='02').order_by('hit_count_generic__hits').last()

            mar = post.objects.filter(author=user,date_post__year = i,date_post__month='03')
            total_mar_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='03').count()
            marfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='03').order_by('hit_count_generic__hits').last()

            apr = post.objects.filter(author=user,date_post__year = i,date_post__month='04')
            total_apr_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='04').count()
            aprfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='04').order_by('hit_count_generic__hits').last()

            may = post.objects.filter(author=user,date_post__year = i,date_post__month='05')
            total_may_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='05').count()
            mayfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='05').order_by('hit_count_generic__hits').last()

            june = post.objects.filter(author=user,date_post__year = i,date_post__month='06')
            total_june_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='06').count()
            junefamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='06').order_by('hit_count_generic__hits').last()

            july = post.objects.filter(author=user,date_post__year = i,date_post__month='07')
            total_july_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='07').count()
            julyfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='07').order_by('hit_count_generic__hits').last()

            aug = post.objects.filter(author=user,date_post__year = i,date_post__month='08')
            total_aug_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='08').count()
            augfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='08').order_by('hit_count_generic__hits').last()

            sep = post.objects.filter(author=user,date_post__year = i,date_post__month='09')
            total_sep_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='09').count()
            sepfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='09').order_by('hit_count_generic__hits').last()

            oct = post.objects.filter(author=user,date_post__year = i,date_post__month='10')
            total_oct_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='10').count()
            octfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='10').order_by('hit_count_generic__hits').last()

            nov = post.objects.filter(author=user,date_post__year = i,date_post__month='11')
            total_nov_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='11').count()
            novfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='11').order_by('hit_count_generic__hits').last()

            dec = post.objects.filter(author=user,date_post__year = i,date_post__month='12')
            total_dec_posts = post.objects.filter(author=user,date_post__year = i,date_post__month='12').count()
            decfamrecipe = post.objects.filter(author=user,date_post__year = i,date_post__month='12').order_by('hit_count_generic__hits').last()
        
        
            brkfsts = post.objects.filter(author=user,date_post__year = i,type='Breakfast').order_by('hit_count_generic__hits').all()
            lnch = post.objects.filter(author=user,date_post__year = i,type='Lunch').order_by('hit_count_generic__hits').all()
            evesnck = post.objects.filter(author=user,date_post__year = i,type='Evening Snack').order_by('hit_count_generic__hits').all()
            dnr = post.objects.filter(author=user,date_post__year = i,type='Dinner').order_by('hit_count_generic__hits').all()
    
            # Retrieve the recipe data from the post model
            recipe_data = post.objects.annotate(month=Extract('date_post',lookup_name='month')).values('month').annotate(recipe_count=Count('id')).order_by('month').filter(author=user,date_post__year = i)

            # Prepare the data for the chart
            months = [calendar.month_name[i] for i in range(1, 13)]  # List of all month names
            # recipe_counts = [0] * 12  # Initialize recipe counts with zeros for all months

            # Update the recipe counts for the corresponding months
            for data in recipe_data:
                month_index = data['month'] - 1  # Adjust month index to match list indices (starting from 0)
                recipe_counts[month_index] = data['recipe_count']

            # Create a dictionary to hold the chart data
            chart_data = {
                'months': months,
                'recipeCounts': recipe_counts
            }
  
  
        
    cyearposts = str(posts)[1:-1]

    tot_posts_byuser = post.objects.filter(author=user).all().count()
    allrecipes = post.objects.all().order_by('-date_post').all().count()
    trnposts = post.objects.order_by('-hit_count_generic__hits') [0:4]

    return render(request,'testingapp/timeline.html',
    {"date":date,'prev_months':prev_months,'prev_recipe_counts':prev_recipe_counts,'recipe_data': json.dumps(chart_data),
    'year_list':year_list,'curyear':curyear,'prev_recipe_data': json.dumps(prev_chart_data),
    "all_recipes":all_recipes,'b':b,'trecipes':trecipes,"curyear":curyear,"totalrecipes":totalrecipes,
    'nowmonth':nowmonth,"tot_posts_byuser":tot_posts_byuser,"allrecipes":allrecipes,"trnposts":trnposts,
    'Jan1':Jan1,'Feb2':Feb2,'Mar3':Mar3,'Apr4':Apr4,'May5':May5,'June6':June6,
    'July7':July7,'Aug8':Aug8,'Sep9':Sep9,'Oct10':Oct10,'Nov11':Nov11,'Dec12':Dec12,
    'currmonth':currmonth,'joined':joined,
    'cyearposts':cyearposts,"year_list":year_list,
    'stryear':stryear,'posts':posts,'this_year_posts':this_year_posts,
    'date_list':date_list,'prev_years':prev_years,'cur_year_posts':cur_year_posts,
    'jan':jan,'total_jan_posts':total_jan_posts,'janfamrecipe':janfamrecipe,
    'prev_jan':prev_jan,'prev_total_jan_posts':prev_total_jan_posts,'prev_janfamrecipe':prev_janfamrecipe,
    
    'feb':feb,'total_feb_posts':total_feb_posts,'febfamrecipe':febfamrecipe,
    'prev_feb':prev_feb,'prev_total_feb_posts':prev_total_feb_posts,'prev_febfamrecipe':prev_febfamrecipe,
    
    'mar':mar,'total_mar_posts':total_mar_posts,'marfamrecipe':marfamrecipe,
    'prev_mar':prev_mar,'prev_total_mar_posts':prev_total_mar_posts,'prev_marfamrecipe':prev_marfamrecipe,
    
    'apr':apr,'total_apr_posts':total_apr_posts,'aprfamrecipe':aprfamrecipe,
    'prev_apr':prev_apr,'prev_total_apr_posts':prev_total_apr_posts,'prev_aprfamrecipe':prev_aprfamrecipe,
    
    'may':may,'total_may_posts':total_may_posts,'mayfamrecipe':mayfamrecipe,
    'prev_may':prev_may,'prev_total_may_posts':prev_total_may_posts,'prev_mayfamrecipe':prev_mayfamrecipe,
    
    'june':june,'total_june_posts':total_june_posts,'junefamrecipe':junefamrecipe,
    'prev_june':prev_june,'prev_total_june_posts':prev_total_june_posts,'prev_junefamrecipe':prev_junefamrecipe,
    
    'july':july,'total_july_posts':total_july_posts,'julyfamrecipe':julyfamrecipe,
    'prev_july':prev_july,'prev_total_july_posts':prev_total_july_posts,'prev_julyfamrecipe':prev_julyfamrecipe,
    
    'aug':aug,'total_aug_posts':total_aug_posts,'augfamrecipe':augfamrecipe,
    'prev_aug':prev_aug,'prev_total_aug_posts':prev_total_aug_posts,'prev_augfamrecipe':prev_augfamrecipe,
    
    'sep':sep,'total_sep_posts':total_sep_posts,'sepfamrecipe':sepfamrecipe,
    'prev_sep':prev_sep,'prev_total_sep_posts':prev_total_sep_posts,'prev_sepfamrecipe':prev_sepfamrecipe,
    
    'oct':oct,'total_oct_posts':total_oct_posts,'octfamrecipe':octfamrecipe,
    'prev_oct':prev_oct,'prev_total_oct_posts':prev_total_oct_posts,'prev_octfamrecipe':prev_octfamrecipe,
    
    'nov':nov,'total_nov_posts':total_nov_posts,'novfamrecipe':novfamrecipe,
    'prev_nov':prev_nov,'prev_total_nov_posts':prev_total_nov_posts,'prev_novfamrecipe':prev_novfamrecipe,
    
    'dec':dec,'total_dec_posts':total_dec_posts,'decfamrecipe':decfamrecipe,
    'prev_dec':prev_dec,'prev_total_dec_posts':prev_total_dec_posts,'prev_decfamrecipe':prev_decfamrecipe,
    
    'prev_brkfsts':prev_brkfsts,'prev_lnch':prev_lnch,'prev_evesnck':prev_evesnck,'prev_dnr':prev_dnr,
    'brkfsts':brkfsts,'lnch':lnch,'evesnck':evesnck,'dnr':dnr,
    
    })



def generate_recipe_with_ai_image(request):

    if request.method == 'POST' and request.POST.get("img_type") == 'recipeimage':
        try:

            image_generation_form = AIRecipeGenerationForm(request.POST)

            if image_generation_form.is_valid():
                # Get the title from the image generation form
                title = image_generation_form.cleaned_data['title']

                # if OpenAI API is available then generate both recipe and its image
                if openai.api_key:
                    openai.api_key = settings.OPENAI_API_KEY

                    # Generate an image based on the user's input
                    response = openai.Image.create(
                        prompt=title,
                        n=1,
                        size="256x256"
                    )

                    try:
                        # Download the generated image
                        recipe_image_url = response.data[0].url
                    except (AttributeError, KeyError):
                        # Handle the case where the response structure doesn't provide a direct URL
                        recipe_image_url = None
                
                    # Call the second function to generate the recipe    
                    generated_recipe = generate_recipe(title)

                    formatted_generated_recipe = generated_recipe.replace('\n', '<br>')

                    if recipe_image_url:
                        return JsonResponse({"recipe_image_url": recipe_image_url,"generated_recipe": formatted_generated_recipe})
                
                # Else use Gemini API to generate textual recipe only
                else: 
                    generated_recipe = generate_recipe(title)

                    formatted_generated_recipe = generated_recipe.replace('\n', '')

                    return JsonResponse({"recipe_image_url": None,"generated_recipe": formatted_generated_recipe})


        except Exception as e:
            error = str(e)
            return JsonResponse({"error": error})

    form = AIRecipeGenerationForm()
    return render(request, 'testingapp/generate_recipe.html', {'form': form})



def generate_recipe(title):
    try:
        # Generate recipe using OpenAI API
        # recipe_prompt = f"Generate a recipe for {title}."
        # recipe_response = openai.Completion.create(
        #     engine="gpt-3.5-turbo-instruct",
        #     prompt=recipe_prompt,
        #     max_tokens=50,
        #     temperature=0.7,
        #     n=1,
        # )

        # generated_recipe = recipe_response.choices[0].text.strip()

        # return generated_recipe

        '''-------------------------------------------------------------'''

        # Generating recipe using Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Generate a recipe for {title} with detailed nutritional information in grams only not for ingredients (nutritional inforamtion should be in table format and at top) . Also provide prep time, cook time, servings, variation and best time to consume. Include a numbered bullet-point list for ingredients and instructions. Do not use any special characters in anywhere just use periods (.) in the bullet points. Output should be in HTML formatted without ''' and html. At last add a happy cooking message or related similar with emoji with some vertical space."
        )

        generated_recipe = response.text

        return generated_recipe

    except Exception as e:
        error = str(e)
        return JsonResponse({"error": error})
    


def year_recap(request):
    
    curyear = datetime.datetime.today().year

    user = request.user
    
    all_recipes = post.objects.filter().all()

    if request.user.is_authenticated:

        auth_trending_recipes = post.objects.filter(author=user,date_post__year = curyear).order_by('-hit_count_generic__hits')

        year_recap = post.objects.filter(author=user,date_post__year = curyear).all()

        total_recipes = post.objects.filter(author=user,date_post__year = curyear).count()
        total_breakfast = post.objects.filter(author=user,type ='Breakfast',date_post__year = curyear).count()
        total_lunch = post.objects.filter(author=user,type ='Lunch',date_post__year = curyear).count()
        total_evesnack = post.objects.filter(author=user,type ='Evening Snack',date_post__year = curyear).count()
        total_dinner = post.objects.filter(author=user,type ='Dinner',date_post__year = curyear).count()
        totalveg = post.objects.filter(author=user,category='Veg',date_post__year = curyear).count()
        totalnonveg = post.objects.filter(author=user,category='Non-Veg',date_post__year = curyear).count()


        top_breakfast = post.objects.filter(author=user,type ='Breakfast',date_post__year = curyear).order_by('-hit_count_generic__hits')
        top_lunch = post.objects.filter(author=user,type ='Lunch',date_post__year = curyear).order_by('-hit_count_generic__hits')
        top_evesnack = post.objects.filter(author=user,type ='Evening Snack',date_post__year = curyear).order_by('-hit_count_generic__hits')
        top_dinner = post.objects.filter(author=user,type ='Dinner',date_post__year = curyear).order_by('-hit_count_generic__hits')

        topveg = post.objects.filter(author=user,category='Veg',date_post__year = curyear).order_by('-hit_count_generic__hits')
        topnonveg = post.objects.filter(author=user,category='Non-Veg',date_post__year = curyear).order_by('-hit_count_generic__hits')


        most_liked_recipe_count = post.objects.filter(author=request.user,date_post__year = curyear).annotate(like_count=Count('likes')).order_by('-like_count').first()

        most_liked_recipe = post.objects.filter(author=request.user,date_post__year = curyear).annotate(like_count=Count('likes')).order_by('-like_count')

        if most_liked_recipe_count:
            total_likes = most_liked_recipe_count.like_count
        else:
            total_likes = 0

    else:
        return redirect('login')

    return render(request,'testingapp/year_recap.html',{'all_recipes':all_recipes,'auth_trending_recipes':auth_trending_recipes,'year_recap':year_recap,'curyear':curyear,
    'total_recipes':total_recipes,'top_breakfast':top_breakfast,'top_lunch':top_lunch,'top_evesnack':top_evesnack,'top_dinner':top_dinner,'topveg':topveg,'topnonveg':topnonveg,
    'most_liked_recipe':most_liked_recipe,'total_likes':total_likes,'total_breakfast':total_breakfast,'total_lunch':total_lunch,'total_evesnack':total_evesnack,
    'total_dinner':total_dinner,'totalveg':totalveg,'totalnonveg':totalnonveg})




def newnavbarnavrail(request):
    form = SearchForm(request.GET)

    all_recipes = post.objects.filter().all()
    
    return render(request,'testingapp/newnavbar_navrail.html',{"form": form,'all_recipes':all_recipes})



@login_required(login_url='login')
def favorite_list(request):
    new = post.objects.filter(favourites=request.user)
    all_recipes = post.objects.filter().all()
    return render(request,'testingapp/favourites.html',{"new":new,"all_recipes":all_recipes})


from django.template.loader import render_to_string

@login_required
def add_to_favorites(request, id):
    blog = get_object_or_404(post, id=id)
    recipe_name = post.objects.get(id=id)
    recipe_title = recipe_name.title
    new = post.objects.filter(favourites=request.user)

    if blog.favourites.filter(id=request.user.id).exists():
        blog.favourites.remove(request.user)
        action = 'remove'
    else:
        blog.favourites.add(request.user)
        action = 'add'

    # Render the updated HTML for the favourites page (updating favourites page using update_recipe_card.html page without reloadinq)
    updated_html = render(request, 'testingapp/update_recipe_card.html', {'post': blog, 'user': request.user}).content.decode('utf-8')
    # print(updated_html)
    return JsonResponse({'action': action,'recipe_title':recipe_title,'updated_html': updated_html, 'post_id': id})
        
    
    # return HttpResponseRedirect(request.META['HTTP_REFERER'])





def post_chart(request):

    user = request.user
    curyear = datetime.datetime.today().year
    joined = user.date_joined.date().year
    year_list = []

    prev_recipe_counts = [0] * 12  # Initialize prev_recipe_counts with zeros for all months
        
    prev_chart_data = 0  # Initialize prev_recipe_counts with zeros for all months
    recipe_counts = [0] * 12  # Initialize recipe_counts with zeros for all months
    
    for i in range(joined,curyear+1):
        year_list.append(i)

        if i != curyear:

            # Retrieve the recipe data from the post model
            prev_recipe_data = post.objects.annotate(month=Extract('date_post',lookup_name='month')).values('month').annotate(recipe_count=Count('id')).order_by('month').filter(author=request.user,date_post__year = i)

            # Prepare the data for the chart
            months = [calendar.month_name[i] for i in range(1, 13)]  # List of all month names
            prev_recipe_counts = [0] * 12  # Initialize recipe counts with zeros for all months

            # Update the recipe counts for the corresponding months
            for data in prev_recipe_data:
                month_index = data['month'] - 1  # Adjust month index to match list indices (starting from 0)
                prev_recipe_counts[month_index] = data['recipe_count']

            # Create a dictionary to hold the chart data
            prev_chart_data = {
                'months': months,
                'recipeCounts': prev_recipe_counts
            }

        
        if i == curyear:

            # Retrieve the recipe data from the post model
            recipe_data = post.objects.annotate(month=Extract('date_post',lookup_name='month')).values('month').annotate(recipe_count=Count('id')).order_by('month').filter(author=request.user,date_post__year = i)

            # Prepare the data for the chart
            months = [calendar.month_name[i] for i in range(1, 13)]  # List of all month names
            recipe_counts = [0] * 12  # Initialize recipe counts with zeros for all months

            # Update the recipe counts for the corresponding months
            for data in recipe_data:
                month_index = data['month'] - 1  # Adjust month index to match list indices (starting from 0)
                recipe_counts[month_index] = data['recipe_count']

            # Create a dictionary to hold the chart data
            chart_data = {
                'months': months,
                'recipeCounts': recipe_counts
            } 

    return render(request, 'testingapp/post_chart.html',{'prev_recipe_data': json.dumps(prev_chart_data),
    'recipe_data': json.dumps(chart_data),'year_list':year_list,'curyear':curyear})




@login_required(login_url='login')
def credits(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        redeem_amount = int(request.POST.get('redeem_amount', 0))

        # Ensure the redeem amount is not greater than the earned credits
        redeem_amount = min(redeem_amount, profile.earned_credits)

        # Add the redeem amount to the credits field
        profile.credits += redeem_amount

        # Add the redeemed credits to the redeemed_credits field
        profile.redeemed_credits += redeem_amount

        redeemed_credit = RedeemedCredit.objects.create(user=user, amount=redeem_amount)

        profile.earned_credits -= redeem_amount

        profile.save()

        return redirect('credits')

    redeemed_credits = RedeemedCredit.objects.filter(user=user)

    credit_history = CreditHistory.objects.filter(user=user)

    credit_spent_history = CreditSpentHistory.objects.filter(user=user)

    credit_spent_by_month = credit_spent_history.annotate(month=TruncMonth('spent_timestamp')).values('month').annotate(total_credits_spent=Sum('amount'))

    # Calculate the total number of months for which there are credit spent records
    total_months = credit_spent_by_month.count()

    total_credits_spent = sum(entry['total_credits_spent'] for entry in credit_spent_by_month)

    if total_months > 0:
        average_credit_spent = total_credits_spent / total_months
    else:
        average_credit_spent = 0

    credit_spent_by_month = (
        CreditSpentHistory.objects.filter(user=user).annotate(month=ExtractMonth('spent_timestamp'))
        .values('month')
        .annotate(total_credits_spent=Sum('amount'))
    )

    average_credit_spent_month = (
        CreditSpentHistory.objects.filter(user=user).aggregate(avg_credit_spent=Avg('amount'))['avg_credit_spent']
    )

    credit_spent_by_month_json = json.dumps(list(credit_spent_by_month))
    average_credit_spent_json = json.dumps(average_credit_spent_month)


    return render(request, 'testingapp/credits.html', {'redeemed_credits': redeemed_credits,
    'credit_history':credit_history,'credit_spent_history':credit_spent_history,'total_credits_spent': total_credits_spent,
        'average_credit_spent': average_credit_spent,'credit_spent_by_month_json':credit_spent_by_month_json,'average_credit_spent_json':average_credit_spent_json})


@login_required(login_url='login')
def delete_redeemed_history(request):
    if request.method == 'POST':
        redeemed_history_ids = request.POST.getlist('redeemed_history')
        RedeemedCredit.objects.filter(id__in=redeemed_history_ids, user=request.user).delete()
        return redirect('credits')
    else:
        return HttpResponseForbidden("Unable to perform this action.")


@login_required(login_url='login')
def delete_credit_history(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_history')
        CreditHistory.objects.filter(id__in=selected_ids, user=request.user).delete()
        return redirect('credits')
    else:
        return HttpResponseForbidden("Unable to perform this action.")

@login_required(login_url='login')
def delete_spent_history(request):
    if request.method == 'POST':
        spent_history_ids = request.POST.getlist('spent_history')
        CreditSpentHistory.objects.filter(id__in=spent_history_ids, user=request.user).delete()
        return redirect('credits')
    else:
        return HttpResponseForbidden("Unable to perform this action.")


def total_views(request):
    user = request.user
    posts = post.objects.filter(author=user)

    distinct_years = post.objects.filter(author=user).dates('date_post', 'year').reverse()

    year_recipes = {}
    year_hits = {}
    avg_hits = {}
    most_hit = {}

    for year in distinct_years:
        recipes_for_year = post.objects.filter(author=user, date_post__year=year.year)
        year_recipes[year.year] = recipes_for_year
        
        total_hits_per_year = post.objects.filter(author=user, date_post__year=year.year).aggregate(total=Sum('hit_count_generic__hits'))['total']
        year_hits[year.year] = total_hits_per_year
       
        total_hits_avg = post.objects.filter(author=user, date_post__year=year.year).aggregate(total=Avg('hit_count_generic__hits'))['total']
        avg_hits[year.year] = total_hits_avg

        top_hit = post.objects.filter(author=user, date_post__year=year.year).order_by('-hit_count_generic__hits').first()
        most_hit[year.year] = top_hit
        

    return render(request, 'testingapp/total_views.html',{'distinct_years':distinct_years,'year_recipes':year_recipes,'year_hits':year_hits,
    'avg_hits':avg_hits,'most_hit':most_hit,'posts':posts})


def feedback_view(request):
    try:
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.user = request.user 
                feedback.save()
                messages.success(request, 'Feedback submitted', extra_tags='feedback')

                return redirect('feedback') 
        else:
            form = FeedbackForm()

        user_feedback = Feedback.objects.filter(user=request.user)
        feedback_len = Feedback.objects.filter(user=request.user).count()
        return render(request, 'testingapp/feedback_form.html', {'form': form,'user_feedback': user_feedback,'feedback_len': feedback_len})
    except Exception as e:
        error = str(e)
        return render(request, 'testingapp/feedback_form.html', {'error_message': error})

@login_required
def follow_unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    current_user_profile = profile.objects.get(user=request.user)
    followed = False
    authenticated_user = False

    if request.user != target_user:
        #if user is following the targered user 
        if Follow.objects.filter(follower=request.user, following=target_user).exists():
            # Then unfollow the targeted user
            Follow.objects.filter(follower=request.user, following=target_user).delete()
            
            # Delete the following notification
            Notification.objects.filter(actor_object_id=request.user.id, recipient=target_user, verb='following').delete()
        else:
            # Follow the targeted user
            Follow.objects.create(follower=request.user, following=target_user)
            followed = True
            
            notify.send(
                sender=request.user,
                recipient=target_user,
                verb='following',
            )
    else:
        authenticated_user = True

    if followed:
        messages.success(request, f'{target_user.get_full_name()}', extra_tags='follow_message')

    if authenticated_user:
        messages.success(request, f'Action not allowed', extra_tags='same_user')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

from itertools import chain
from collections import OrderedDict

@login_required
def followers_list(request, name, pk):
    
    user = request.user
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)

    follower_years_qs = Follow.objects.filter(following=user).dates('created_at', 'year')
    following_years_qs = Follow.objects.filter(follower=user).dates('created_at', 'year')
    distinct_years = sorted(set(chain(follower_years_qs, following_years_qs)), reverse=True)

    year_data = {}
    year_data_history = OrderedDict()

    for year in distinct_years:
        year_int = year.year
        followers_for_year = Follow.objects.filter(following=user, created_at__year=year_int)
        followings_for_year = Follow.objects.filter(follower=user, created_at__year=year_int)

        year_data[year_int] = {
            'followers': followers_for_year,
            'followings': followings_for_year,
        }

        year_data_history[year_int] = {}

        for month in range(1, 13):
            month_name = calendar.month_name[month]
            
            followers_for_month = Follow.objects.filter(following=user, created_at__year=year_int, created_at__month=month)
            followings_for_month = Follow.objects.filter(follower=user, created_at__year=year_int, created_at__month=month)
            total_followers_count = Follow.objects.filter(following=user, created_at__year=year_int).count()
            total_followings_count = Follow.objects.filter(follower=user, created_at__year=year_int).count()
            
            if followers_for_month.exists() or followings_for_month.exists():
                year_data_history[year_int][month_name] = {
                    'followers': followers_for_month,
                    'followings': followings_for_month,
                    'followers_obj':followers_for_year,
                    'followings_obj':followings_for_year,
                    'monthly_followers_count':total_followers_count,
                    'monthly_followings_count':total_followings_count,
                }
            else:
                year_data_history[year_int][month_name] = {
                    'followers': '',
                    'followings': '',
                    'followers_obj':'',
                    'followings_obj':'',
                }

    

    
    return render(request, 'testingapp/connections.html', {'user': user, 'followers': followers, 'following': following,
    'followers_count':followers_count,'following_count':following_count,'distinct_years':distinct_years,'year_data':year_data,
    'year_data_history':year_data_history})