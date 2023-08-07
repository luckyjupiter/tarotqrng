import telebot
import win32com.client
import pythoncom
import openai

# Set your OpenAI API key here
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)
chats = {}

# Define the tarot cards with meanings
tarot_cards = {
    "The Fool": "Spontaneity, free spirit, new beginnings, innocence, optimism.",
    "The Magician": "Manifestation, power, action, resourcefulness, creativity.",
    "The High Priestess": "Intuition, mystery, spirituality, inner knowledge.",
    "The Empress": "Fertility, nurturing, abundance, motherhood, sensuality.",
    "The Emperor": "Authority, structure, leadership, stability, father figure.",
    "The Hierophant": "Tradition, spirituality, religion, mentorship, guidance.",
    "The Lovers": "Love, relationships, choices, alignment, harmony.",
    "The Chariot": "Willpower, determination, victory, control, progress.",
    "Strength": "Courage, inner strength, resilience, compassion, self-control.",
    "The Hermit": "Soul-searching, introspection, solitude, inner guidance.",
    "Wheel of Fortune": "Change, cycles, destiny, fate, turning point.",
    "Justice": "Fairness, balance, truth, cause and effect, legal matters.",
    "The Hanged Man": "Sacrifice, surrender, letting go, new perspectives.",
    "Death": "Endings, transformation, rebirth, change, renewal.",
    "Temperance": "Balance, moderation, harmony, patience, healing.",
    "The Devil": "Materialism, temptation, bondage, unhealthy choices.",
    "The Tower": "Sudden change, upheaval, revelation, awakening, liberation.",
    "The Star": "Hope, inspiration, optimism, spirituality, healing.",
    "The Moon": "Intuition, emotions, illusions, subconscious, uncertainty.",
    "The Sun": "Joy, success, vitality, positivity, enlightenment.",
    "Judgement": "Renewal, awakening, reckoning, transformation, inner calling.",
    "The World": "Completion, fulfillment, integration, travel, achievement.",
}

suits = ["Wands", "Cups", "Swords", "Pentacles"]
faces = ["Page", "Knight", "Queen", "King"]

