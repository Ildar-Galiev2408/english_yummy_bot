from gtts import gTTS
import os

# Your 20 listening texts
listening_texts = [
    "Anna eats an apple and a banana.",
    "Ben has bread and cheese for breakfast.",
    "Clara drinks orange juice every morning.",
    "David likes grapes and milk.",
    "Emma eats cereal and strawberries.",
    "Finn loves toast with jam.",
    "Grace eats carrots and cucumbers.",
    "Harry enjoys soup and salad.",
    "Isla drinks tea with lemon.",
    "Jack eats yogurt and honey.",
    "Kate has eggs and tomatoes.",
    "Liam eats watermelon and pineapple.",
    "Mia likes pizza and soda.",
    "Noah eats pasta and peas.",
    "Olivia drinks milk and water.",
    "Paul eats chicken and rice.",
    "Quinn likes pears and plums.",
    "Rose eats chocolate and cookies.",
    "Sam has sausages and mashed potatoes.",
    "Tina enjoys salad and fish."
]

# Make folder if not exists
os.makedirs("audio", exist_ok=True)

# Generate audio files
for i, text in enumerate(listening_texts, start=1):
    tts = gTTS(text=text, lang="en")
    path = f"audio/{i}.mp3"
    tts.save(path)
    print(f"✅ Saved {path}")
