# import cv2
# import pytesseract
 
# # Read image from which text needs to be extracted
# img = cv2.imread("/Users/arshad/Desktop/Projects/concode/training_images/kurkure.png")
 
# # Preprocessing the image starts
 
# # Convert the image  as pytesseract accepts RGB only and cv2 is in BGR 
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# extracted_data = pytesseract.image_to_string(img)
# print(extracted_data)

# import openai
# openai.api_key = "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"
# food = input("WRITE")
# response = openai.Completion.create(
#         model="text-davinci-002",
#         prompt=f"Give a nutrition analysis of the following:\nExample:\nPrompt:\n1 cup rice,\n10 oz chickpeas\nResult:\n1 cup of rice contains 702 kcal\n10 oz of chickpeas contains 1071.6 kcal\n\n###\n\nPrompt:\n{food}\nResult:\n",
#         temperature=0.7,
#         max_tokens=256,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#         )
# answer = response["choices"][0]["text"]
# list_answer = answer.split("\n")
# print(list_answer)
# import py_edamam

# app_id = "2e2a95e8"

# app_key = "a7103cf7671e8fe63ec327c9d2b8fe15"

# e = py_edamam.Edamam(recipes_appid=app_id,
#            recipes_appkey=app_key)
           
# # print(e.search_nutrient("1 large apple"))
# # print(e.search_recipe("onion and chicken"))
# # print(e.search_food("coke"))
# print(recipe.url)


# import requests

# api_id = "2e2a95e8"
# api_key = "a7103cf7671e8fe63ec327c9d2b8fe15"

# ingredients = input('Which ingredient do you have? ')
# dishType = input("dish type??")
# dietLabels = input("dish label??")
# healthLabels = input("health")
# cuisineType = input("cuisine Type??")

# url = f"https://api.edamam.com/api/recipes/v2?type=public&app_id={api_id}&app_key={api_key}&q=&ingredients={ingredients}&dishType={dishType}&dietLabels={dietLabels}&healthLabels={healthLabels}&cuisineType={cuisineType}"


# response = requests.get(url)  # returns response e.g. 200
# data = response.json()  # returns actual API content
# print(data)
# hits = data["hits"]
# # print(hits[0])
# a = []
# for i in hits:
#     print(i["recipe"]["label"])
#     print(i["recipe"]["url"])
#     print(i["recipe"]["image"])
#     print('\n')






# TOMTOM = "7pCqOfkP8LLvHXHGANRdT4gKLzeemhA5"

import openai
openai.api_key = "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"


response = openai.Image.create_variation(
  image=open("Arshad.png", "rb"),
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)