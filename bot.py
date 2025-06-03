import os
import random
import asyncio
import nest_asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile, Voice
from difflib import SequenceMatcher

# Fix permissions
os.chmod("images", 0o755)
for file in os.listdir("images"):
    os.chmod(f"images/{file}", 0o644)

nest_asyncio.apply()

API_TOKEN = "your-actual-bot-key"

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Learn Vocabulary")],
        [KeyboardButton(text="🎧 Listening")],
        [KeyboardButton(text="📖 Reading")],
        [KeyboardButton(text="✍️ Writing")],
        [KeyboardButton(text="📊 Results")]
    ],
    resize_keyboard=True
)

final_test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Final Test")],
        [KeyboardButton(text="⬅️ Back to Menu")]
    ],
    resize_keyboard=True
)

def get_dynamic_menu(uid):
    progress = user_progress.get(uid, set())
    show_quiz_buttons = progress == set(flashcard_categories.keys())
    show_final_test = user_state.get(uid, {}).get("show_final_test", False)

    base_buttons = [[KeyboardButton(text="📘 Learn Vocabulary")]]
    if show_quiz_buttons:
        base_buttons += [
            [KeyboardButton(text="🎧 Listening")],
            [KeyboardButton(text="📖 Reading")],
            [KeyboardButton(text="✍️ Writing")],
            [KeyboardButton(text="📊 Results")]
        ]
        if show_final_test:
            base_buttons += [[KeyboardButton(text="📋 Final Test")]]

    return ReplyKeyboardMarkup(keyboard=base_buttons, resize_keyboard=True)


# === Vocabulary Learning ===
flashcard_categories = {
    "🥦 Vegetables": "https://quizlet.com/ru/1050306480/vegetables-flash-cards/?i=3hzpf6&x=1jqU",
    "🍎 Fruits": "https://quizlet.com/ru/1050306479/fruits-flash-cards/?i=3hzpf6&x=1jqU",
    "🧃 Drinks": "https://quizlet.com/fi/1050312572/drinks-flash-cards/?i=3hzpf6&x=1jqU",
    "🍳 Breakfast Foods": "https://quizlet.com/fi/1050312570/breakfast-foods-flash-cards/?i=3hzpf6&x=1jqU",
    "🍽 Lunch/Dinner Foods": "https://quizlet.com/de/1050314772/lunchdinner-foods-flash-cards/?i=3hzpf6&x=1jqU",
    "🍰 Sweets/Desserts": "https://quizlet.com/de/1050315473/sweetsdesserts-flash-cards/?i=3hzpf6&x=1jqU"
}

learn_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=cat)] for cat in flashcard_categories] + [[KeyboardButton(text="⬅️ Back to Menu")]],
    resize_keyboard=True
)

user_progress = {}

@dp.message(lambda msg: msg.text == "📘 Learn Vocabulary")
async def learn_menu(message: types.Message):
    uid = message.chat.id
    await message.answer("📚 Choose a category to study vocabulary:", reply_markup=learn_kb)

@dp.message(lambda msg: msg.text in flashcard_categories)
async def send_flashcards(message: types.Message):
    uid = message.chat.id
    category = message.text
    link = flashcard_categories[category]

    await message.answer(
        f"🔤 Here are the vocabulary flashcards for {category}:\n"
        f"{link}\n\n"
        "📈 Study all the words and come back to choose another category!",
        reply_markup=learn_kb  # <- stay in the category menu
    )

    # Track progress
    progress = user_progress.setdefault(uid, set())
    progress.add(category)

    if progress == set(flashcard_categories.keys()):
        await message.answer(
            "🎉 You've studied all categories! Great job!\n\nNow you're ready to practice with quizzes!",
            reply_markup=get_dynamic_menu(uid)  # return to dynamic main menu
        )

@dp.message(lambda msg: msg.text == "⬅️ Back to Menu")
async def back_to_main(message: types.Message):
    uid = message.chat.id
    await message.answer("🔙 Back to the main menu.", reply_markup=get_dynamic_menu(uid))

# === Original Quiz Logic (Unchanged) ===

