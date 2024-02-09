"""This should get a list of Anime objects and generate a static overview site 
with the Anime Title, Picture and a list of episode links for each anime in a grid."""

import logging
from anime_interface import Anime

logger = logging.getLogger(__name__)


# EXAMPLE Anime object:
# Title: "Shin no Nakama ja Nai ... | Banished from the Hero\u2019s Party"
# Cover: https://bs.to//public/images/cover/7993.jpg
# Anime Base URL: https://bs.to/serie/Shin-no-Nakama-ja-Nai-Banished-from-the-Hero-s-Party
# Episode_List:
# - Title1: https://bs.to/serie/Shin-no-Nakama-ja-Nai-Banished-from-the-Hero-s-Party/2/5-The-Man-Who-Doesn-t-Get-Chill-Living/des
# - Title2: https://bs.to/serie/Shin-no-Nakama-ja-Nai-Banished-from-the-Hero-s-Party/2/4-The-Red-String-of-Fate/des

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
            .anime-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
                align-items: start;
                justify-items: center;
            }
            .episode-list {
                text-align: center;
                padding-top: 20px;
                padding-bottom: 10px;
                display: flex;
                flex-direction: column;

            }
            .anime_title {
                height: 50px;
                text-align: center;
                color: white;
                overflow: hidden;
            }
            h1 {
                text-align: center;
                text-decoration: underline;
                color: orange;
                font-size: 40px;
                text-shadow: 0px 0px 5px darkorange;
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
                color: orange;
                text-decoration: none;
                margin: 5px;
            }

            .episode-list a:hover {
                color: gold;
            }

            .episode-list a:visited {
                color: darkred;
            }
        </style>
    </head>
    <body>
    """

    html = (
        head
        + """
    <h1>Anime Overview</h1>
    <div class="anime-grid">
    """
    )

    # a episode obj has title and episode_url
    for anime in anime_list:
        html += f"""
        <div class="anime">
            <h2 class=anime_title><a class=anime_title href="{anime.series_url}">{anime.title}</a></h2>
            <a href="{anime.series_url}"><img src="{anime.cover_url}" alt="{anime.title}"></a>
            <div class="episode-list">
                {"".join(f'<a href="{episode.url}">{episode.title}</a>' for episode in anime.episode_list)}
            </div> <!-- episode-list -->
        </div> <!-- anime -->
        """

    html += """
    </div> <!-- anime-grid -->
    </body>
    </html>
    """

    with open("/tmp/anime_overview.html", "w", encoding="utf-8") as file:
        file.write(html)
        logger.info("The static site has been generated successfully")

    return "/tmp/anime_overview.html"
