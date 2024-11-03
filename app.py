from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Sample route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Sample /generate route for poetry generation
@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()  # Get the JSON data from the request
        seed_text = data.get('start_text', '')
        length = int(data.get('length', 5))  # Default to 5 lines if not provided
        custom_words = data.get('custom_words', '')
        theme = data.get('theme', 'general')

        # Define word categories for better structure
        nouns = ["dream", "light", "night", "shadow", "whisper", 
                 "stars", "heart", "soul", "thunder", "sun",
                 "kite", "fox", "dew", "puzzle", "honesty",
                 "wind", "snow", "bird", "friend", "love"]
        
        verbs = ["flow", "shine", "dance", "whisper", "bloom",
                 "flutter", "glow", "sparkle", "sing", "float"]

        adjectives = ["gentle", "bright", "soft", "dark", "sweet",
                      "silent", "endless", "warm", "cool", "clear"]

        # Select words based on the theme
        if theme == "nature":
            nouns += ["tree", "river", "mountain", "sky", "ocean"]
            verbs += ["grow", "sway", "wave", "chirp", "sing"]
            adjectives += ["lush", "vast", "serene", "blooming", "colorful"]
        elif theme == "love":
            nouns += ["heart", "kiss", "embrace", "passion", "memory"]
            verbs += ["cherish", "adore", "long", "yearn", "believe"]
            adjectives += ["eternal", "boundless", "fiery", "tender", "loving"]
        
        # Combine words into a pool
        words = {
            'nouns': nouns + seed_text.split() + custom_words.split(','),
            'verbs': verbs,
            'adjectives': adjectives
        }

        # Emojis associated with themes
        emojis = {
            "nature": "🌳🌼🌿🌈",
            "love": "❤️💕💘",
            "sadness": "😢💔🌧️",
            "joy": "😊🎉🌞",
            "general": "✨🌟💫"
        }

        selected_emojis = emojis.get(theme, "")
        poetic_lines = []

        # Generate lines of poetry based on length
        for _ in range(length):
            line_structure = random.choice([
                "The {adj} {noun} will {verb}.",
                "{verb} like a {adj} {noun}.",
                "In the {adj} {noun}, I {verb}.",
                "A {adj} {noun} whispers {verb}."
            ])
            line = line_structure.format(
                noun=random.choice(words['nouns']),
                verb=random.choice(words['verbs']),
                adj=random.choice(words['adjectives'])
            )
            if selected_emojis:
                line += " " + random.choice(selected_emojis)  # Add a random emoji
            poetic_lines.append(line.capitalize())

        return jsonify({'generated_poetry': '\n'.join(poetic_lines)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
