# Generates a large synthetic dataset for Stage 1.5 music sub-intents
# Tone: mix of casual (B) + gen-z (C)
# Classes: play_track, recommend_genre, recommend_artist, play_mood

import json, os, random

OUT_PATH = os.path.join("data", "music_subintent_train.json")
os.makedirs("data", exist_ok=True)

random.seed(42)

# --- Artist pools (mixed categories) ---
# --- Artist pools (mixed categories) ---
# --- Modern Pop / Mainstream (2015–2025) ---
pop_artists = [
    "Taylor Swift","The Weeknd","Billie Eilish","Olivia Rodrigo","Dua Lipa","Ariana Grande","Ed Sheeran",
    "Drake","Sabrina Carpenter","Tate McRae","Charlie Puth","Shawn Mendes","Justin Bieber","Camila Cabello",
    "Selena Gomez","Troye Sivan","SZA","Halsey","Lana Del Rey","Khalid","Miley Cyrus","Lady Gaga","Rihanna",
    "Beyoncé","Sam Smith","Rosalía","Conan Gray","Niall Horan","ZAYN","Meghan Trainor","Ava Max","Ellie Goulding",
    "Tori Kelly","Jessie J","Julia Michaels","Noah Kahan","Tove Lo","Sigrid","Bebe Rexha","Anne-Marie","Kacey Musgraves",
    "Tori Amos","Alec Benjamin","Lewis Capaldi","Ben Platt","Ari Abdul","Raye","Pink","Kehlani","Sabrina Claudio",
    "Carly Rae Jepsen","Zara Larsson"
]


# --- Gen-Z / Viral / TikTok artists (2020–2025) ---
viral_artists = [
    "PinkPantheress","Ice Spice","Doja Cat","Rema","Reneé Rapp","Stephen Sanchez","JVKE","GAYLE","Ruth B.",
    "Gracie Abrams","Laufey","Benson Boone","Bella Poarch","Ayesha Erotica","Chappell Roan","Lizzy McAlpine",
    "mxmtoon","Conan Gray","Noah Kahan","Bea Miller","Armani White","Peggy Gou","New West","Kali Uchis",
    "d4vd","Joji","Keshi","JNR Choi","Yung Gravy","Lil Peep","BoyWithUke","Iann Dior","iann dior","Riovaz",
    "Sophie Cates","Ericdoa","Glaive","Midwxst","Tyla","Jazmin Bean","Lay Bankz","Jersey Club Mafia",
    "JP Saxe","Mimi Webb","Sody","Jeremy Zucker","Chelsea Cutler","Lily Rose","Mae Stephens","Alex G","Lauren Spencer Smith"
]


# --- K-pop / J-pop / Asian pop ---
kpop_artists = [
    "BTS","Jungkook","V","RM","Jimin","BLACKPINK","Lisa","Jennie","Rose","Jisoo","NewJeans","IVE",
    "LE SSERAFIM","aespa","ITZY","TWICE","Stray Kids","SEVENTEEN","NCT DREAM","ATEEZ","TREASURE",
    "Red Velvet","BIGBANG","Taeyeon","EXO","SHINee","IU","Sunmi","HyunA","LOONA","(G)I-DLE",
    "STAYC","fromis_9","Kep1er","EVERGLOW","Oh My Girl","MAMAMOO","BOL4","AKMU","CRAVITY","Enhypen",
    "ZEROBASEONE","Billlie","The Boyz","VIXX","GOT7","DAY6","KARD","MONSTA X","Dreamcatcher"
]


jpop_artists = [
    "YOASOBI","Kenshi Yonezu","Fujii Kaze","Vaundy","King Gnu","Aimer","LiSA","Uru","RADWIMPS",
    "Hikaru Utada","Ado","Yorushika","Eve","Kikuo","Ryokuoushoku Shakai","ZUTOMAYO","Wednesday Campanella",
    "Mafumafu","Reol","kradness","Official HIGE DANDism","Aimyon","Nana Mizuki","GARNiDELiA",
    "Yui","Scandal","FLOW","Kokia","Yoko Kanno","Utada Hikaru","Queen Bee","Kana Hanazawa","Kumi Koda",
    "AAA","Asian Kung-Fu Generation","The Pillows","Polkadot Stingray","Lamp","Ichiko Aoba","Judy and Mary",
    "Perfume","Capsule","Daoko","Toshiki Kadomatsu","Taeko Ohnuki","Mariya Takeuchi","Tatsuro Yamashita",
    "Miki Matsubara","Anri","Aran","Jin"
]


