"""The plugin for the website bs.to"""

import logging
from bs4 import BeautifulSoup
import requests
from anime_interface import Anime, AnimeInterface

# extend/implement the AnimeInterface
logger = logging.getLogger(__name__)


class AnimePlugin(AnimeInterface):
    """The interface for the anime details"""

    def login(self, username, password):
        """Login to the website"""
        raise NotImplementedError("BS.to plugin currently does not support login")

    def get_anime_from_url(self, url) -> Anime:
        """Get the episodes from all seasons that are unwatched"""

        base_url = self.get_base_url(url)

        # Get the page
        page = requests.get(url, timeout=5, headers=self.extra_headers)

        # check if the page was fetched successfully
        assert page.status_code == 200, f"The page could not be fetched for the url: {url}"
        soup = BeautifulSoup(page.content, "html.parser")

        new_episode_links = []

        seasons = soup.find("div", class_="seasons")
        assert seasons, f"No seasons found for the anime: {url}, pls report this issue"

        # find child with li class that without watched
        for season in seasons.find("div", id="seasons").find_all("li"):
            if "watched" in season["class"]:
                continue

            # New season found
            season_url = base_url + season.find("a")["href"]
            new_episode_links.extend(self.get_season_episodes(season_url))

        logger.debug("The new episodes for the anime are: %s", new_episode_links)

        # Get Title of the anime
        title = soup.find("div", id="sp_left").find("h2").text.strip().split("\n")[0]
        cover_image = base_url + soup.find("div", id="sp_right").find("img")["src"]

        return Anime(title, cover_image, set(new_episode_links))

    def get_season_episodes(self, url):
        """Get the anime details from the website"""
        base_url = self.get_base_url(url)

        # Get the page
        page = requests.get(url, timeout=5, headers=self.extra_headers)

        # check if the page was fetched successfully
        assert page.status_code == 200, f"The page could not be fetched for the url: {url}"
        soup = BeautifulSoup(page.content, "html.parser")

        new_episode_links = []

        episodes = soup.find("table", class_="episodes")
        assert episodes, f"No episodes in current season for the anime: {url}"

        for ep in episodes.find_all("tr"):  # Check if the episode is watched
            if ep["class"] == ["watched"]:
                continue

            new_episode_links.append(base_url + ep.find("a")["href"])

        return new_episode_links
