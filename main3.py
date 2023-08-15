import telebot
import win32com.client
import pythoncom
import openai

# Set your OpenAI API key here
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

TOKEN = "6006160419:AAG5JZcFqngrKJ4tFasJesa-YZwDmTRq7hw"
bot = telebot.TeleBot(TOKEN)
chats = {}

# Define the tarot cards with meanings
tarot_cards = {
    "The Fool": "Spontaneity, free spirit, new beginnings, innocence, optimism. Yes",
    "The Magician": "Manifestation, power, action, resourcefulness, creativity. Yes",
    "The High Priestess": "Intuition, mystery, spirituality, inner knowledge. Maybe",
    "The Empress": "Fertility, nurturing, abundance, motherhood, sensuality. Yes",
    "The Emperor": "Authority, structure, leadership, stability, father figure. Yes",
    "The Hierophant": "Tradition, spirituality, religion, mentorship, guidance. Maybe",
    "The Lovers": "Love, relationships, choices, alignment, harmony. Yes",
    "The Chariot": "Willpower, determination, victory, control, progress. Yes",
    "Strength": "Courage, inner strength, resilience, compassion, self-control. Yes",
    "The Hermit": "Soul-searching, introspection, solitude, inner guidance. No",
    "Wheel of Fortune": "Change, cycles, destiny, fate, turning point. Yes",
    "Justice": "Fairness, balance, truth, cause and effect, legal matters. Maybe",
    "The Hanged Man": "Sacrifice, surrender, letting go, new perspectives. No",
    "Death": "Endings, transformation, rebirth, change, renewal. No",
    "Temperance": "Balance, moderation, harmony, patience, healing. Maybe",
    "The Devil": "Materialism, temptation, bondage, unhealthy choices. No",
    "The Tower": "Sudden change, upheaval, revelation, awakening, liberation. No",
    "The Star": "Hope, inspiration, optimism, spirituality, healing. Yes",
    "The Moon": "Intuition, emotions, illusions, subconscious, uncertainty. Maybe",
    "The Sun": "Joy, success, vitality, positivity, enlightenment. Yes",
    "Judgement": "Renewal, awakening, reckoning, transformation, inner calling. Maybe",
    "The World": "Completion, fulfillment, integration, travel, achievement. Yes",
}

minor_arcana = {
    # Wands
    "Ace of Wands": "Creative potential, inspiration, new opportunities. Yes",
    "2 of Wands": "Planning, making decisions, progress. Maybe",
    "3 of Wands": "Expansion, exploration, foresight, trade. Yes",
    "4 of Wands": "Celebration, harmony, home, joyful moments. Yes",
    "5 of Wands": "Conflict, competition, disagreements. No",
    "6 of Wands": "Victory, recognition, achievement, public acclaim. Yes",
    "7 of Wands": "Defensiveness, challenges, standing your ground. Maybe",
    "8 of Wands": "Rapid action, movement, travel, messages. Yes",
    "9 of Wands": "Resilience, perseverance, courage, last stretch. Maybe",
    "10 of Wands": "Burden, responsibility, hard work, overwhelm. No",
    "Page of Wands": "Exploration, curiosity, new beginnings. Yes",
    "Knight of Wands": "Energy, passion, adventure, impulsiveness. Maybe",
    "Queen of Wands": "Courage, confidence, leadership, determination. Yes",
    "King of Wands": "Inspiring, charismatic, visionary, bold. Yes",
    # Cups
    "Ace of Cups": "Emotional new beginning, love, intuition. Yes",
    "2 of Cups": "Unified love, partnership, connection. Yes",
    "3 of Cups": "Friendship, celebration, joy, community. Yes",
    "4 of Cups": "Contemplation, reevaluation, seeking purpose. No",
    "5 of Cups": "Loss, grief, disappointment, moving on. No",
    "6 of Cups": "Fond memories, nostalgia, innocence, childhood. Yes",
    "7 of Cups": "Choices, opportunities, imagination, wishful thinking. Maybe",
    "8 of Cups": "Disillusionment, withdrawal, seeking deeper meaning. No",
    "9 of Cups": "Contentment, satisfaction, emotional fulfillment. Yes",
    "10 of Cups": "Harmony, happiness, family, emotional bliss. Yes",
    "Page of Cups": "Creative inspiration, sensitivity, new ideas. Maybe",
    "Knight of Cups": "Romantic, dreamy, following one's heart. Yes",
    "Queen of Cups": "Nurturing, compassion, emotional stability. Yes",
    "King of Cups": "Emotional balance, wisdom, mentorship. Yes",
    # Swords
    "Ace of Swords": "Clarity, mental breakthroughs, new ideas. Yes",
    "2 of Swords": "Indecision, stalemate, difficult choices. Maybe",
    "3 of Swords": "Heartbreak, sorrow, emotional pain. No",
    "4 of Swords": "Rest, recuperation, contemplation, relaxation. No",
    "5 of Swords": "Conflict, betrayal, winning at all costs. No",
    "6 of Swords": "Transition, moving on, leaving the past behind. Maybe",
    "7 of Swords": "Deception, sneakiness, avoiding conflict. No",
    "8 of Swords": "Feeling trapped, self-imposed restrictions. No",
    "9 of Swords": "Anxiety, fear, nightmares, overthinking. No",
    "10 of Swords": "Defeat, rock bottom, hitting a low point. No",
    "Page of Swords": "Curiosity, mental agility, seeking the truth. Maybe",
    "Knight of Swords": "Ambition, determination, assertiveness. Maybe",
    "Queen of Swords": "Clarity, independence, analytical thinking. Maybe",
    "King of Swords": "Intellectual power, leadership, authority. Yes",
    # Pentacles
    "Ace of Pentacles": "Opportunity, prosperity, new venture. Yes",
    "2 of Pentacles": "Balance, adaptability, time management. Maybe",
    "3 of Pentacles": "Teamwork, collaboration, craftsmanship. Yes",
    "4 of Pentacles": "Security, stability, possessiveness, conservatism. No",
    "5 of Pentacles": "Financial hardship, poverty, isolation. No",
    "6 of Pentacles": "Generosity, giving and receiving, charity. Yes",
    "7 of Pentacles": "Assessment, reevaluation, long-term vision. Maybe",
    "8 of Pentacles": "Diligence, skill development, craftsmanship. Yes",
    "9 of Pentacles": "Abundance, luxury, self-sufficiency. Yes",
    "10 of Pentacles": "Wealth, family legacy, success, inheritance. Yes",
    "Page of Pentacles": "Manifestation, practicality, new skills. Maybe",
    "Knight of Pentacles": "Responsibility, hard work, reliability. Maybe",
    "Queen of Pentacles": "Nurturing, abundance, practicality, homeliness. Yes",
    "King of Pentacles": "Wealth, success, leadership, business acumen. Yes",
}


