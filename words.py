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
        ("GATO", "🐱", "el"), ("PERRO", "🐶", "el"), ("VACA", "🐄", "la"),
        ("CERDO", "🐷", "el"), ("PATO", "🦆", "el"), ("RANA", "🐸", "la"),
        ("PEZ", "🐟", "el"), ("OSO", "🐻", "el"), ("LEÓN", "🦁", "el"),
        ("BÚHO", "🦉", "el"), ("AVE", "🐦", "el"), ("LOBO", "🐺", "el"),
        ("CABRA", "🐐", "la"), ("CABALLO", "🐴", "el"), ("RATÓN", "🐭", "el"),
        ("OVEJA", "🐑", "la"), ("MONO", "🐵", "el"), ("TIGRE", "🐯", "el"),
        ("CEBRA", "🦓", "la"), ("CONEJO", "🐰", "el"), ("PANDA", "🐼", "el"),
        ("TORTUGA", "🐢", "la"), ("POLLO", "🐔", "el"), ("JIRAFA", "🦒", "la"),
        ("BALLENA", "🐳", "la"), ("ABEJA", "🐝", "la"), ("HORMIGA", "🐜", "la"),
        ("ZORRO", "🦊", "el"), ("CANGREJO", "🦀", "el"), ("VENADO", "🦌", "el"),
        ("NIÑO", "👶", "el"),
        # Comida
        ("HUEVO", "🥚", "el"), ("MAÍZ", "🌽", "el"), ("BIZCOCHO", "🎂", "el"),
        ("LECHE", "🥛", "la"), ("ARROZ", "🍚", "el"), ("MANZANA", "🍎", "la"),
        ("UVA", "🍇", "la"), ("LIMÓN", "🍋", "el"), ("PIZZA", "🍕", "la"),
        ("PAN", "🍞", "el"), ("DULCE", "🍬", "el"), ("GALLETA", "🍪", "la"),
        ("GUINEO", "🍌", "el"), ("CEREZA", "🍒", "la"),
        # Hogar y objetos
        ("CAMA", "🛏️", "la"), ("TAZA", "🥤", "la"), ("LLAVE", "🔑", "la"),
        ("BOLA", "⚽", "la"), ("LIBRO", "📖", "el"), ("PUERTA", "🚪", "la"),
        ("LUZ", "💡", "la"), ("CASA", "🏠", "la"), ("SILLA", "🪑", "la"),
        ("RELOJ", "🕐", "el"), ("ZAPATO", "👟", "el"), ("ESTRELLA", "⭐", "la"),
        ("TAMBOR", "🥁", "el"), ("CAMPANA", "🔔", "la"),
        # Naturaleza
        ("SOL", "☀️", "el"), ("LUNA", "🌙", "la"), ("LLUVIA", "🌧️", "la"),
        ("ÁRBOL", "🌳", "el"), ("HOJA", "🍃", "la"), ("NUBE", "☁️", "la"),
        ("AGUA", "💧", "el"), ("FLOR", "🌸", "la"),
        # Vehículos
        ("GUAGUA", "🚌", "la"), ("CARRO", "🚗", "el"), ("BARCO", "⛵", "el"),
        ("BICI", "🚲", "la"), ("TREN", "🚂", "el"), ("CAMIÓN", "🚛", "el"),
        ("AVIÓN", "✈️", "el"), ("COHETE", "🚀", "el"),
        # Cuerpo y personas
        ("OREJA", "👂", "la"), ("OJO", "👁️", "el"), ("NARIZ", "👃", "la"),
        ("MANO", "✋", "la"), ("PIE", "🦶", "el"), ("BEBÉ", "👶", "el"),
        ("REY", "👑", "el"),
    ],

    "de": [
        # Tiere
        ("KATZE", "🐱", "die"), ("HUND", "🐶", "der"), ("KUH", "🐄", "die"),
        ("SCHWEIN", "🐷", "das"), ("ENTE", "🦆", "die"), ("FROSCH", "🐸", "der"),
        ("FISCH", "🐟", "der"), ("BÄR", "🐻", "der"), ("LÖWE", "🦁", "der"),
        ("EULE", "🦉", "die"), ("VOGEL", "🐦", "der"), ("WOLF", "🐺", "der"),
        ("ZIEGE", "🐐", "die"), ("PFERD", "🐴", "das"), ("MAUS", "🐭", "die"),
        ("SCHAF", "🐑", "das"), ("AFFE", "🐵", "der"), ("TIGER", "🐯", "der"),
        ("ZEBRA", "🦓", "das"), ("HASE", "🐰", "der"), ("PANDA", "🐼", "der"),
        ("HUHN", "🐔", "das"), ("GIRAFFE", "🦒", "die"), ("WAL", "🐳", "der"),
        ("SCHLANGE", "🐍", "die"), ("BIENE", "🐝", "die"), ("AMEISE", "🐜", "die"),
        ("FUCHS", "🦊", "der"), ("KREBS", "🦀", "der"), ("REH", "🦌", "das"),
        # Essen
        ("EI", "🥚", "das"), ("MAIS", "🌽", "der"), ("KUCHEN", "🎂", "der"),
        ("MILCH", "🥛", "die"), ("REIS", "🍚", "der"), ("APFEL", "🍎", "der"),
        ("TRAUBE", "🍇", "die"), ("ZITRONE", "🍋", "die"), ("PIZZA", "🍕", "die"),
        ("BROT", "🍞", "das"), ("KEKS", "🍪", "der"), ("BANANE", "🍌", "die"),
        ("KIRSCHE", "🍒", "die"),
        # Haus und Objekte
        ("BETT", "🛏️", "das"), ("TASSE", "🥤", "die"), ("HUT", "🎩", "der"),
        ("BALL", "⚽", "der"), ("GLOCKE", "🔔", "die"), ("BUCH", "📖", "das"),
        ("TÜR", "🚪", "die"), ("LAMPE", "💡", "die"), ("SCHUH", "👟", "der"),
        ("STERN", "⭐", "der"), ("TROMMEL", "🥁", "die"), ("HAUS", "🏠", "das"),
        ("STUHL", "🪑", "der"), ("UHR", "🕐", "die"),
        # Natur
        ("SONNE", "☀️", "die"), ("MOND", "🌙", "der"), ("REGEN", "🌧️", "der"),
        ("BAUM", "🌳", "der"), ("BLATT", "🍃", "das"), ("WOLKE", "☁️", "die"),
        ("WASSER", "💧", "das"), ("BLUME", "🌸", "die"),
        # Fahrzeuge
        ("BUS", "🚌", "der"), ("AUTO", "🚗", "das"), ("BOOT", "⛵", "das"),
        ("ZUG", "🚂", "der"), ("RAKETE", "🚀", "die"), ("FAHRRAD", "🚲", "das"),
        ("FLUGZEUG", "✈️", "das"),
        # Körper und Menschen
        ("OHR", "👂", "das"), ("AUGE", "👁️", "das"), ("NASE", "👃", "die"),
        ("HAND", "✋", "die"), ("BABY", "👶", "das"), ("KÖNIG", "👑", "der"),
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
    "en": {"prompt": "Press:"},
    "es": {"prompt": "Pulsa:"},
    "de": {"prompt": "Drücke:"},
}

CELEBRATION_PHRASES = {
    "en": ["Great job!", "Awesome!", "Well done!", "You did it!", "Amazing!"],
    "es": ["¡Muy bien!", "¡Genial!", "¡Excelente!", "¡Lo lograste!", "¡Increíble!"],
    "de": ["Super gemacht!", "Toll!", "Gut gemacht!", "Klasse!", "Wunderbar!"],
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
    """Return a random (display_word, emoji, article) tuple for *lang*.

    *article* is the definite article (e.g. "der", "el") or ``None``
    for languages without gendered articles (English).
    """
    word_list = WORDS[lang]
    choices = word_list if exclude is None else [w for w in word_list if w[0] != exclude]
    entry = random.choice(choices)
    if len(entry) == 3:
        return entry
    return (entry[0], entry[1], None)


def get_celebration_phrase(lang="en"):
    """Return a random celebration phrase for *lang*."""
    return random.choice(CELEBRATION_PHRASES[lang])
