"""This should get a list of Anime objects and generate a static overview site 
with the Anime Title, Picture and a list of episode links for each anime in a grid."""

import logging
from anime_interface import Anime

logger = logging.getLogger(__name__)


# EXAMPLE Anime object:
# Title: "Shin no Nakama ja Nai ... | Banished from the Hero\u2019s Party"
# Cover: https://bs.to//public/images/cover/7993.jpg
# Episode_List:
# - https://bs.to/serie/Shin-no-Nakama-ja-Nai-Banished-from-the-Hero-s-Party/2/5-The-Man-Who-Doesn-t-Get-Chill-Living/des
# - https://bs.to/serie/Shin-no-Nakama-ja-Nai-Banished-from-the-Hero-s-Party/2/4-The-Red-String-of-Fate/des

# The Page has a Dark Theme


def generate_static_site(anime_list: list[Anime]) -> str:
    """Generate a static site with the anime details"""

    head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Anime Overview</title>
        <style>
            body {
                background-color: #1d1d1d;
                color: white;
                font-family: Arial, sans-serif;
            }
            .anime {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: 20px;
            }
            h2 {
                margin-bottom: 10px;
            }
            img {
                width: 200px;
                height: 300px;
                object-fit: cover;
                border-radius: 10px;
            }
            a {
                color: white;
                text-decoration: none;
                margin: 5px;
            }
        </style>
    </head>
    <body>
    """

    html = head + """
    <h1>Anime Overview</h1>
    """

    for anime in anime_list:
        html += f"""
        <div class="anime">
            <h2>{anime.title}</h2>
            <img src="{anime.cover_url}" alt="{anime.title}">
            <div>
                {"".join(f'<a href="{episode}">Link: {episode}</a><br>' for episode in sorted(anime.episode_list))}
            </div>
        </div>
        """

    html += """
    </body>
    </html>
    """

    with open("/tmp/anime_overview.html", "w", encoding="utf-8") as file:
        file.write(html)
        logger.info("The static site has been generated successfully")

    return "/tmp/anime_overview.html"