reading_entries = [
    ("Lily starts her day with crisp apples and milk, occasionally pancakes.", ["apples"]),
    ("Tom loves pizza but balances it with lemonade.", ["pizza"]),
    ("Anna prefers tea and toast.", ["toast"]),
    ("Ben's English breakfast includes eggs, bacon, tomatoes, and beans.", ["eggs"]),
    ("Nina enjoys soup packed with vegetables.", ["soup"]),
    ("Liam eats sandwiches and orange juice.", ["sandwiches"]),
    ("Clara eats cereal with bananas and honey.", ["bananas"]),
    ("Omar eats pancakes and cocoa on Sundays.", ["pancakes"]),
    ("Ella enjoys burgers and fries with friends.", ["burgers"]),
    ("Sophie eats pasta with tomato sauce and cheese.", ["pasta"]),
    ("Leo eats cornflakes and milk.", ["cornflakes"]),
    ("Zoe eats jasmine rice and curry.", ["rice"]),
    ("Max makes tacos with beans, salsa, and guacamole.", ["tacos"]),
    ("Chloe loves strawberries with whipped cream.", ["strawberries"]),
    ("Ryan makes noodles with carrots and vegetables.", ["noodles"]),
    ("Emma eats grapes with cheese in the evening.", ["grapes"]),
    ("Sam eats muffins and fruit juice mid-morning.", ["muffins"]),
    ("Jade eats toast with jam and coffee.", ["toast"]),
    ("Noah eats apples and peanut butter post-workout.", ["apples"]),
    ("Amy eats salad with grilled chicken.", ["salad"])
]

listening_entries = [
    ("Anna eats an apple and a banana.", ["apple", "banana"]),
    ("Ben has bread and cheese for breakfast.", ["bread", "cheese"]),
    ("Clara drinks orange juice every morning.", ["orange"]),
    ("David likes grapes and milk.", ["grapes", "milk"]),
    ("Emma eats cereal and strawberries.", ["cereal", "strawberries"]),
    ("Finn loves toast with jam.", ["toast", "jam"]),
    ("Grace eats carrots and cucumbers.", ["carrots", "cucumbers"]),
    ("Harry enjoys soup and salad.", ["soup", "salad"]),
    ("Isla drinks tea with lemon.", ["lemon", "tea"]),
    ("Jack eats yogurt and honey.", ["yogurt", "honey"]),
    ("Kate has eggs and tomatoes.", ["eggs", "tomatoes"]),
    ("Liam eats watermelon and pineapple.", ["watermelon", "pineapple"]),
    ("Mia likes pizza and soda.", ["pizza", "soda"]),
    ("Noah eats pasta and peas.", ["pasta", "peas"]),
    ("Olivia drinks milk and water.", ["milk", "water"]),
    ("Paul eats chicken and rice.", ["chicken", "rice"]),
    ("Quinn likes pears and plums.", ["pears", "plums"]),
    ("Rose eats chocolate and cookies.", ["chocolate", "cookies"]),
    ("Sam has sausages and mashed potatoes.", ["sausages", "mashed potatoes"]),
    ("Tina enjoys salad and fish.", ["salad", "fish"])
]

writing_data = {
    "apple.png": ["apple"],
    "aubergine or eggplant.png": ["aubergine", "eggplant"],
    "avocado.png": ["avocado"],
    "banana.png": ["banana"],
    "bell pepper.png": ["bell pepper", "pepper"],
    "blueberry.png": ["blueberry", "blueberries"],
    "broccoli.png": ["broccoli"],
    "cabbage.png": ["cabbage"],
    "carrot.png": ["carrot", "carrots"],
    "cauliflower.png": ["cauliflower"],
    "cereal.png": ["cereal"],
    "corn.png": ["corn"],
    "grapes.png": ["grapes"],
    "kiwi.png": ["kiwi"],
    "orange.png": ["orange"],
    "pear.png": ["pear"],
    "pineapple.png": ["pineapple"],
    "strawberry.png": ["strawberry", "strawberries"],
    "tomato.png": ["tomato", "tomatoes"],
    "watermelon.png": ["watermelon"]
}

user_answers = {}
user_state = {}

# Helper

def is_typo(user_word, correct_word):
    return SequenceMatcher(None, user_word, correct_word).ratio() > 0.75

def check_typo(user_input, correct_answers):
    for correct in correct_answers:
        if is_typo(user_input, correct):
            return correct
    return None

def normalize(text):
    return text.lower().replace(",", "").replace("and", " ").split()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    uid = message.chat.id
    user_answers.pop(uid, None)
    user_progress.pop(uid, None)
    user_state[uid] = {
        "score": 0,
        "attempts": 0,
        "mistakes": [],
        "last_question_wrong": False,
        "show_final_test": False
    }

    await message.answer(
        "👋 Hello! Welcome to Yummy English Bot!\n\n"
        "Let's learn English with tasty topics about food! 🍎🍕🍌\n\n"
        "You can practice:\n"
        "🎧 Listening - Hear descriptions and identify foods\n"
        "📖 Reading - Read passages and answer questions\n"
        "✍️ Writing - Name foods from pictures\n\n"
        "Choose an activity below ⬇️",
        reply_markup=get_dynamic_menu(uid)
    )


