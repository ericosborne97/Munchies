#this program can be scheduled to run with windows task manager a

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
import html

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

#Now make a grocery list
grocery_list_with_duplicates = []
for recipe in breakfast_list:
    for item in recipe["ingredients"]:
        grocery_list_with_duplicates.append(item)
for recipe in lunch_list:
    for item in recipe["ingredients"]:
        grocery_list_with_duplicates.append(item)
for recipe in dinner_list:
    for item in recipe["ingredients"]:
        grocery_list_with_duplicates.append(item)
grocery_list_without_duplicates = list(set(grocery_list_with_duplicates))


#email
body_of_email = f"""
🍽️  **Weekly Munchies for {datetime.now().strftime('%B %d, %Y')}**

You'll be having the following:

🗓️ **Monday**
    🌅 Breakfast: {breakfast_list[0]['name']} 🍳
    🥪 Lunch: {lunch_list[0]['name']} 🥗
    🍽️ Dinner: {dinner_list[0]['name']} 🍝

🗓️ **Tuesday**
    🌅 Breakfast: {breakfast_list[1]['name']} 🍳
    🥪 Lunch: {lunch_list[1]['name']} 🥗
    🍽️ Dinner: {dinner_list[1]['name']} 🍝

🗓️ **Wednesday**
    🌅 Breakfast: {breakfast_list[2]['name']} 🍳
    🥪 Lunch: {lunch_list[2]['name']} 🥗
    🍽️ Dinner: {dinner_list[2]['name']} 🍝

🗓️ **Thursday**
    🌅 Breakfast: {breakfast_list[3]['name']} 🍳
    🥪 Lunch: {lunch_list[3]['name']} 🥗
    🍽️ Dinner: {dinner_list[3]['name']} 🍝

🗓️ **Friday**
    🌅 Breakfast: {breakfast_list[4]['name']} 🍳
    🥪 Lunch: {lunch_list[4]['name']} 🥗
    🍽️ Dinner: {dinner_list[4]['name']} 🍝

🗓️ **Saturday**
    🌅 Breakfast: {breakfast_list[5]['name']} 🍳
    🥪 Lunch: {lunch_list[5]['name']} 🥗
    🍽️ Dinner: {dinner_list[5]['name']} 🍝

🗓️ **Sunday**
    🌅 Breakfast: {breakfast_list[6]['name']} 🍳
    🥪 Lunch: {lunch_list[6]['name']} 🥗
    🍽️ Dinner: {dinner_list[6]['name']} 🍝


🛒 **Grocery List**
{', '.join(grocery_list_without_duplicates)}

🛠️ **Task Timeline**
Monday:
    ✅ {breakfast_list[0]['tasks']}
    ✅ {lunch_list[0]['tasks']}
    ✅ {dinner_list[0]['tasks']}
    
Tuesday:
    ✅ {breakfast_list[1]['tasks']}
    ✅ {lunch_list[1]['tasks']}
    ✅ {dinner_list[1]['tasks']}
    
Wednesday:
    ✅ {breakfast_list[2]['tasks']}
    ✅ {lunch_list[2]['tasks']}
    ✅ {dinner_list[2]['tasks']}
    
Thursday:
    ✅ {breakfast_list[3]['tasks']}
    ✅ {lunch_list[3]['tasks']}
    ✅ {dinner_list[3]['tasks']}
    
Friday:
    ✅ {breakfast_list[4]['tasks']}
    ✅ {lunch_list[4]['tasks']}
    ✅ {dinner_list[4]['tasks']}
    
Saturday:
    ✅ {breakfast_list[5]['tasks']}
    ✅ {lunch_list[5]['tasks']}
    ✅ {dinner_list[5]['tasks']}
    
Sunday:
    ✅ {breakfast_list[6]['tasks']}
    ✅ {lunch_list[6]['tasks']}
    ✅ {dinner_list[6]['tasks']}


📜 **Recipes**
Monday:
    🍳 Breakfast: {breakfast_list[0]['recipe']}
    🥪 Lunch: {lunch_list[0]['recipe']}
    🍽️ Dinner: {dinner_list[0]['recipe']}
    
Tuesday:
    🍳 Breakfast: {breakfast_list[1]['recipe']}
    🥪 Lunch: {lunch_list[1]['recipe']}
    🍽️ Dinner: {dinner_list[1]['recipe']}
    
Wednesday:
    🍳 Breakfast: {breakfast_list[2]['recipe']}
    🥪 Lunch: {lunch_list[2]['recipe']}
    🍽️ Dinner: {dinner_list[2]['recipe']}
    
Thursday:
    🍳 Breakfast: {breakfast_list[3]['recipe']}
    🥪 Lunch: {lunch_list[3]['recipe']}
    🍽️ Dinner: {dinner_list[3]['recipe']}
    
Friday:
    🍳 Breakfast: {breakfast_list[4]['recipe']}
    🥪 Lunch: {lunch_list[4]['recipe']}
    🍽️ Dinner: {dinner_list[4]['recipe']}
    
Saturday:
    🍳 Breakfast: {breakfast_list[5]['recipe']}
    🥪 Lunch: {lunch_list[5]['recipe']}
    🍽️ Dinner: {dinner_list[5]['recipe']}
    
Sunday:
    🍳 Breakfast: {breakfast_list[6]['recipe']}
    🥪 Lunch: {lunch_list[6]['recipe']}
    🍽️ Dinner: {dinner_list[6]['recipe']}
    
"""


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