# --- Indie / Alternative / Bedroom pop ---
indie_artists = [
    "Arctic Monkeys","The 1975","Mitski","Phoebe Bridgers","Beabadoobee","Snail Mail","Clairo","Japanese Breakfast",
    "Lucy Dacus","Julien Baker","Sufjan Stevens","Lana Del Rey","Florence + The Machine","Boygenius","Cigarettes After Sex",
    "Men I Trust","Rex Orange County","Dayglow","Wallows","Beach Bunny","Vacations","Tame Impala","Mac DeMarco",
    "The Strokes","Paramore","Car Seat Headrest","Soccer Mommy","Hippo Campus","Cannons","Tamino","Duster","Alex G",
    "Weyes Blood","Pierce the Veil","Hozier","Wilbur Soot","Sir Chloe","Peach Pit","Moses Sumney","Andrew Bird",
    "Glass Animals","Wet Leg","Still Woozy","Bad Suns","Gorillaz","The National","TV Girl","Foster the People","Local Natives"
]


# --- Hip-Hop / R&B / Trap (modern) ---
hiphop_artists = [
    "Kendrick Lamar","J. Cole","Travis Scott","Tyler, The Creator","21 Savage","Drake","SZA","Frank Ocean",
    "Playboi Carti","Lil Uzi Vert","Don Toliver","Metro Boomin","Baby Keem","A$AP Rocky","Kanye West","Kid Cudi",
    "Post Malone","Bryson Tiller","Summer Walker","Chase Shakur","JID","Doja Cat","Lil Nas X","Jack Harlow",
    "Central Cee","Loyle Carner","Denzel Curry","Joey Bada$$","Cordae","Logic","Freddie Gibbs","Anderson .Paak",
    "Brent Faiyaz","Giveon","Daniel Caesar","Aminé","Tory Lanez","EST Gee","Young Thug","Gunna","Megan Thee Stallion",
    "Latto","Ice Spice","Flo Milli","Offset","Quavo","Future","NAV","Lil Baby","Chief Keef"
]


# --- Classic / Legends / Evergreen ---
classic_artists = [
    "Queen","AC/DC","The Beatles","The Rolling Stones","Elton John","Billy Joel","David Bowie","Nirvana",
    "Fleetwood Mac","Red Hot Chili Peppers","Metallica","Led Zeppelin","Pink Floyd","Eagles","Bon Jovi",
    "Aerosmith","Guns N' Roses","Bruce Springsteen","Radiohead","U2","Journey","Lynyrd Skynyrd","The Police",
    "The Beach Boys","The Doors","Heart","Deep Purple","Cream","The Who","Chicago","Genesis","Rush",
    "Pearl Jam","Soundgarden","Stone Temple Pilots","REM","The Clash","The Smiths","Depeche Mode","Talking Heads",
    "The Cure","Dire Straits","Blue Öyster Cult","Whitesnake","Def Leppard","Iron Maiden","KISS","Stevie Wonder",
    "Prince","Bob Dylan"
]


# COMBINE ALL
ARTISTS = (
    pop_artists
    + viral_artists
    + kpop_artists
    + jpop_artists
    + indie_artists
    + hiphop_artists
    + classic_artists
)


# --- Genres & moods ---
GENRES = [
    "lofi",
    "jazz",
    "k-pop",
    "indie",
    "classical",
    "edm",
    "house",
    "rock",
    "r&b",
    "hip hop",
    "city pop",
    "phonk",
    "synthwave",
    "j-pop",
    "acoustic",
    "latin",
    "afrobeats",
    "metal",
    "punk",
    "folk",
]
MOODS = [
    "chill",
    "sad",
    "hype",
    "focus",
    "study",
    "gym",
    "sleep",
    "romantic",
    "rainy day",
    "feel-good",
    "throwback",
    "late-night",
    "roadtrip",
    "party",
    "deep work",
    "cozy",
    "sunset",
    "gaming",
    "meditation",
    "morning boost",
]

# --- Helper pools for phrasing (B/C tone) ---
REQ_PLAY = [
    "play",
    "put on",
    "spin",
    "queue up",
    "blast",
    "throw on",
    "run",
    "drop",
    "fire up",
]
REQ_RECO = [
    "recommend",
    "suggest",
    "hook me up with",
    "hit me with",
    "i need",
    "put me on some",
    "drop me a",
]
SUFFIX = [
    "",
    " pls",
    " please",
    " rn",
    " right now",
    " asap",
    " fr",
    " lowkey",
    " highkey",
    " tbh",
]
PLATFORM_HINT = [
    "",
    " on youtube",
    " on spotify",
    " on yt",
    " on spof",
    " (yt)",
    " (spotify)",
]


def pick(xs):
    return random.choice(xs)


