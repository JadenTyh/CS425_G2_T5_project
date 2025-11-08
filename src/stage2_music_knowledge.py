# Genre → Example playlists (YouTube)
GENRE_PLAYLISTS = {
    "lofi": [
        "lofi hip hop radio", "lofi beats to relax/study to", "lofi sleep mix",
        "late night lofi", "japanese lofi", "calm lofi chillhop", "rainy day lofi",
        "cozy bedroom lofi", "coffee shop lofi", "lofi jazzhop mix", "sad lofi",
        "deep focus lofi", "soothing lofi piano", "chillhop essentials", "midnight study lofi"
    ],

    "jazz": [
        "smooth jazz playlist", "jazz for study", "late night jazz bar ambience",
        "rainy jazz cafe", "bossa nova jazz playlist", "jazz piano chill",
        "quiet jazz night", "90s jazz mix", "romantic jazz classics", "soft sax jazz",
        "elegant dinner jazz", "jazz for reading", "cozy cafe jazz", "sunday brunch jazz"
    ],

    "r&b": [
        "r&b slow jams", "modern r&b mix", "late night r&b", "moody r&b",
        "sad r&b playlist", "soulful r&b vocals", "neo-soul essentials",
        "bedroom r&b", "smooth r&b chill", "dark r&b vibe", "sexy slow r&b",
        "heartbreak r&b", "quiet storm r&b", "r&b deep cuts"
    ],

    "rock": [
        "90s rock playlist", "classic rock hits", "indie rock vibes",
        "alternative rock bangers", "garage rock revival", "post-punk essentials",
        "grunge anthems", "rock for gym", "soft rock chill", "emotional rock",
        "late night road trip rock", "melancholic indie rock", "punk rock classics"
    ],

    "indie": [
        "indie vibes playlist", "indie chill mix", "indie acoustic cozy",
        "sad indie songs", "cute indie bedroom pop", "indie cafe music",
        "rainy indie mix", "sleepy indie playlist", "indie love songs",
        "late-night indie vibe", "sad girl indie", "indie slow dance playlist",
        "warm indie folk", "indie guitar chill", "indie daydreaming playlist"
    ],

    "pop": [
        "today's top hits", "pop trending playlist", "soft pop chill",
        "sad pop girl vibes", "uplifting pop mix", "sleepy pop",
        "dance pop bangers", "late night pop aesthetic", "melancholy pop",
        "acoustic pop stripped", "romantic pop songs", "viral tiktok pop"
    ],

    "k-pop": [
        "k-pop best hits", "k-pop chill b-sides", "k-pop sad songs",
        "k-pop dance practice bangers", "k-pop soft vocals", "k-band live session",
        "k-drama ost playlist", "k-pop aesthetic mix", "k-pop indie playlist"
    ],

    "hip-hop": [
        "chill hip hop beats", "trap bangers playlist", "90s hip hop classics",
        "emotional rap", "lofi hip hop", "melodic rap playlist", "alternative rap vibes",
        "gym trap playlist", "rage trap mix", "late-night rap storytelling"
    ],

    "city pop": [
        "city pop classics", "japanese city pop night drive", "retro asian pop vibes",
        "future funk mix", "vaporwave city pop remix", "nostalgic summer city pop"
    ]
}


