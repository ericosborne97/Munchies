# 🍽️ Munchies

> **Fast food is expensive — cooking at home doesn’t have to be.**  
> **Munchies** generates a weekly meal plan **and** a consolidated grocery list, then emails everything straight to you.

---

## ✨ Features
- **Automated meal plans** – one breakfast, lunch, and dinner for every day of the week  
- **Smart grocery list** – buy exactly what each recipe needs, nothing more  
- **Custom recipes** – drop simple **`.json`** files into the `recipes/` folder, no code changes required  
- **Set-and-forget scheduling** – hook it up to Windows Task Scheduler (or cron) and get your email every week  

---

## 🚀 Quick-Start

1. **Create a Google “App Password”** (needed for the script to send email)  
   [Video walkthrough](https://www.youtube.com/watch?v=wniM7sU0bmU)
2. **Open `main.py`** and fill in the first few lines with  
   - your email address  
   - the generated app password  
   > ⚠️ **Never commit this file with real credentials!**  
   > Anyone who sees them can send mail from your account.
3. **Schedule a weekly run** via Windows Task Scheduler  
   [5-minute setup guide](https://www.youtube.com/watch?v=ic4lUiDTbVI)

That’s it — next week your inbox will have **seven recipes + one grocery list** ready to go. 🎉

---

## 🥑 Managing Recipes

- **Keep at least *seven* recipes** for each mealtime (breakfast, lunch, dinner).  
  Fewer than that and the script can’t build a full week.
- Don’t like one of the defaults?  
  Delete or edit its file in `recipes/`, but make sure you stay above the 7-per-meal minimum.
- **Add your own** by dropping a new **`.json`** file that follows this structure:

```jsonc
{
  "name": "Ham Sandwich",
  "ingredients": ["bread", "mayo", "mustard", "ham", "lettuce", "provolone", "tomato"],
  "recipe": "Assemble ingredients between slices of bread.",
  "breakfast": false,
  "lunch": true,
  "dinner": false,
  "days": 2,                 // how many days this yields servings for
  "tasks": "Make a sandwich" // optional prep note
}
