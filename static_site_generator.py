"""This should get a list of Anime objects and generate a static overview site 
with the Anime Title, Picture and a list of episode links for each anime in a grid."""

import logging
from anime_interface import Anime

logger = logging.getLogger(__name__)


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
            }
            .anime-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 30px;
                padding: 20px;
                align-items: start;
                justify-items: center;
            }
            .episode-list {
                text-align: center;
                margin-top: 20px;
                height: 100px;
                width: 200px;
                overflow-y: auto;
                scrollbar-width: thin;
                scrollbar-color: darkorange transparent;
                backdrop-filter: brightness(0.65);
                border-radius: 10px;
                padding: 10px;
            }
            .anime_title {
                display: -webkit-box;
                -webkit-box-orient: vertical;
                -webkit-line-clamp: 2;
                word-wrap: break-word;
                width: 200px;
                text-align: center;
                color: white;
                overflow: hidden;
            }
            .title_wrapper {
                margin-bottom: 10px;
                height: 90px;
            }
            h1 {
                text-align: center;
                text-decoration: underline;
                color: orange;
                font-size: 40px;
                text-shadow: 0px 0px 5px darkorange;
            }
            img {
                width: 180px;
                height: 250px;
                object-fit: cover;
                border-radius: 10px;
            }
            a {
                color: orange;
                text-decoration: none;
            }
            .episode-list a:hover {
                color: gold;
            }
            .episode-list a:visited {
                color: darkred;
            }
            .ep-link {
                display: block;
                font-size: 1em;
                height: 1.2em;
                overflow: hidden;
                margin-left: 3px;
                margin-bottom: 3px;
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
            <div class=title_wrapper>
                <h2 class=anime_title><a class=anime_title href="{anime.series_url}">{anime.title}</a></h2>
            </div>
            <a href="{anime.series_url}"><img src="{anime.cover_url}" alt="{anime.title}"></a>
            <div class="episode-list">
                {"".join(f'<a class="ep-link" href="{episode.url}">{episode.title}</a>' for episode in anime.episode_list)}
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
