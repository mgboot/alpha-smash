"""Word dictionary for Alpha Smash — toddler-friendly words with emoji.

Supports English, Latin American Spanish, and German.  Words are stored
with their *display* form (including diacritics).  Use ``get_input_form``
to obtain the ASCII-only version used for keyboard matching.
"""

import random

# ---------------------------------------------------------------------------
# Word lists keyed by language code
# ---------------------------------------------------------------------------

WORDS = {
    "en": [
        # Animals
        ("CAT", "🐱"), ("DOG", "🐶"), ("COW", "🐄"), ("PIG", "🐷"),
        ("HEN", "🐔"), ("BEE", "🐝"), ("ANT", "🐜"), ("OWL", "🦉"),
        ("BAT", "🦇"), ("FOX", "🦊"), ("DUCK", "🦆"), ("FROG", "🐸"),
        ("FISH", "🐟"), ("BEAR", "🐻"), ("LION", "🦁"), ("DEER", "🦌"),
        ("BIRD", "🐦"), ("WOLF", "🐺"), ("GOAT", "🐐"), ("CRAB", "🦀"),
        ("HORSE", "🐴"), ("MOUSE", "🐭"), ("SHEEP", "🐑"), ("SNAKE", "🐍"),
        ("WHALE", "🐳"), ("TIGER", "🐯"), ("ZEBRA", "🦓"), ("BUNNY", "🐰"),
        ("PANDA", "🐼"), ("MONKEY", "🐵"), ("TURTLE", "🐢"), ("KITTEN", "🐱"),
        ("CHICKEN", "🐔"), ("GIRAFFE", "🦒"),
        # Food
        ("PIE", "🥧"), ("EGG", "🥚"), ("CORN", "🌽"), ("CAKE", "🎂"),
        ("MILK", "🥛"), ("RICE", "🍚"), ("APPLE", "🍎"), ("GRAPE", "🍇"),
        ("LEMON", "🍋"), ("PIZZA", "🍕"), ("BREAD", "🍞"), ("CANDY", "🍬"),
        ("COOKIE", "🍪"), ("BANANA", "🍌"), ("CHERRY", "🍒"),
        # Home & Objects
        ("BED", "🛏️"), ("CUP", "🥤"), ("KEY", "🔑"), ("HAT", "🎩"),
        ("BALL", "⚽"), ("BELL", "🔔"), ("BOOK", "📖"), ("DOOR", "🚪"),
        ("LAMP", "💡"), ("SOCK", "🧦"), ("SHOE", "👟"), ("STAR", "⭐"),
        ("DRUM", "🥁"), ("HOUSE", "🏠"), ("CHAIR", "🪑"), ("CLOCK", "🕐"),
        ("PHONE", "📱"),
        # Nature
        ("SUN", "☀️"), ("BUG", "🐛"), ("MOON", "🌙"), ("RAIN", "🌧️"),
        ("TREE", "🌳"), ("LEAF", "🍃"), ("CLOUD", "☁️"), ("WATER", "💧"),
        ("FLOWER", "🌸"), ("RAINBOW", "🌈"),
        # Vehicles
        ("BUS", "🚌"), ("CAR", "🚗"), ("BOAT", "⛵"), ("BIKE", "🚲"),
        ("TRAIN", "🚂"), ("TRUCK", "🚛"), ("PLANE", "✈️"), ("ROCKET", "🚀"),
        # Body & People
        ("EAR", "👂"), ("EYE", "👁️"), ("NOSE", "👃"), ("HAND", "✋"),
        ("FOOT", "🦶"), ("BABY", "👶"), ("KING", "👑"),
    ],

    "es": [
        # Animales
        ("GATO", "🐱"), ("PERRO", "🐶"), ("VACA", "🐄"), ("CERDO", "🐷"),
        ("PATO", "🦆"), ("RANA", "🐸"), ("PEZ", "🐟"), ("OSO", "🐻"),
        ("LEÓN", "🦁"), ("BÚHO", "🦉"), ("AVE", "🐦"), ("LOBO", "🐺"),
        ("CABRA", "🐐"), ("CABALLO", "🐴"), ("RATÓN", "🐭"), ("OVEJA", "🐑"),
        ("MONO", "🐵"), ("TIGRE", "🐯"), ("CEBRA", "🦓"), ("CONEJO", "🐰"),
        ("PANDA", "🐼"), ("TORTUGA", "🐢"), ("POLLO", "🐔"), ("JIRAFA", "🦒"),
        ("BALLENA", "🐳"), ("ABEJA", "🐝"), ("HORMIGA", "🐜"),
        ("ZORRO", "🦊"), ("CANGREJO", "🦀"), ("VENADO", "🦌"),
        ("NIÑO", "👶"),
        # Comida
        ("HUEVO", "🥚"), ("MAÍZ", "🌽"), ("TORTA", "🎂"), ("LECHE", "🥛"),
        ("ARROZ", "🍚"), ("MANZANA", "🍎"), ("UVA", "🍇"), ("LIMÓN", "🍋"),
        ("PIZZA", "🍕"), ("PAN", "🍞"), ("DULCE", "🍬"), ("GALLETA", "🍪"),
        ("BANANA", "🍌"), ("CEREZA", "🍒"),
        # Hogar y objetos
        ("CAMA", "🛏️"), ("TAZA", "🥤"), ("LLAVE", "🔑"), ("BOLA", "⚽"),
        ("LIBRO", "📖"), ("PUERTA", "🚪"), ("LUZ", "💡"), ("CASA", "🏠"),
        ("SILLA", "🪑"), ("RELOJ", "🕐"), ("ZAPATO", "👟"),
        ("ESTRELLA", "⭐"), ("TAMBOR", "🥁"), ("CAMPANA", "🔔"),
        # Naturaleza
        ("SOL", "☀️"), ("LUNA", "🌙"), ("LLUVIA", "🌧️"), ("ÁRBOL", "🌳"),
        ("HOJA", "🍃"), ("NUBE", "☁️"), ("AGUA", "💧"), ("FLOR", "🌸"),
        # Vehículos
        ("BUS", "🚌"), ("CARRO", "🚗"), ("BARCO", "⛵"), ("BICI", "🚲"),
        ("TREN", "🚂"), ("CAMIÓN", "🚛"), ("AVIÓN", "✈️"), ("COHETE", "🚀"),
        # Cuerpo y personas
        ("OREJA", "👂"), ("OJO", "👁️"), ("NARIZ", "👃"), ("MANO", "✋"),
        ("PIE", "🦶"), ("BEBÉ", "👶"), ("REY", "👑"),
    ],

    "de": [
        # Tiere
        ("KATZE", "🐱"), ("HUND", "🐶"), ("KUH", "🐄"), ("SCHWEIN", "🐷"),
        ("ENTE", "🦆"), ("FROSCH", "🐸"), ("FISCH", "🐟"), ("BÄR", "🐻"),
        ("LÖWE", "🦁"), ("EULE", "🦉"), ("VOGEL", "🐦"), ("WOLF", "🐺"),
        ("ZIEGE", "🐐"), ("PFERD", "🐴"), ("MAUS", "🐭"), ("SCHAF", "🐑"),
        ("AFFE", "🐵"), ("TIGER", "🐯"), ("ZEBRA", "🦓"), ("HASE", "🐰"),
        ("PANDA", "🐼"), ("HUHN", "🐔"), ("GIRAFFE", "🦒"), ("WAL", "🐳"),
        ("SCHLANGE", "🐍"), ("BIENE", "🐝"), ("AMEISE", "🐜"),
        ("FUCHS", "🦊"), ("KREBS", "🦀"), ("REH", "🦌"),
        # Essen
        ("EI", "🥚"), ("MAIS", "🌽"), ("KUCHEN", "🎂"), ("MILCH", "🥛"),
        ("REIS", "🍚"), ("APFEL", "🍎"), ("TRAUBE", "🍇"), ("ZITRONE", "🍋"),
        ("PIZZA", "🍕"), ("BROT", "🍞"), ("KEKS", "🍪"), ("BANANE", "🍌"),
        ("KIRSCHE", "🍒"),
        # Haus und Objekte
        ("BETT", "🛏️"), ("TASSE", "🥤"), ("HUT", "🎩"), ("BALL", "⚽"),
        ("GLOCKE", "🔔"), ("BUCH", "📖"), ("TÜR", "🚪"), ("LAMPE", "💡"),
        ("SCHUH", "👟"), ("STERN", "⭐"), ("TROMMEL", "🥁"), ("HAUS", "🏠"),
        ("STUHL", "🪑"), ("UHR", "🕐"),
        # Natur
        ("SONNE", "☀️"), ("MOND", "🌙"), ("REGEN", "🌧️"), ("BAUM", "🌳"),
        ("BLATT", "🍃"), ("WOLKE", "☁️"), ("WASSER", "💧"), ("BLUME", "🌸"),
        # Fahrzeuge
        ("BUS", "🚌"), ("AUTO", "🚗"), ("BOOT", "⛵"), ("ZUG", "🚂"),
        ("RAKETE", "🚀"), ("FAHRRAD", "🚲"), ("FLUGZEUG", "✈️"),
        # Körper und Menschen
        ("OHR", "👂"), ("AUGE", "👁️"), ("NASE", "👃"), ("HAND", "✋"),
        ("BABY", "👶"), ("KÖNIG", "👑"),
    ],
}

