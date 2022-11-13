# importing dependencies
from django.shortcuts import render, redirect
from .models import Nutrition, User
from .forms import ExtractForm, NutrtionForm, UploadForm, MyUserCreationForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import cv2
import pytesseract
import os
import glob
 
import openai

import requests

from base.recipe_option import dietlabels, healthlabels, dishtype, cuisinetype


# OPENAI API_KEY
openai.api_key = "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"

# Edamam API
api_id = "2e2a95e8"
api_key = "a7103cf7671e8fe63ec327c9d2b8fe15"


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
        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credentials Incorrect!')

    context = {'page':page}
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

    context = {'form':form}   
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

            list_of_files = glob.glob('/Users/arshad/Desktop/Healthy-Eats/static/images/*') # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime) # selecting the latest file
            print(latest_file)

            # Reading and processing image using openCV
            img = cv2.imread(latest_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Extracting the text from the photo
            extracted_data = pytesseract.image_to_string(img)

            # Processing the extracted data to search for ingredients
            response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"A list summarizing the ingredients in the following text and write 5 lines about each ingredient:\n\nExample:\nPrompt:\nTotal Fat 4g ae ~\nSaturated Fat 159\nTrans Fat 0g\nCholesterol 5mg 2%\nSodium 115mg 5%\nTotal Carbohydrate 189 Th\nDietary Fiber 0g (0%\nTotal Sugars 9g\nIncludes 9g Added Sugars 18%\nProtein 19\nVitamin D Omeg 0%\nCalcium 3mg 0%\n{{ron 1mg 6%\nPotassium 3mg a 0%\n“The % Daity Value tells you how much ‘a nutrient ina\nServing of food contributes to a daly det 2,000 calories a\n‘Gay is used for general nutrition advice.\n\nINGREDIENTS: ENRICHED FLOUR (WHEAT FLOUR, NIACIN,\nREDUCED IRON, THIAMIN MONONITRATE, RIBOFLAVIN AND FOLIC\nACID), CANE SUGAR, NON-HYDROGENATED PALM OIL, EGGS,\nWATER, BAKING SODA, MEYER LEMON OIL, SALT, NONEAT MILK,\nBUTTER FLAVOR, NATURAL CITRUS FLAVOR, AND LEMON ZEST\nDONTAINS WHEAT, EGG, MILK.\n\nMANUFACTURED ON SHARED EQUIPMENT THAT PROCESSES\nPEANUTS, SOY, AND TREE HUTS.\n\nResult:\n-enriched flour (Healthy) 🍚\n Enriched flour is a type of flour that has been enriched with vitamins and minerals. It is often used in breads, pastries, and other baked goods. \n-cane sugar (Unhealthy) 🍭\n Cane sugar is a type of sugar that is derived from sugar cane. It is often used in baking and has a sweeter taste than other types of sugar.\n-non-hydrogenated palm oil (Healthy) 🌴\nNon-hydrogenated palm oil is a type of palm oil that has not been treated with hydrogen gas. It is often used in cooking and baking.\n-eggs (Healthy) 🥚\nEggs are a nutritious food that can be used in a variety of recipes. They are a good source of protein and contain essential nutrients.\n-water (Healthy) 💧\nWater is a essential for life and is necessary for the body to function properly. It is often recommended to drink eight glasses of water per day.\n-baking soda (Healthy) 🧂\nBaking soda is a type of baking powder that is used to leaven baked goods. It is also a common ingredient in many household cleaning products.\n-meyer lemon oil (Healthy) 🍋\nMeyer lemon oil is a type of essential oil that is derived from Meyer lemons. It has a fresh, citrusy scent and is often used in aromatherapy.\n-salt (Healthy) 🧂\nSalt is a mineral that is used to add flavor to food. It is also used to preserve food and prevent spoilage.\nNonfat milk (Healthy) 🥛\n Nonfat milk is a type of milk that has had the majority of its fat content removed. It is often used in baking and cooking.\n-butter flavor (Healthy) 🧈\nButter flavor is a type of flavoring that is used to mimic the taste of butter. It is often used in baking and cooking.\n-natural citrus flavor (Healthy) 🍊\nNatural citrus flavor is a type of flavoring that is derived from citrus fruits. It is often used in baking and cooking.\n-lemon zest (Healthy) 🍋\nLemon zest is the outermost layer of a lemon peel. It is often used to add flavor to food.\n\n\n##\n\nPrompt:\n{extracted_data}\nResult:\n\n",
            temperature=0.3,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            # Processing the final answer
            final_answer = response["choices"][0]["text"].lstrip("'") # converting json into string
            array_answer = list(final_answer.split("\n")) # string to list
            modified_array_answer = [x.lstrip('-') for x in array_answer] 
            # print(array_answer)
            # print(modified_array_answer)
            # print(modified_array_answer)

            context = {'form':form, 'array_answer':array_answer, 'modified_array_answer':modified_array_answer}        
            return render(request, 'base/result.html', context)

    context = {'form':form}        
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
        param = ''.join(ingredients+dishType+dietLabels+
                    healthLabels+cuisineType)
            
        url = f"https://api.edamam.com/api/recipes/v2?type=public&app_id={api_id}&app_key={api_key}&q={param}"
            
        response = requests.get(url)  # returns response e.g. 200
        data = response.json()  # returns actual API content
        
        hits = data["hits"]

        context = {'hits':hits}
        return render(request, 'base/recipe_result.html', context)

    context = {'dietlabels':dietlabels, 'healthlabels':healthlabels,
               'dishtype':dishtype, 'cuisinetype':cuisinetype}
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

        context = {'list_answer':list_answer, 'form':form}
        return render(request, 'base/nutrition.html', context)


    context = {'form':form}
    return render(request, 'base/nutrition.html', context)




        
