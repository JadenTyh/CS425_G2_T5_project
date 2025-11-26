# import requests
# import os
# import re
# from random import choice as choose 

# def get_omdb_api_key():
#     # Try Streamlit secrets, then env var
#     try:
#         import streamlit as st
#         return st.secrets.get("OMDB_API_KEY", None)
#     except Exception:
#         return os.getenv("OMDB_API_KEY")

# OMDB_API_KEY = get_omdb_api_key()

# def extract_creative_work_title(query):
#     """
#     Extract likely creative work title from a user's query.
#     Returns the extracted title or None.
#     """
#     query = query.lower().strip()
#     # Try match quoted substring
#     quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', query)
#     if quoted:
#         return next(q for q in quoted[0] if q)
#     # Common trigger words: 'find', 'show', 'search', 'get'
#     trigger = re.search(r'(find|show|search|get|describe)\s+(.*)', query)
#     if trigger:
#         possible_title = trigger.group(2)
#         # Remove generic followups
#         possible_title = re.sub(r'for|about|some creative work|a creative work', '', possible_title).strip()
#         # Remove extra whitespace and trailing punctuation
#         possible_title = re.sub(r'\s+', ' ', possible_title).strip(' .!?')
#         if possible_title:
#             return possible_title
#     # If "creative work" is followed by something, try that
#     after_cw = re.search(r'creative work\s+(.*)', query)
#     if after_cw:
#         possible_title = after_cw.group(1).strip(' .!?')
#         if possible_title:
#             return possible_title
#     return None

# def search_creative_work(user_query):
#     """
#     Handler: Extracts title from user query then searches for a movie using OMDb API.
#     """
#     if not OMDB_API_KEY:
#         return "OMDb API key not set. Please add OMDB_API_KEY to .streamlit/secrets.toml."
#     title = extract_creative_work_title(user_query)
#     if not title:
#         return ("Hey dude, I couldn't figure out what creative work you meant man. "
#                 "Please specify with a title, e.g. 'Find \"Guardians of the Galaxy Vol. 2\"'.")

#     url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
#     resp = requests.get(url)
#     if resp.status_code != 200:
#         return "Error contacting OMDb API."
#     data = resp.json()
#     if data.get("Response") == "False":
#         return choose(
#                 [ # Giving varied responses with a 'moody tenager characteristic' for no results found
#                     f"Well too bad 🙅, no creative work found for '**{title}**'.",
#                     f"no creative work found for '**{title}**'. Oh well 🤷",
#                     f'no creative work found for '**{title}**'. Such is life 🤷',
#                     f'no creative work found for '**{title}**'. We do not get what we want in life do we 🤷',
#                     f'no creative work found for '**{title}**'. If only life was simpler 😤'
#                 ]
#             )

#     # Compose detailed info using the API response
#     msg = (
#         f"**{data.get('Title','Unknown')}** ({data.get('Year','N/A')})\n"
#         f"Genre: {data.get('Genre','N/A')}\n"
#         f"Rated: {data.get('Rated','N/A')} • Released: {data.get('Released','N/A')} • Runtime: {data.get('Runtime','N/A')}\n"
#         f"Director: {data.get('Director','N/A')}\n"
#         f"Actors: {data.get('Actors','N/A')}\n"
#         f"IMDb Rating: {data.get('imdbRating','N/A')}\n\n"
#         f"**Plot:** {data.get('Plot','No plot available.')}\n"
#     )
#     poster = data.get('Poster', None)
#     if poster and poster != "N/A":
#         msg += f"\n![Poster]({poster})"
#     moody_teen_starting_msg = choose(
#         [ # Giving varied responses with a 'moody tenager characteristic' for no results found
#             f"Have fun man\n",
#             f"Maybe check it out together with your boyfriend or girlfriend 😉\n",
#             f"Well enjoy your time watching it 🍿\n",
#             f"Here you go dude\n",
#         ]
#     )
#     return moody_teen_starting_msg + msg