def make_play_track(n=600):
    out = []
    for _ in range(n):
        a = pick(ARTISTS)
        # Lightly bias some famous tracks (not exhaustive; classifier only needs phrasing)
        track_templates = [
            f"{pick(REQ_PLAY)} 'Blinding Lights' by The Weeknd",
            f"{pick(REQ_PLAY)} 'lovely' by Billie Eilish",
            f"{pick(REQ_PLAY)} 'Love Story' by Taylor Swift",
            f"{pick(REQ_PLAY)} 'drivers license' by Olivia Rodrigo",
            f"{pick(REQ_PLAY)} 'As It Was' by Harry Styles",
            f"{pick(REQ_PLAY)} 'bad guy' by Billie Eilish",
            f"{pick(REQ_PLAY)} '{pick(['After Dark','SLOW DANCING IN THE DARK','Always','Some'])}' by {pick(['Mr.Kitty','Joji','Cigarettes After Sex','Arctic Monkeys'])}",
            f"{pick(REQ_PLAY)} '{pick(['Seven','Dynamite','Butter'])}' by {pick(['Jungkook','BTS'])}",
            f"{pick(REQ_PLAY)} a track by {a}",
            f"{pick(REQ_PLAY)} something by {a}",
            f"{pick(REQ_PLAY)} {a}'s latest",
            f"{pick(REQ_PLAY)} {a} top hit",
            f"{pick(REQ_PLAY)} 'Bohemian Rhapsody' by Queen",
            f"{pick(REQ_PLAY)} 'Hotel California' by Eagles",
            f"{pick(REQ_PLAY)} 'Take On Me' by a-ha",
            f"{pick(REQ_PLAY)} 'Dancing Queen' by ABBA",
            f"{pick(REQ_PLAY)} 'Yellow Submarine' by The Beatles",
            f"{pick(REQ_PLAY)} 'Back In Black' by AC/DC",
            f"{pick(REQ_PLAY)} 'Space Oddity' by David Bowie",
            f"{pick(REQ_PLAY)} 'Under the Bridge' by Red Hot Chili Peppers",
            f"{pick(REQ_PLAY)} 'Smells Like Teen Spirit' by Nirvana",
            f"{pick(REQ_PLAY)} 'Livin’ On a Prayer' by Bon Jovi",
            f"{pick(REQ_PLAY)} something from old-school rock",
            f"{pick(REQ_PLAY)} some classic hits rn",
        ]
        t = pick(track_templates) + pick(SUFFIX)
        out.append({"text": t, "label": "play_track"})
    return out


def make_recommend_genre(n=600):
    out = []
    for _ in range(n):
        g = pick(GENRES)
        templates = [
            f"{pick(REQ_RECO)} {g} playlist",
            f"{pick(REQ_RECO)} some {g} tracks",
            f"{pick(REQ_RECO)} a {g} mix",
            f"{pick(REQ_RECO)} {g} songs{pick(PLATFORM_HINT)}",
            f"{pick(['need','want'])} {g} vibes{pick(SUFFIX)}",
            f"what {g} should i listen to",
            f"drop {g} recs{pick(SUFFIX)}",
            f"put me on {g} bangers",
        ]
        out.append({"text": pick(templates), "label": "recommend_genre"})
    return out


def make_recommend_artist(n=600):
    out = []
    for _ in range(n):
        a = pick(ARTISTS)
        templates = [
            f"{pick(REQ_RECO)} songs like {a}",
            f"{pick(REQ_RECO)} artists similar to {a}",
            f"{pick(REQ_RECO)} a mix like {a}",
            f"{pick(['need','want'])} tracks similar to {a}{pick(SUFFIX)}",
            f"if i like {a}, what should i play",
            f"who sounds like {a}{pick(SUFFIX)}",
            f"anything like {a} {pick(PLATFORM_HINT)}",
        ]
        out.append({"text": pick(templates), "label": "recommend_artist"})
    return out


def make_play_mood(n=600):
    out = []
    for _ in range(n):
        m = pick(MOODS)
        templates = [
            f"{pick(REQ_PLAY)} {m} music",
            f"{pick(REQ_PLAY)} {m} playlist",
            f"{pick(REQ_RECO)} {m} vibes{pick(SUFFIX)}",
            f"{pick(['need','want'])} songs for {m}{pick(SUFFIX)}",
            f"music for {m} pls",
            f"hit me with a {m} mix",
            f"{pick(REQ_PLAY)} something {m}{pick(PLATFORM_HINT)}",
        ]
        out.append({"text": pick(templates), "label": "play_mood"})
    return out


dataset = []
dataset += make_play_track(650)  # 650
dataset += make_recommend_genre(650)  # 650
dataset += make_recommend_artist(650)  # 650
dataset += make_play_mood(650)  # 650
random.shuffle(dataset)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(dataset)} examples to {OUT_PATH}")
print(
    "Class counts:",
    {
        c: sum(1 for d in dataset if d["label"] == c)
        for c in ["play_track", "recommend_genre", "recommend_artist", "play_mood"]
    },
)
