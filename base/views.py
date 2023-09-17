# importing dependencies
from django.shortcuts import render, redirect
from .models import Nutrition, User
from .forms import ExtractForm, NutrtionForm, UploadForm, MyUserCreationForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import os
import glob
import json
import openai
import requests
from dotenv import load_dotenv

from base.recipe_option import dietlabels, healthlabels, dishtype, cuisinetype

load_dotenv()

# OPENAI API_KEY
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


# Edamam API
api_id = os.getenv("EDAMAM_API_ID")
api_key = os.getenv('EDAMAM_API_KEY')


# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User Does not exist!!!')

        # Authentication
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credentials Incorrect!')

    context = {'page': page}
    return render(request, 'base/login.html', context)


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            # Freeze the user object so we can mainpulate (i.e, lowercase it simultaneously)
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration!')

    context = {'form': form}
    return render(request, 'base/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    context = {}
    return render(request, 'base/home.html', context)

# Scan


def upload_and_extract(request):
    form = UploadForm

    # Uploading the photo
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # * means all if need specific format then *.csv
            list_of_files = glob.glob(
                '/Users/arshad/Desktop/Projects/Healthy-Eats/static/images/*')
            # selecting the latest file
            food_label = max(list_of_files, key=os.path.getctime)

            # Prompt Template
            ingredients_template = PromptTemplate(
                input_variables=['food_label'],
                template="""You are a great Ingredient Parser who can extract ingredients from a given food label text.
                Extract the ingredients from the following food_label:
                FOOD LABEL: {food_label}"""
            )

            template_string = """You are a master ingredient parser from a given food label. You give detailed descriptions of the ingredients\
            You can classify each ingredient as Healthy/Unhealthy.
            You also add emojis for each ingredient.

            Take the Food Label below delimited by triple backticks and use it to extract the ingredients and provide a detailed description.

            brand description: ```{food_label}```

            then based on the description you give the brand an Emoji and a label for healthy or unhelathy.

            Format the output as JSON with the following keys:
            Ingredient
            Description
            Emoji
            Healthy/Unhealthy label
            """

            prompt_template = ChatPromptTemplate.from_template(template_string)

            chat_llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
            llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
            ingredients_chain = LLMChain(
                llm=llm, prompt=ingredients_template, verbose=True, output_key='ingredients')

            ingredients_list = prompt_template.format_messages(
                food_label=ingredients_chain.run(food_label))

            response = chat_llm(ingredients_list)

            get_response = response.content

            data_dict = json.loads(get_response)
            parsed_dict = data_dict['ingredients']

            print(parsed_dict)

            context = {'form': form, 'parsed_dict': parsed_dict,}
            return render(request, 'base/result.html', context)

    context = {'form': form}
    return render(request, 'base/upload_extract.html', context)


# recipe search
def recipe(request):

    if request.GET.get('ingredients') or request.GET.get('dishType') or request.GET.get('allergies') or request.GET.get('cuisine'):
        ing = request.GET.getlist('ingredients'),
        ingredients_list = [i.lower().strip() for i in filter(None, ing[0])]

        dish_l = request.GET.getlist('dishType'),
        dish_list = list(dish_l)
        diet_l = request.GET.getlist('dietLabels'),
        diet_list = list(diet_l)
        health_l = request.GET.getlist('healthLabels'),
        health_list = list(health_l)
        cuisine_l = request.GET.getlist('cuisineType')
        cuisine_list = list(cuisine_l)

        ingredients = str(','.join(ingredients_list))

        dish_Array = []
        for d in dish_list[0]:
            dish_Array.append("&dishType=" + d)

        d_Array = []
        for d in diet_list[0]:
            d_Array.append("&diet=" + d)

        h_Array = []
        for h in health_list[0]:
            h_Array.append("&health=" + h)

        c_Array = []
        for c in cuisine_list:
            c_Array.append("&cuisineType=" + c)

        dishType = ''.join(dish_Array)
        dietLabels = ''.join(d_Array)
        healthLabels = ''.join(h_Array)
        cuisineType = ''.join(c_Array)

        # Concat all parameters
        param = ''.join(ingredients+dishType+dietLabels +
                        healthLabels+cuisineType)

        url = f"https://api.edamam.com/api/recipes/v2?type=public&app_id={api_id}&app_key={api_key}&q={param}"

        response = requests.get(url)  # returns response e.g. 200
        data = response.json()  # returns actual API content

        hits = data["hits"]

        context = {'hits': hits}
        return render(request, 'base/recipe_result.html', context)

    context = {'dietlabels': dietlabels, 'healthlabels': healthlabels,
               'dishtype': dishtype, 'cuisinetype': cuisinetype}
    return render(request, 'base/recipe.html', context)


# Nutrition Analysis
def nutrition(request):
    form = NutrtionForm
    food = Nutrition.objects.all()

    if request.method == 'POST':
        food = request.POST.get('food')

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Give a nutrition analysis of the following:\nPrompt:\n1 kg chicken\n1 liter milk\n\nResult:\n1 kg chicken contains approximately 2390 calories, 270 grams of protein, and 140 grams of fat.\n1 liter milk contains approximately 628 calories, 32 grams of protein, and 33 grams of fat.\n\nPrompt:\n5 eggs\n\nResult:\n5 eggs contains approximately 390 calories, 30 grams of protein, and 25 grams of fat.\n\nPrompt:\n600 gram chickpeas\n\nResult:\n600 grams of chickpeas contains approximately 2184 calories, 114 grams of protein, and 36 grams of fat.\n\n###\n\nPrompt:\n50 oz lentils\n\nResult:\n50 oz of lentils contains approximately 1164 calories, 128 grams of protein, and 5.7 grams of fat.\n\n###\n\nPrompt:\n{food}\n\nResult:\n",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response["choices"][0]["text"]
        list_answer = answer.split("\n")

        context = {'list_answer': list_answer, 'form': form}
        return render(request, 'base/nutrition.html', context)

    context = {'form': form}
    return render(request, 'base/nutrition.html', context)