@dp.message(lambda msg: msg.text == "🎧 Listening")
async def handle_listening(message: types.Message):
    index = random.randint(0, len(listening_entries) - 1)
    text, correct_answers = listening_entries[index]
    user_answers[message.chat.id] = correct_answers

    audio_path = f"audio/{index + 1}.mp3"
    if os.path.exists(audio_path):
        await bot.send_voice(
            chat_id=message.chat.id,
            voice=FSInputFile(audio_path),
            caption="🎧 Listen carefully to the description!"
        )
    else:
        await message.answer(f"🔊 Audio not available. Here's the text:\n\n{text}")

    await message.answer("❓ Name any food mentioned in the description.")

@dp.message(lambda msg: msg.text == "📖 Reading")
async def handle_reading(message: types.Message):
    text, correct_answers = random.choice(reading_entries)
    user_answers[message.chat.id] = correct_answers

    await message.answer(f"📖 Read this passage carefully:\n\n{text}")

    flat_correct = correct_answers[0]
    all_foods = list(set([item for sub in [entry[1] for entry in reading_entries] for item in sub]))
    wrong_options = random.sample([f for f in all_foods if f not in correct_answers], 2)
    options = [flat_correct] + wrong_options
    random.shuffle(options)

    await message.answer("❓ Name any food mentioned in the passage:\n" +
                         "\n".join([f"- {opt.capitalize()}" for opt in options]))

@dp.message(lambda msg: msg.text == "✍️ Writing")
async def handle_writing(message: types.Message):
    img_name, correct_answers = random.choice(list(writing_data.items()))
    user_answers[message.chat.id] = correct_answers

    try:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=types.FSInputFile(f"images/{img_name}"),
            caption="✍️ What food is this? Type its name in English."
        )
    except Exception:
        await message.answer("⚠️ Couldn't load the image. Developer is checking logs.")

@dp.message(lambda msg: msg.text == "📊 Results")
async def handle_results(message: types.Message):
    uid = message.chat.id
    state = user_state.get(uid)
    if not state:
        await message.answer("ℹ️ Please select an activity from the menu first.")
        return

    score = state["score"]
    attempts = state["attempts"]
    mistakes = state["mistakes"]
    accuracy = round((score / attempts) * 100) if attempts else 0

    msg_text = (
        f"📊 Your Session Stats\n\n"
        f"✅ Correct: {score}\n"
        f"❌ Incorrect: {attempts - score}\n"
        f"🎯 Accuracy: {accuracy}%\n"
    )

    if mistakes:
        msg_text += "\n🧠 Mistakes:\n" + "\n\n".join(mistakes)

    user_state[uid]["show_final_test"] = True
    await message.answer(msg_text, reply_markup=get_dynamic_menu(uid))

@dp.message(lambda msg: msg.text == "📋 Final Test")
async def handle_final_test(message: types.Message):
    test_link = "https://forms.gle/etsPw4HyhidJ7B7r5"
    await message.answer(f"📝 Here's your final test:\n{test_link}")

@dp.message()
async def handle_answer(message: types.Message):
    uid = message.chat.id
    expected = user_answers.get(uid)
    if not expected:
        await message.answer("ℹ️ Please select an activity from the menu first.")
        return

    user_state.setdefault(uid, {"score": 0, "attempts": 0, "mistakes": []})
    user_input_raw = message.text.lower()
    normalized_input = user_input_raw.replace(",", " ").replace(" and ", " ").split()
    normalized_input = [w.strip() for w in normalized_input if w.strip()]

    matched = set()
    almost = []

    for word in normalized_input:
        for correct in expected:
            if word == correct:
                matched.add(correct)
            elif SequenceMatcher(None, word, correct).ratio() > 0.75:
                almost.append((word, correct))

    # Prepare question reference
    question_text = None
    if message.reply_to_message:
        question_text = message.reply_to_message.caption or message.reply_to_message.text
    if not question_text:
        question_text = "Previous question"

    if matched:
        user_state[uid]["score"] += 1
        user_state[uid]["attempts"] += 1
        user_answers.pop(uid, None)
        user_state[uid].pop("last_question_wrong", None)
        await message.answer("✅ Correct! Great job!", reply_markup=get_dynamic_menu(uid))
    elif almost:
        feedback = "\n".join([
            f"🟡 Almost correct! You wrote: <b>{wrong}</b>\nDid you mean: <b>{right}</b>?"
            for wrong, right in almost
        ])
        await message.answer(feedback + "\nTry again!")
    else:
        # Only track first error for the question
        user_state[uid]["attempts"] += 1
        user_state[uid]["mistakes"].append(
            f"❌ You typed: '{user_input_raw}'\n✅ Correct: {', '.join(expected)}"
        )
        await message.answer("❌ Not quite. Try again.")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
