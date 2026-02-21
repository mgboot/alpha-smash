"""Word dictionary for Alpha Smash — toddler-friendly words with emoji."""

import random

WORDS = [
    # Animals
    ("CAT", "🐱"),
    ("DOG", "🐶"),
    ("COW", "🐄"),
    ("PIG", "🐷"),
    ("HEN", "🐔"),
    ("BEE", "🐝"),
    ("ANT", "🐜"),
    ("OWL", "🦉"),
    ("BAT", "🦇"),
    ("FOX", "🦊"),
    ("DUCK", "🦆"),
    ("FROG", "🐸"),
    ("FISH", "🐟"),
    ("BEAR", "🐻"),
    ("LION", "🦁"),
    ("DEER", "🦌"),
    ("BIRD", "🐦"),
    ("WOLF", "🐺"),
    ("GOAT", "🐐"),
    ("CRAB", "🦀"),
    ("HORSE", "🐴"),
    ("MOUSE", "🐭"),
    ("SHEEP", "🐑"),
    ("SNAKE", "🐍"),
    ("WHALE", "🐳"),
    ("TIGER", "🐯"),
    ("ZEBRA", "🦓"),
    ("BUNNY", "🐰"),
    ("PANDA", "🐼"),
    ("MONKEY", "🐵"),
    ("TURTLE", "🐢"),
    ("KITTEN", "🐱"),
    ("CHICKEN", "🐔"),
    ("GIRAFFE", "🦒"),

    # Food
    ("PIE", "🥧"),
    ("EGG", "🥚"),
    ("CORN", "🌽"),
    ("CAKE", "🎂"),
    ("MILK", "🥛"),
    ("RICE", "🍚"),
    ("APPLE", "🍎"),
    ("GRAPE", "🍇"),
    ("LEMON", "🍋"),
    ("PIZZA", "🍕"),
    ("BREAD", "🍞"),
    ("CANDY", "🍬"),
    ("COOKIE", "🍪"),
    ("BANANA", "🍌"),
    ("CHERRY", "🍒"),

    # Home & Objects
    ("BED", "🛏️"),
    ("CUP", "🥤"),
    ("KEY", "🔑"),
    ("HAT", "🎩"),
    ("BALL", "⚽"),
    ("BELL", "🔔"),
    ("BOOK", "📖"),
    ("DOOR", "🚪"),
    ("LAMP", "💡"),
    ("SOCK", "🧦"),
    ("SHOE", "👟"),
    ("STAR", "⭐"),
    ("DRUM", "🥁"),
    ("HOUSE", "🏠"),
    ("CHAIR", "🪑"),
    ("CLOCK", "🕐"),
    ("PHONE", "📱"),

    # Nature
    ("SUN", "☀️"),
    ("BUG", "🐛"),
    ("MOON", "🌙"),
    ("RAIN", "🌧️"),
    ("TREE", "🌳"),
    ("LEAF", "🍃"),
    ("CLOUD", "☁️"),
    ("WATER", "💧"),
    ("FLOWER", "🌸"),
    ("RAINBOW", "🌈"),

    # Vehicles
    ("BUS", "🚌"),
    ("CAR", "🚗"),
    ("BOAT", "⛵"),
    ("BIKE", "🚲"),
    ("TRAIN", "🚂"),
    ("TRUCK", "🚛"),
    ("PLANE", "✈️"),
    ("ROCKET", "🚀"),

    # Body & People
    ("EAR", "👂"),
    ("EYE", "👁️"),
    ("NOSE", "👃"),
    ("HAND", "✋"),
    ("FOOT", "🦶"),
    ("BABY", "👶"),
    ("KING", "👑"),
]

# Number words for codeword display
NUMBER_WORDS = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}


def get_random_word(exclude=None):
    """Return a random (word, emoji) tuple, optionally excluding a word."""
    choices = WORDS if exclude is None else [w for w in WORDS if w[0] != exclude]
    return random.choice(choices)