minor_arcana = {
    # Wands
    "Ace of Wands": "Creative potential, inspiration, new opportunities.",
    "2 of Wands": "Planning, making decisions, progress.",
    "3 of Wands": "Expansion, exploration, foresight, trade.",
    "4 of Wands": "Celebration, harmony, home, joyful moments.",
    "5 of Wands": "Conflict, competition, disagreements.",
    "6 of Wands": "Victory, recognition, achievement, public acclaim.",
    "7 of Wands": "Defensiveness, challenges, standing your ground.",
    "8 of Wands": "Rapid action, movement, travel, messages.",
    "9 of Wands": "Resilience, perseverance, courage, last stretch.",
    "10 of Wands": "Burden, responsibility, hard work, overwhelm.",
    "Page of Wands": "Exploration, curiosity, new beginnings.",
    "Knight of Wands": "Energy, passion, adventure, impulsiveness.",
    "Queen of Wands": "Courage, confidence, leadership, determination.",
    "King of Wands": "Inspiring, charismatic, visionary, bold.",

    # Cups
    "Ace of Cups": "Emotional new beginning, love, intuition.",
    "2 of Cups": "Unified love, partnership, connection.",
    "3 of Cups": "Friendship, celebration, joy, community.",
    "4 of Cups": "Contemplation, reevaluation, seeking purpose.",
    "5 of Cups": "Loss, grief, disappointment, moving on.",
    "6 of Cups": "Fond memories, nostalgia, innocence, childhood.",
    "7 of Cups": "Choices, opportunities, imagination, wishful thinking.",
    "8 of Cups": "Disillusionment, withdrawal, seeking deeper meaning.",
    "9 of Cups": "Contentment, satisfaction, emotional fulfillment.",
    "10 of Cups": "Harmony, happiness, family, emotional bliss.",
    "Page of Cups": "Creative inspiration, sensitivity, new ideas.",
    "Knight of Cups": "Romantic, dreamy, following one's heart.",
    "Queen of Cups": "Nurturing, compassion, emotional stability.",
    "King of Cups": "Emotional balance, wisdom, mentorship.",

    # Swords
    "Ace of Swords": "Clarity, mental breakthroughs, new ideas.",
    "2 of Swords": "Indecision, stalemate, difficult choices.",
    "3 of Swords": "Heartbreak, sorrow, emotional pain.",
    "4 of Swords": "Rest, recuperation, contemplation, relaxation.",
    "5 of Swords": "Conflict, betrayal, winning at all costs.",
    "6 of Swords": "Transition, moving on, leaving the past behind.",
    "7 of Swords": "Deception, sneakiness, avoiding conflict.",
    "8 of Swords": "Feeling trapped, self-imposed restrictions.",
    "9 of Swords": "Anxiety, fear, nightmares, overthinking.",
    "10 of Swords": "Defeat, rock bottom, hitting a low point.",
    "Page of Swords": "Curiosity, mental agility, seeking the truth.",
    "Knight of Swords": "Ambition, determination, assertiveness.",
    "Queen of Swords": "Clarity, independence, analytical thinking.",
    "King of Swords": "Intellectual power, leadership, authority.",

    # Pentacles
    "Ace of Pentacles": "Opportunity, prosperity, new venture.",
    "2 of Pentacles": "Balance, adaptability, time management.",
    "3 of Pentacles": "Teamwork, collaboration, craftsmanship.",
    "4 of Pentacles": "Security, stability, possessiveness, conservatism.",
    "5 of Pentacles": "Financial hardship, poverty, isolation.",
    "6 of Pentacles": "Generosity, giving and receiving, charity.",
    "7 of Pentacles": "Assessment, reevaluation, long-term vision.",
    "8 of Pentacles": "Diligence, skill development, craftsmanship.",
    "9 of Pentacles": "Abundance, luxury, self-sufficiency.",
    "10 of Pentacles": "Wealth, family legacy, success, inheritance.",
    "Page of Pentacles": "Manifestation, practicality, new skills.",
    "Knight of Pentacles": "Responsibility, hard work, reliability.",
    "Queen of Pentacles": "Nurturing, abundance, practicality, homeliness.",
    "King of Pentacles": "Wealth, success, leadership, business acumen.",
}

all_tarot_cards = {**tarot_cards, **minor_arcana}

def get_tarot_card():
    """Fetch a random tarot card using the quantum device."""
    pythoncom.CoInitialize()  # Initialize the COM library
    qng = win32com.client.Dispatch("QWQNG.QNG")
    rand32 = qng.RandInt32

    # Get a random index between 0 and 77 (inclusive)
    index = rand32 % len(all_tarot_cards)
    card = list(all_tarot_cards.keys())[index]

    pythoncom.CoUninitialize()  # Uninitialize the COM library
    return card

def get_tarot_card_meaning(card):
    """Get the meaning of the given tarot card using the OpenAI Chat API."""
    prompt = f"What is the meaning of {card} tarot card?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fortune teller."},
            {"role": "user", "content": prompt},
        ],
    )

    meaning = response['choices'][0]['message']['content']
    return meaning

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_message = message.text

    if "@" + bot.get_me().username in user_message:
        tarot_card = get_tarot_card()
        tarot_card_meaning = get_tarot_card_meaning(tarot_card)
        bot.send_message(chat_id, f"Your tarot card is: {tarot_card}\nMeaning: {tarot_card_meaning}")

        # Simplified logic to add message to chat without checking existence (dict.setdefault will handle that)
        chats.setdefault(chat_id, []).append({"role": "user", "content": user_message})

# Polling loop to keep the bot running
bot.polling(none_stop=True)
