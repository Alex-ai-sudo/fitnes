from .exercises import person_wrkout, bttns, EX
from .utils import first_num, calc_bmi, calc_bmr, calc_tde, random_motiv
import random
from datetime import datetime

# ID картинок
id_igm = ["1656841/f41afaa7627a28ab7df9", "1656841/7bae17369106129be9da"]


def dialog(req, res, storage):
    user_id = req['session']['user_id']
    utterance = req['request']['original_utterance'].lower().strip()

    if req['session'].get('new'):
        storage[user_id] = {
            "step": "start",
            "height": None,
            "weight": None,
            "age": None,
            "gender": None,
            "level": None,
            "goal": None,
            "target_kg": None,
            "activity": "medium",
            "last_workout": None,
            "streak": 0,
            "workouts_done": 0,
            "weight_history": []
        }
        res['response']['text'] = (
            'Привет, чемпион 👊\n'
            'Я Алиса Фитнес-ИИ яндекс калаборэйшн.\n'
            'Давай создадим тебе идеальную программу для тренировок \n'
            'Скажи свой рост в сантиметрах (например: 175)'
        )
        res['response']['buttons'] = []
        return

    profile = storage[user_id]
    step = profile.get("step")

    if step == "change_height":
        h = first_num(utterance)
        if h and 100 <= h <= 250:
            profile["height"] = h
            profile["step"] = "change_ves"
            res['response']['text'] = f'Рост обновлён: {h} см\nТеперь новый вес в килограммах?'
        else:
            res['response']['text'] = 'Пожалуйста, напиши рост цифрами (100-250 см)'
        storage[user_id] = profile
        return


    elif step == "change_ves":
        w = first_num(utterance)

        if w and 40 <= w <= 200:
            profile["weight"] = w
            profile["step"] = "main_menu"
            profile["bmi"] = calc_bmi(profile["weight"], profile["height"])
            bmr = calc_bmr(profile["weight"], profile["height"], profile["age"], profile["gender"])
            profile["tdee"] = calc_tde(bmr, profile["activity"])
            # Сохранение истории веса
            today = datetime.now().strftime("%d.%m.%Y")

            profile["weight_history"].append({"date": today, "weight": w})

            if len(profile["weight_history"]) > 10:
                profile["weight_history"] = profile["weight_history"][-10:]

            congrats = ""

            if profile.get("target_kg"):
                if profile["goal"] == "Похудение" and w <= profile["target_kg"]:
                    congrats = f"\n🎉🎉 Поздравляем! Ты достиг цели по похудению ({profile['target_kg']} кг)!"
                elif profile["goal"] == "Набор массы" and w >= profile["target_kg"]:
                    congrats = f"\n🎉🎉 Поздравляем! Ты достиг цели по набору массы ({profile['target_kg']} кг)!"

            res['response']['text'] = (
                f'Данные обновлены ✅\n'
                f'Рост: {profile["height"]} см | Вес: {profile["weight"]} кг{congrats}\n'
                f'Что делаем дальше?'
            )

            res['response']['buttons'] = [
                {"title": "Новая тренировка", "hide": True},
                {"title": "Мой прогресс", "hide": True},
                {"title": "Питание сегодня", "hide": True},
                {"title": "Рандомная цитата", "hide": True},
                {"title": "Изменить данные", "hide": True}
            ]

        else:
            res['response']['text'] = 'Напиши вес цифрами (40-200 кг)'
        storage[user_id] = profile
        return

    if step == "start":
        h = first_num(utterance)
        if h and 100 <= h <= 250:
            profile["height"] = h
            profile["step"] = "ves"
            res['response']['text'] = f'Отлично! Рост {h} см сохранён.\nТеперь твой вес в килограммах?'
        else:
            res['response']['text'] = 'Пожалуйста, напиши рост цифрами (100-250 см)'
        res['response']['buttons'] = []
        storage[user_id] = profile
        return

    elif step == "ves":
        w = first_num(utterance)
        if w and 40 <= w <= 200:
            profile["weight"] = w
            profile["step"] = "await_age"
            res['response']['text'] = f'Вес {w} кг запомнил ✅\nСколько тебе лет?'
        else:
            res['response']['text'] = 'Напиши вес цифрами (40-200 кг)'
        res['response']['buttons'] = []
        storage[user_id] = profile
        return

    elif step == "await_age":
        age = first_num(utterance)
        if age and 14 <= age <= 80:
            profile["age"] = age
            profile["step"] = "gen"
            res['response']['text'] = 'Отлично! Теперь скажи свой пол:\nМужской или Женский...'
            res['response']['buttons'] = [
                {"title": "Мужской", "hide": True},
                {"title": "Женский", "hide": True}
            ]
        else:
            res['response']['text'] = 'Возраст от 14 до 80 лет'
        storage[user_id] = profile
        return

    elif step == "gen":
        if "муж" in utterance or "male" in utterance:
            profile["gender"] = "male"
        else:
            profile["gender"] = "female"
        profile["step"] = "await_level"
        res['response']['text'] = 'Какой у тебя уровень подготовки?\nВыбери кнопку:'
        res['response']['buttons'] = [
            {"title": "Новичок", "hide": True},
            {"title": "Средний", "hide": True},
            {"title": "Продвинутый", "hide": True}
        ]
        storage[user_id] = profile
        return

    elif step == "await_level":
        if "новичок" in utterance:
            profile["level"] = "Новичок"
        elif "средний" in utterance:
            profile["level"] = "Средний"
        else:
            profile["level"] = "Продвинутый"
        profile["step"] = "await_goal"
        res['response']['text'] = 'Какая твоя главная цель?'
        res['response']['buttons'] = [
            {"title": "Похудение", "hide": True},
            {"title": "Набор массы", "hide": True},
            {"title": "Сила и выносливость", "hide": True},
            {"title": "Поддержка формы", "hide": True}
        ]
        storage[user_id] = profile
        return

    # цель пользователя
    elif step == "await_goal":
        if "похуд" in utterance:
            profile["goal"] = "Похудение"
        elif "набор" in utterance or "масса" in utterance:
            profile["goal"] = "Набор массы"
        elif "сила" in utterance:
            profile["goal"] = "Сила"
        else:
            profile["goal"] = "Поддержка"

        if profile["goal"] in ["Сила", "Поддержка"]:
            profile["target_kg"] = None
            profile["step"] = "main_menu"
            res['response']['text'] = (
                f'Отлично! Цель — {profile["goal"]}\n'
                f'Профиль готов! 🎉\nЧто делаем дальше?'
            )
            res['response']['buttons'] = [
                {"title": "Новая тренировка", "hide": True},
                {"title": "Мой прогресс", "hide": True},
                {"title": "Питание сегодня", "hide": True},
                {"title": "Рандомная цитата", "hide": True},
                {"title": "Изменить данные", "hide": True}
            ]
        else:
            profile["step"] = "await_target_kg"
            res['response']['text'] = f'Отлично! Цель — {profile["goal"]}\nСколько килограмм ты хочешь весить в итоге?'
            res['response']['buttons'] = []

        storage[user_id] = profile
        return
    elif step == "await_target_kg":
        target = first_num(utterance)
        if target and 30 <= target <= 200:
            if profile["goal"] == "Похудение" and target >= profile["weight"]:
                res['response']['text'] = f'При похудении цель должна быть меньше текущего веса ({profile["weight"]} кг). Введи заново:'
                storage[user_id] = profile
                return
            elif profile["goal"] == "Набор массы" and target <= profile["weight"]:
                res['response']['text'] = f'При наборе массы цель должна быть больше текущего веса ({profile["weight"]} кг). Введи заново:'
                storage[user_id] = profile
                return

            profile["target_kg"] = target
            profile["bmi"] = calc_bmi(profile["weight"], profile["height"])
            bmr = calc_bmr(profile["weight"], profile["height"], profile["age"], profile["gender"])
            profile["tdee"] = calc_tde(bmr, profile["activity"])
            profile["step"] = "main_menu"

            res['response']['text'] = (
                f'🎉🎉🎉 !Профиль готов! 🎉🎉🎉\n'
                f'Рост: {profile["height"]} см -|- Вес: {profile["weight"]} кг -|- Цель: {target} кг\n'
                f'BMI: {profile["bmi"]} -|- BMR: {bmr} ккал -|- TDE: {profile["tdee"]} ккал\n\n'
                f'Что делаем дальше?'
            )
            res['response']['buttons'] = [
                {"title": "Новая тренировка", "hide": True},
                {"title": "Мой прогресс", "hide": True},
                {"title": "Питание сегодня", "hide": True},
                {"title": "Рандомная цитата", "hide": True},
                {"title": "Изменить данные", "hide": True}
            ]
        else:
            res['response']['text'] = 'Напиши желаемый вес цифрами (30-200 кг)'
        storage[user_id] = profile
        return

    elif step in ("main_menu", "await_group"):

        if any(word in utterance for word in ["хватит", "выход", "стоп", "пока", "завершить"]):
            res['response']['text'] = 'До встречи, чемпион! 💪 Приходи ещё!'
            res['response']['end_session'] = True
            return

        # Рандомная цитата с картинкой
        if "цитат" in utterance or "мотивац" in utterance or "рандом" in utterance:
            res['response']['text'] = random_motiv()
            res['response']['card'] = {
                "type": "BigImage",
                "image_id": random.choice(id_igm),
                "title": "Мотивация дня",
                "description": f"ты сильнее чем думаешьь 💪"
            }
            res['response']['buttons'] = [
                {"title": "Новая тренировка", "hide": True},
                {"title": "Мой прогресс", "hide": True},
                {"title": "Питание сегодня", "hide": True},
                {"title": "Рандомная цитата", "hide": True}
            ]
            storage[user_id] = profile
            return

        # Выбор группы мышц
        gruppa = None
        for g in EX.keys():
            if g.lower() in utterance:
                gruppa = g
                break

        if gruppa:

            ex_list = EX[gruppa]
            text = f"🔥 Упражнения на {gruppa}:\n\n"
            for ex in ex_list:
                text += f"• {ex['name']} — {ex['sets']}\n  {ex['desc']}\n\n"
            res['response']['text'] = text
            res['response']['buttons'] = bttns() + [
                {"title": "Мой прогресс", "hide": True},
                {"title": "Питание сегодня", "hide": True},
                {"title": "Рандомная цитата", "hide": True},
                {"title": "Изменить данные", "hide": True}
            ]
            storage[user_id] = profile
            return

        # Новая тренировка
        if "тренировк" in utterance or "новая" in utterance:
            workout = person_wrkout(profile)
            profile["last_workout"] = "Сегодня"
            profile["workouts_done"] = profile.get("workouts_done", 0) + 1
            profile["streak"] = profile.get("streak", 0) + 1

            res['response']['text'] = workout
            res['response']['buttons'] = bttns() + [
                {"title": "Мой прогресс", "hide": True},
                {"title": "Питание сегодня", "hide": True},
                {"title": "Рандомная цитата", "hide": True},
                {"title": "Изменить данные", "hide": True}
            ]
            profile["step"] = "await_group"
            storage[user_id] = profile
            return

        # Мой прогресс
        elif "прогресс" in utterance or "мой" in utterance:
            histor = ""
            if profile.get("weight_history"):
                histor = "\n\n📅 История взвешиваний:\n"
                for entry in reversed(profile.get("weight_history", [])[-8:]):
                    histor += f"• {entry['date']}: {entry['weight']} кг\n"
            else:
                histor = "\n\nИстория взвешиваний пока пуста."

            goaal_name = profile.get("goal", "Не указана")
            if goaal_name == "Сила":
                goaal_name = "Сила и выносливость"
            elif goaal_name == "Поддержка":
                goaal_name = "Поддержка формы"

            if profile.get("target_kg"):
                goaal = f"{goaal_name} ({profile['target_kg']} кг)"
            else:
                goaal = goaal_name

            res['response']['text'] = (
                f'📊 Твой прогресс:\n'
                f'Тренировок: {profile.get("workouts_done", 0)}\n'
                f'Стрек: {profile.get("streak", 0)} дней 🔥\n'
                f'Цель: {goaal}\n'
                f'Текущий вес: {profile.get("weight")} кг'
                f'{histor}'
            )
            res['response']['buttons'] = [
                {"title": "Новая тренировка", "hide": True},
                {"title": "Питание сегодня", "hide": True},
                {"title": "Рандомная цитата", "hide": True},
                {"title": "Изменить данные", "hide": True}
            ]

        elif "питан" in utterance or "калор" in utterance or "еда" in utterance:
            res['response']['text'] = (
                f'🍎 Норма сегодня: {profile.get("tdee", 0)} ккал\n\n'
                f'Пример меню:\n'
                f'• Завтрак: омлет + овсянка\n'
                f'• Обед: курица + рис + овощи\n'
                f'• Ужин: рыба + салат'
            )
            res['response']['buttons'] = [
                {"title": "Новая тренировка", "hide": True},
                {"title": "Мой прогресс", "hide": True},
                {"title": "Рандомная цитата", "hide": True}
            ]

        elif "измен" in utterance or "данные" in utterance:
            profile["step"] = "change_height"
            res['response']['text'] = 'Окей, давай обновим данные. Скажи новый рост в см.'
            res['response']['buttons'] = []
            storage[user_id] = profile
            return

        else:
            res['response']['text'] = 'Что делаем дальше?'
            res['response']['buttons'] = [
                {"title": "Новая тренировка", "hide": True},
                {"title": "Мой прогресс", "hide": True},
                {"title": "Питание сегодня", "hide": True},
                {"title": "Рандомная цитата", "hide": True},
                {"title": "Изменить данные", "hide": True}
            ]

    storage[user_id] = profile