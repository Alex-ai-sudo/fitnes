import random
import requests

motivation = [
    "Каждый чемпион был когда-то новичком. Начни сегодня!",
    "Тело достигает того, во что верит разум.",
    "Не сдавайся! 1% лучше, чем вчера — это уже победа.",
    "Боль сегодня — сила завтра.",
    "Ты сильнее, чем думаешь.",
    "Маленькие шаги каждый день приводят к большим результатам.",
]


def random_motiv():
    try:
        resp = requests.get("https://zenquotes.io/api/random")
        if resp.status_code == 200:
            data = resp.json()[0]
            return data["q"] + " — " + data["a"]
    except:
        pass
    return random.choice(motivation)


def first_num(text):
    num = ''
    for char in text:
        if char.isdigit():
            num += char
        elif num:
            break
    return int(num) if num else None


def calc_bmi(weight, height):
    if not weight or not height:
        return 0
    return round(weight / ((height / 100) ** 2), 1)


def calc_bmr(weight, height, age, gender):
    if gender == "male":
        return round(88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age))
    else:
        return round(447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age))


def calc_tde(bmr, activity_level):
    multipliers = {
        "very_light": 1.2,
        "light": 1.375,
        "medium": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    return round(bmr * multipliers.get(activity_level, 1.55))