# ---------------------------------------------------------------------------
# Diacritic mapping — display char → keyboard input char
# ---------------------------------------------------------------------------

DIACRITIC_MAP = {
    "es": {"Ñ": "N", "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"},
    "de": {"Ä": "A", "Ö": "O", "Ü": "U"},
}

# ---------------------------------------------------------------------------
# Localised UI strings
# ---------------------------------------------------------------------------

UI_STRINGS = {
    "en": {"celebration": "Great job!", "prompt": "Press:"},
    "es": {"celebration": "¡Muy bien!", "prompt": "Pulsa:"},
    "de": {"celebration": "Super gemacht!", "prompt": "Drücke:"},
}

# Language display order (used for flag buttons)
LANGUAGES = ["en", "es", "de"]

# ---------------------------------------------------------------------------
# Number words for codeword display (always English)
# ---------------------------------------------------------------------------

NUMBER_WORDS = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_input_form(word, lang):
    """Return the keyboard-input form of *word* (diacritics stripped)."""
    mapping = DIACRITIC_MAP.get(lang, {})
    return "".join(mapping.get(ch, ch) for ch in word)


def get_random_word(lang="en", exclude=None):
    """Return a random (display_word, emoji) tuple for *lang*."""
    word_list = WORDS[lang]
    choices = word_list if exclude is None else [w for w in word_list if w[0] != exclude]
    return random.choice(choices)