# Mood → Playlist keywords
MOOD_KEYWORDS = {
    "sad": "sad songs playlist",
    "heartbroken": "heartbreak songs playlist",
    "crying": "emotional cry playlist",
    "lonely": "songs that feel like being alone at night",
    "chill": "chill vibes playlist",
    "soft": "soft cozy bedroom pop",
    "sleep": "sleepy calm music",
    "study": "deep focus study music",
    "relax": "relaxing ambient playlist",
    "cozy": "warm cozy music like a rainy cafe",
    "romantic": "love songs playlist",
    "in love": "soft romantic guitar playlist",
    "hype": "party bangers playlist",
    "confident": "power walk hot girl playlist",
    "gym": "workout pump mix",
    "aggressive": "rage trap gym playlist",
    "driving": "night drive aesthetic playlist",
    "late night": "late night slow playlist",
    "sunset": "golden hour aesthetic playlist",
    "coffee": "coffee shop background mix",
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
    # --- INDIE / BEDROOM POP ---
    "Phoebe Bridgers": ["Lucy Dacus", "Julien Baker", "Boygenius", "Soccer Mommy", "Snail Mail"],
    "Mitski": ["Japanese Breakfast", "Weyes Blood", "Faye Webster", "Big Thief", "Adrienne Lenker"],
    "Clairo": ["Beabadoobee", "Girl in Red", "Laufey", "Men I Trust", "Rex Orange County"],
    "Beabadoobee": ["Clairo", "Soccer Mommy", "Snail Mail", "Phoebe Bridgers", "Laufey"],
    "Men I Trust": ["Still Woozy", "Crumb", "Mild High Club", "Mac DeMarco", "Barrie"],
    "Laufey": ["Norah Jones", "Lana Del Rey", "Beabadoobee", "Faye Webster", "Lizzy McAlpine"],
    "Lana Del Rey": ["Weyes Blood", "Florence + The Machine", "Lorde", "Mazzy Star", "Cigarettes After Sex"],
    "Cigarettes After Sex": ["Joji", "The xx", "Beach House", "Mazzy Star", "Ricky Eat Acid"],

    # --- ALT / INDIE BANDS ---
    "Arctic Monkeys": ["The Strokes", "The 1975", "Wallows", "Cage the Elephant", "The Neighbourhood"],
    "The 1975": ["Arctic Monkeys", "The Japanese House", "LANY", "Wallows", "COIN"],
    "Wallows": ["Hippo Campus", "The Backseat Lovers", "The 1975", "Dayglow", "Peach Pit"],
    "Peach Pit": ["Hippo Campus", "Dayglow", "Rex Orange County", "Still Woozy", "Mac DeMarco"],
    "Mac DeMarco": ["Mild High Club", "Men I Trust", "King Krule", "Rex Orange County", "Boy Pablo"],

    # --- R&B / SOUL ---
    "SZA": ["Summer Walker", "Kehlani", "Jhené Aiko", "Cleo Sol", "H.E.R."],
    "Daniel Caesar": ["Frank Ocean", "Omar Apollo", "Steve Lacy", "Brent Faiyaz", "Giveon"],
    "Frank Ocean": ["Daniel Caesar", "SZA", "Tyler, The Creator", "Blood Orange", "Kali Uchis"],
    "Brent Faiyaz": ["The Weeknd", "PARTYNEXTDOOR", "dvsn", "Giveon", "6LACK"],
    "Steve Lacy": ["Blood Orange", "Tyler, The Creator", "Omar Apollo", "Rex Orange County", "Faye Webster"],

    # --- CHILL / SOFT POP ---
    "Joji": ["Keshi", "DPR Ian", "Cigarettes After Sex", "RINI", "Sycco"],
    "Keshi": ["Joji", "Laufey", "DPR IAN", "RINI", "Jeremy Zucker"],
    "Jeremy Zucker": ["Chelsea Cutler", "Alexander 23", "Lauv", "Conan Gray", "Shallou"],
    "Lorde": ["Lana Del Rey", "Florence + The Machine", "Gracie Abrams", "Girl in Red", "Holly Humberstone"],

    # --- POP / GIRLPOP / MODERN ---
    "Taylor Swift": ["Gracie Abrams", "Olivia Rodrigo", "Phoebe Bridgers", "Lorde", "Sabrina Carpenter"],
    "Olivia Rodrigo": ["Gracie Abrams", "Tate McRae", "Sabrina Carpenter", "Conan Gray", "Nessa Barrett"],
    "Sabrina Carpenter": ["Chappell Roan", "Olivia Rodrigo", "Maisie Peters", "Reneé Rapp", "Tate McRae"],
    "Gracie Abrams": ["Phoebe Bridgers", "Lizzy McAlpine", "Olivia Rodrigo", "Holly Humberstone", "Lorde"],

    # --- ROCK / ALT / CLASSICS ---
    "Radiohead": ["The Smashing Pumpkins", "The Cure", "The Strokes", "Interpol", "Joy Division"],
    "The Strokes": ["Arctic Monkeys", "The Libertines", "The Killers", "Franz Ferdinand", "Metric"],
    "Paramore": ["Fall Out Boy", "My Chemical Romance", "PVRIS", "Tonight Alive", "Hayley Williams"],

    # --- HIP-HOP / ALT RAP ---
    "Tyler, The Creator": ["Earl Sweatshirt", "Steve Lacy", "Frank Ocean", "Smino", "Childish Gambino"],
    "Kendrick Lamar": ["J. Cole", "Childish Gambino", "Anderson .Paak", "Saba", "Denzel Curry"],
    "Joey Bada$$": ["Saba", "Mick Jenkins", "JID", "Denzel Curry", "Isaiah Rashad"],

    # --- CITY POP / J-POP ---
    "Miki Matsubara": ["Mariya Takeuchi", "Tatsuro Yamashita", "Anri", "Taeko Ohnuki", "Yumi Matsutoya"],
    "Lamp": ["Fishmans", "Lily Chou-Chou", "Vaundy", "Cö Shu Nie", "Hitsujibungaku"],
}


# Mood → Genre Mappings
MOOD_TO_GENRE = {
    "sad": "indie",
    "heartbroken": "indie",
    "lonely": "indie",
    "chill": "lofi",
    "study": "lofi",
    "sleep": "lofi",
    "romantic": "r&b",
    "soft": "r&b",
    "late night": "chill",
    "night drive": "chill",
    "hype": "hip-hop",
    "party": "pop",
    "gym": "rock",
    "angry": "rock",
}