# build the checkbox list
checkbox_html = "\n".join(
    f'''<li style="margin:6px 0;">
            <label style="display:flex;align-items:center;font-size:20px;line-height:1.3;">
                <input type="checkbox"
                       style="
                           /* make the box ~2× bigger */
                           transform:scale(2);
                           -webkit-transform:scale(2);  /* iOS/Apple Mail */
                           /* give Outlook a fallback */
                           width:20px;height:20px;
                           margin-right:10px;
                       ">
                {html.escape(item.title())}
            </label>
        </li>'''
    for item in grocery_list_without_duplicates
)

checkbox_body = f"""
<h2>🛒 Weekly Grocery Checklist</h2>
<p>Tick items as you load them into your cart:</p>
<ul style="list-style:none; padding-left:0;">
    {checkbox_html}
</ul>
"""

html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: Arial, Helvetica, sans-serif;
      font-size: 18px;
      line-height: 1.5;
      color: #222;
    }}
    h2 {{
      font-size: 26px;
      margin: 0 0 0.6em;
    }}
    h3 {{
      font-size: 22px;
      margin: 1.2em 0 0.4em;     /* ⬅️ extra space above each day */
    }}
    .meal {{
      margin: 0 0 0.8em 1.2em;    /* ⬅️ bottom-margin = extra line break */
    }}

    /* ---- checkbox look ---- */
    input[type=checkbox] {{
      transform: scale(1.6);
      -webkit-transform: scale(1.6);
      width: 18px; height: 18px;
      margin-right: 10px;
      vertical-align: middle;
    }}
    ul.grocery {{
      list-style: none;
      padding-left: 0;
    }}
    ul.grocery li {{ margin: 6px 0; }}
  </style>
</head>
<body>

<h2>🍽️ Weekly Munchies for {datetime.now().strftime('%B %d, %Y')}</h2>

<!-- ========= MEAL PLAN ========= -->
<h3>🗓️ Monday</h3>
<p class="meal">🌅 Breakfast: {breakfast_list[0]['name']} 🍳</p>
<p class="meal">🥪 Lunch: {lunch_list[0]['name']} 🥗</p>
<p class="meal">🍽️ Dinner: {dinner_list[0]['name']} 🍝</p>

<h3>🗓️ Tuesday</h3>
<p class="meal">🌅 Breakfast: {breakfast_list[1]['name']} 🍳</p>
<p class="meal">🥪 Lunch: {lunch_list[1]['name']} 🥗</p>
<p class="meal">🍽️ Dinner: {dinner_list[1]['name']} 🍝</p>

<h3>🗓️ Wednesday</h3>
<p class="meal">🌅 Breakfast: {breakfast_list[2]['name']} 🍳</p>
<p class="meal">🥪 Lunch: {lunch_list[2]['name']} 🥗</p>
<p class="meal">🍽️ Dinner: {dinner_list[2]['name']} 🍝</p>

<h3>🗓️ Thursday</h3>
<p class="meal">🌅 Breakfast: {breakfast_list[3]['name']} 🍳</p>
<p class="meal">🥪 Lunch: {lunch_list[3]['name']} 🥗</p>
<p class="meal">🍽️ Dinner: {dinner_list[3]['name']} 🍝</p>

<h3>🗓️ Friday</h3>
<p class="meal">🌅 Breakfast: {breakfast_list[4]['name']} 🍳</p>
<p class="meal">🥪 Lunch: {lunch_list[4]['name']} 🥗</p>
<p class="meal">🍽️ Dinner: {dinner_list[4]['name']} 🍝</p>

<h3>🗓️ Saturday</h3>
<p class="meal">🌅 Breakfast: {breakfast_list[5]['name']} 🍳</p>
<p class="meal">🥪 Lunch: {lunch_list[5]['name']} 🥗</p>
<p class="meal">🍽️ Dinner: {dinner_list[5]['name']} 🍝</p>