all_tarot_cards = {**tarot_cards, **minor_arcana}


def get_random_tarot_index():
    pythoncom.CoInitialize()
    qng = win32com.client.Dispatch("QWQNG.QNG")
    rand32 = qng.RandInt32
    index = rand32 % len(all_tarot_cards)
    pythoncom.CoUninitialize()
    return index

def get_random_tarot_card():
    index = get_random_tarot_index()
    card = list(all_tarot_cards.keys())[index]
    return card

def expand_meaning(original_meaning):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a tarot expert."},
                  {"role": "user", "content": f"Can you explain the meaning of this tarot card: {original_meaning}?"}]
    )
    expanded_meaning = response.choices[0].message['content']
    return expanded_meaning

def summarize_meaning(expanded_meaning):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing text."},
            {"role": "user", "content": f"Please summarize the following explanation: {expanded_meaning}"}
        ]
    )
    summarized_meaning = response.choices[0].message['content']
    return summarized_meaning

def process_input(user_input):
    card = get_random_tarot_card()
    meaning = all_tarot_cards[card]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a tarot expert."},
                  {"role": "user", "content": f"Can you interpret this question: {user_input}?\nCard: {card}\nMeaning: {meaning}"}]
    )
    expanded_meaning = response.choices[0].message['content']
    summarized_meaning = summarize_meaning(expanded_meaning)
    fortune_response = f"Your tarot card:\n\nCard: {card}\nMeaning: {expanded_meaning}\nSummary: {summarized_meaning}"
    return fortune_response, summarized_meaning

def get_fortune_response():
    card = get_random_tarot_card()
    meaning = all_tarot_cards[card]
    expanded_meaning = expand_meaning(meaning)
    fortune_response = f"Your tarot card:\n\nCard: {card}\nMeaning: {expanded_meaning}"
    return fortune_response, expanded_meaning

def get_tarot_card_meaning(card):
    return all_tarot_cards[card]

def generate_card_image(card_meaning):
    prompt_text = f"Create an image representing the tarot card with the following meaning: {card_meaning}"
    image_response = openai.Image.create(
        prompt=prompt_text,
        n=1,
        size="512x512"
    )
    return image_response['data'][0]['url']

def generate_spread_image(spread_meanings_text):
    cards_meanings = spread_meanings_text.split('\n\n')
    image_urls = []
    for card_meaning in cards_meanings:
        prompt_text = f"Create an image representing the tarot card with the following meaning: {card_meaning}"
        image_response = openai.Image.create(
            prompt=prompt_text,
            n=1,
            size="512x512"
        )
        image_urls.append(image_response['data'][0]['url'])
    return image_urls[0]  # For simplicity, returning the first image URL

@bot.message_handler(func=lambda message: '@atrios_bot' in message.text.lower())
def handle_mentions(message):
    chat_id = message.chat.id
    user_input = message.text.lower().replace('@atrios_bot', '').strip()
    
    fortune_response, summarized_meaning = process_input(user_input)
    card_image_url = generate_card_image(summarized_meaning)
    bot.send_message(chat_id, fortune_response)
    bot.send_photo(chat_id, card_image_url)

# Polling loop to keep the bot running
bot.polling(none_stop=True)
