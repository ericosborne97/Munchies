#this program can be scheduled to run with the command

"""
EXAMPLE
<SUBJECT:WEEKLY GROCERY LIST>
<BODY>
Here is your weekly munchies for 6/5/2025.
You'll be having the following
Monday,
    Morning: Steak and Egg
    Lunch: Ham Sandwich
    Dinner: Lasagna
Tuesday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Wednesday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Thursday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Friday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Saturday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Sunday,
    Morning: Steak and Egg
    Lunch: Ham Sandwich
    Diner: Lasagna

You'll be needing the following
Ham
Lettuce
Tomato
Rice
Chicken
Turkey

Here's a simple timeline of events
Sunday:
    Cook 2 steaks
    Boil 2 eggs
    Make lasagna
Monday:
    do stuff..

Here are the recipes :)
Monday.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import glob
import random

body_of_email = ""
#generate a list of all breakfast, lunch, and dinner recipes
all_recipes = glob.glob("./Recipes/*.json")
all_breakfast_recipes = []
all_lunch_recipes = []
all_dinner_recipes = []
for recipe_location in all_recipes:
    with open(recipe_location, mode="r", encoding="utf-8") as read_file:
        recipe = json.load(read_file)
        if recipe["breakfast"]: all_breakfast_recipes.append(recipe_location)
        if recipe["lunch"]: all_lunch_recipes.append(recipe_location)
        if recipe["dinner"] : all_dinner_recipes.append(recipe_location)

#now select 7 at random from the list
seven_breakfast_recipes = random.sample(all_breakfast_recipes, k=7)
seven_lunch_recipes = random.sample(all_lunch_recipes, k=7)
seven_diner_recipes = random.sample(all_dinner_recipes, k=7)

#but wait some recipes serve enough for multiple days lets fix that by replacing the recipes after the ones
#that serve multiple meals with that meal
def replace_duplicate_meals(seven_recipes):
    x = 0
    while x<7:
        with open(seven_recipes[x], mode="r", encoding="utf-8") as this_file:
            current_recipe = json.load(this_file)
            if current_recipe["days"]>1:
                #this means we need to start replacing the next days recipe with our multi day recipe
                for y in range(current_recipe["days"]):
                    #replace that days recipe with ours
                    if x+y>=7:
                        break
                    seven_recipes[x+y] = seven_recipes[x]
                x=x+current_recipe["days"]
            else:
                x=x+1

replace_duplicate_meals(seven_breakfast_recipes)
replace_duplicate_meals(seven_lunch_recipes)
replace_duplicate_meals(seven_diner_recipes)

#print(seven_breakfast_recipes)
#print(seven_lunch_recipes)
#print(seven_diner_recipes)

#Now convert each of the json files into a python dicts
def convert_and_add_to_list(recipes_list, seven_recipes):
    for eachfile in seven_recipes:
        with open(eachfile, mode="r", encoding="utf-8") as this_file:
            some_recipe_json = json.load(this_file)
            recipes_list.append(some_recipe_json)  # No json.dumps


breakfast_list = []
lunch_list = []
dinner_list = []
convert_and_add_to_list(breakfast_list,seven_breakfast_recipes)
convert_and_add_to_list(lunch_list,seven_lunch_recipes)
convert_and_add_to_list(dinner_list,seven_diner_recipes)

print(f"todays breakfast {breakfast_list[0]['name']}")
body_of_email = f'''
Here is your weekly munchies for 6/5/2025.
You'll be having the following
Monday,
    Morning: {breakfast_list[0]['name']}
    Lunch: {lunch_list[0]['name']}
    Dinner: {dinner_list[0]['name']}
Tuesday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Wednesday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Thursday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Friday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Saturday,
    Morning: Sausage Biscuit
    Lunch: Chicken Salad
    Dinner: Chicken and Rice
Sunday,
    Morning: Steak and Egg
    Lunch: Ham Sandwich
    Diner: Lasagna

You'll be needing the following
Ham
Lettuce
Tomato
Rice
Chicken
Turkey

Here's a simple timeline of events
Sunday:
    Cook 2 steaks
    Boil 2 eggs
    Make lasagna
Monday:
    do stuff..

Here are the recipes :)
Monday.'''









'''document of the form
sender_email
sender_app_password
receiver_email'''
File_object = open(r"C:/Users/erico/Documents/sensitive.txt","r")
email_sender =   File_object.readline().rstrip()
email_password = File_object.readline().rstrip()
email_receiver = File_object.readline().rstrip()

print(email_sender)
print(email_receiver)
print(email_password)


# Email content
subject = "Weekly Grocery List"
body = f"Here is your weekly munches for {datetime.now().strftime('%Y-%m-%d')}.\n\n[Insert your info here]"

# Create message
msg = MIMEMultipart()
msg["From"] = email_sender
msg["To"] = email_receiver
msg["Subject"] = subject
msg.attach(MIMEText(body_of_email, "plain"))

# Send the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_sender, email_password)
        server.send_message(msg)
        print("Email sent successfully!")
except Exception as e:
    print("Error sending email:", e)