<h3>🗓️ Sunday</h3>
<p class="meal">🌅 Breakfast: {breakfast_list[6]['name']} 🍳</p>
<p class="meal">🥪 Lunch: {lunch_list[6]['name']} 🥗</p>
<p class="meal">🍽️ Dinner: {dinner_list[6]['name']} 🍝</p>

<!-- ========= TASK TIMELINE ========= -->
<h2>🛠️ Task Timeline</h2>

<h3>Monday</h3>
<p class="meal">✅ {breakfast_list[0]['tasks']}</p>
<p class="meal">✅ {lunch_list[0]['tasks']}</p>
<p class="meal">✅ {dinner_list[0]['tasks']}</p>

<h3>Tuesday</h3>
<p class="meal">✅ {breakfast_list[1]['tasks']}</p>
<p class="meal">✅ {lunch_list[1]['tasks']}</p>
<p class="meal">✅ {dinner_list[1]['tasks']}</p>

<h3>Wednesday</h3>
<p class="meal">✅ {breakfast_list[2]['tasks']}</p>
<p class="meal">✅ {lunch_list[2]['tasks']}</p>
<p class="meal">✅ {dinner_list[2]['tasks']}</p>

<h3>Thursday</h3>
<p class="meal">✅ {breakfast_list[3]['tasks']}</p>
<p class="meal">✅ {lunch_list[3]['tasks']}</p>
<p class="meal">✅ {dinner_list[3]['tasks']}</p>

<h3>Friday</h3>
<p class="meal">✅ {breakfast_list[4]['tasks']}</p>
<p class="meal">✅ {lunch_list[4]['tasks']}</p>
<p class="meal">✅ {dinner_list[4]['tasks']}</p>

<h3>Saturday</h3>
<p class="meal">✅ {breakfast_list[5]['tasks']}</p>
<p class="meal">✅ {lunch_list[5]['tasks']}</p>
<p class="meal">✅ {dinner_list[5]['tasks']}</p>

<h3>Sunday</h3>
<p class="meal">✅ {breakfast_list[6]['tasks']}</p>
<p class="meal">✅ {lunch_list[6]['tasks']}</p>
<p class="meal">✅ {dinner_list[6]['tasks']}</p>


<!-- ========= RECIPES ========= -->
<h2>📜 Recipes</h2>

<h3>Monday</h3>
<p class="meal">🍳 Breakfast: {breakfast_list[0]['recipe']}</p>
<p class="meal">🥪 Lunch: {lunch_list[0]['recipe']}</p>
<p class="meal">🍽️ Dinner: {dinner_list[0]['recipe']}</p>

<h3>Tuesday</h3>
<p class="meal">🍳 Breakfast: {breakfast_list[1]['recipe']}</p>
<p class="meal">🥪 Lunch: {lunch_list[1]['recipe']}</p>
<p class="meal">🍽️ Dinner: {dinner_list[1]['recipe']}</p>

<h3>Wednesday</h3>
<p class="meal">🍳 Breakfast: {breakfast_list[2]['recipe']}</p>
<p class="meal">🥪 Lunch: {lunch_list[2]['recipe']}</p>
<p class="meal">🍽️ Dinner: {dinner_list[2]['recipe']}</p>

<h3>Thursday</h3>
<p class="meal">🍳 Breakfast: {breakfast_list[3]['recipe']}</p>
<p class="meal">🥪 Lunch: {lunch_list[3]['recipe']}</p>
<p class="meal">🍽️ Dinner: {dinner_list[3]['recipe']}</p>

<h3>Friday</h3>
<p class="meal">🍳 Breakfast: {breakfast_list[4]['recipe']}</p>
<p class="meal">🥪 Lunch: {lunch_list[4]['recipe']}</p>
<p class="meal">🍽️ Dinner: {dinner_list[4]['recipe']}</p>

<h3>Saturday</h3>
<p class="meal">🍳 Breakfast: {breakfast_list[5]['recipe']}</p>
<p class="meal">🥪 Lunch: {lunch_list[5]['recipe']}</p>
<p class="meal">🍽️ Dinner: {dinner_list[5]['recipe']}</p>

<h3>Sunday</h3>
<p class="meal">🍳 Breakfast: {breakfast_list[6]['recipe']}</p>
<p class="meal">🥪 Lunch: {lunch_list[6]['recipe']}</p>
<p class="meal">🍽️ Dinner: {dinner_list[6]['recipe']}</p>

</body>
</html>
"""




# Email content
subject = "Weekly Grocery List"

# Create message
msg = MIMEMultipart()
msg["From"] = email_sender
msg["To"] = email_receiver
msg["Subject"] = subject
msg.attach(MIMEText(html_body, "html"))
msg.attach(MIMEText(checkbox_body, "html"))        # the new HTML version

# Send the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_sender, email_password)
        server.send_message(msg)
        print("Email sent successfully!")
except Exception as e:
    print("Error sending email:", e)
