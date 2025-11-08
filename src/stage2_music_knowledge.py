# Genre → Example playlists (YouTube)
GENRE_PLAYLISTS = {
    "lofi": ["lofi hip hop radio", "lofi beats to relax/study to"],
    "jazz": ["jazz for study", "smooth jazz playlist"],
    "r&b": ["r&b slow jams", "modern r&b mix"],
    "rock": ["90s rock playlist", "classic rock hits"],
    "indie": ["indie vibes playlist", "indie chill mix"],
    "pop": ["top pop hits", "today's top hits mix"],
}

# Mood → Playlist keywords
MOOD_KEYWORDS = {
    "sad": "sad songs playlist",
    "chill": "chill vibes playlist",
    "hype": "party bangers playlist",
    "study": "focus lofi beats",
    "sleep": "calm sleep music",
    "romantic": "love songs playlist",
    "gym": "workout pump mix",
}

# --- Artist Knowledge Base ---

GENRE_TO_ARTISTS = {
    # --- INDIE / BEDROOM POP / SOFT ALT ---
    "indie": [
        "Phoebe Bridgers","Mitski","The 1975","Beabadoobee","Men I Trust","Clairo","Dayglow","Snail Mail",
        "Lucy Dacus","Julien Baker","Boygenius","Japanese Breakfast","Soccer Mommy","Faye Webster",
        "Still Woozy","Wallows","Peach Pit","Rex Orange County","Hippo Campus","Mac DeMarco",
        "Arctic Monkeys","The Strokes","Cigarettes After Sex","Lana Del Rey","Weyes Blood","Sufjan Stevens",
        "Hozier","Moses Sumney","Bon Iver","Fleet Foxes"
    ],

    # --- LOFI / CHILLHOP / STUDY VIBES ---
    "lofi": [
        "Lofi Girl","Mondo Loops","potsu","Kudasai","Aso","eevee","Jinsang","Idealism","Nymano",
        "Oatmello","Aiguille","Sleepdealer","Kendall Miles","Leavv","SwuM","Burbank","In Love With a Ghost"
    ],

    # --- K-POP / ASIAN POP ---
    "k-pop": [
        "NewJeans","IVE","LE SSERAFIM","TWICE","SEVENTEEN","Stray Kids","ITZY","aespa","BLACKPINK",
        "BTS","Jungkook","Jimin","Big Bang","Red Velvet","Taeyeon","NCT DREAM","TXT","G-IDLE",
        "STAYC","LOONA","BOL4","AKMU","Kep1er"
    ],

    # --- POP (Modern / Mainstream) ---
    "pop": [
        "Taylor Swift","Olivia Rodrigo","Dua Lipa","Sabrina Carpenter","The Weeknd","Billie Eilish",
        "Ariana Grande","Ed Sheeran","SZA","Miley Cyrus","Lady Gaga","Selena Gomez","Lorde","Troye Sivan",
        "Sam Smith","Conan Gray","Reneé Rapp","RAYE","Tate McRae","Carly Rae Jepsen","Ellie Goulding",
        "Halsey","Khalid","Chappell Roan","Gracie Abrams"
    ],

    # --- ROCK / ALT ROCK / BAND VIBES ---
    "rock": [
        "Nirvana","Arctic Monkeys","Red Hot Chili Peppers","Queen","AC/DC","Radiohead","The Strokes",
        "The Killers","Green Day","Paramore","Foo Fighters","Pearl Jam","Soundgarden","The Smashing Pumpkins",
        "The Rolling Stones","Pink Floyd","Led Zeppelin","Blur","The Cure","The Smiths","Muse","My Chemical Romance"
    ],

    # --- R&B / SOUL / SMOOTH / MOODY ---
    "r&b": [
        "SZA","Brent Faiyaz","Daniel Caesar","The Weeknd","Frank Ocean","Khalid","Kehlani","Summer Walker",
        "Jhené Aiko","Giveon","Cleo Sol","Lucky Daye","Omar Apollo","Steve Lacy","Raveena","Joy Crookes"
    ],

    # --- HIP-HOP / ALTERNATIVE RAP / VIBEY RAP ---
    "hip-hop": [
        "Kendrick Lamar","J. Cole","Travis Scott","Tyler, The Creator","Baby Keem","A$AP Rocky","21 Savage",
        "Playboi Carti","Lil Uzi Vert","Joey Bada$$","JID","Denzel Curry","Earl Sweatshirt","Anderson .Paak",
        "Smino","Noname","Amine","Mac Miller","Cordae","Westside Boogie"
    ],

    # --- CITY POP / J-POP / VINTAGE ASIAN GROOVE ---
    "city pop": [
        "Miki Matsubara","Mariya Takeuchi","Anri","Tatsuro Yamashita","Taeko Ohnuki","Lamp","Fujii Kaze",
        "Vaundy","Aimer","Hikaru Utada","YOASOBI","King Gnu","Wednesday Campanella"
    ],

    # --- CHILL / ROMANTIC / LATE NIGHT (CROSS-GENRE) ---
    "chill": [
        "Joji","Laufey","Cigarettes After Sex","Daniel Caesar","Rex Orange County","Faye Webster",
        "Khalid","Raveena","Sufjan Stevens","Kacey Musgraves","Clairo","Men I Trust"
    ],

    # --- GYM / HYPE / ENERGY ---
    "hype": [
        "Travis Scott","21 Savage","Don Toliver","Drake","Central Cee","Lil Uzi Vert","Dua Lipa","Doja Cat",
        "Stray Kids","SEVENTEEN","BLACKPINK","The Weeknd","Skrillex","David Guetta"
    ]
}


# Quick Artist Similarity Map (expandable later)
SIMILAR_ARTISTS = {
    "SZA": ["Summer Walker", "Kehlani", "Jhené Aiko"],
    "Phoebe Bridgers": ["Lucy Dacus", "Julien Baker", "Boygenius"],
    "Laufey": ["Norah Jones", "Beabadoobee", "Faye Webster"],
    "Arctic Monkeys": ["The Strokes", "The 1975", "Wallows"],
    "Joji": ["Keshi", "DPR Ian", "Cigarettes After Sex"],
}

# Mood → Genre Mappings
MOOD_TO_GENRE = {
    "sad": "indie",
    "chill": "lofi",
    "study": "lofi",
    "hype": "rock",
    "romantic": "r&b",
    "gym": "rock",
}