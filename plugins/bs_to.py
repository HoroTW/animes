"""The plugin for the website bs.to"""

import logging
import re
from bs4 import BeautifulSoup
import requests
from anime_interface import Anime, AnimeInterface, Episode

# extend/implement the AnimeInterface
logger = logging.getLogger(__name__)


class AnimePlugin(AnimeInterface):
    """The interface for the anime details"""

    session = requests.Session()

    def login(self, username, password):
        """Login to the website"""

        # first a plain GET to collect the security token
        response = self.session.get("https://bs.to/", timeout=5)
        assert response.status_code == 200, "The login page could not be fetched"

        security_token = re.search(
            r'<input type="hidden" name="security_token" value="(.*)" />',
            response.text,
        ).group(1)
        logger.debug("The security token is: %s", security_token)  # not a secret so we can log it
        assert security_token, "The security token could not be found"

        data = {
            "login[user]": username,
            "login[pass]": password,
            "security_token": security_token,
        }

        response = self.session.post("https://bs.to/", data=data, timeout=5)
        assert response.status_code == 200, f"The login was not successful with the status code: {response.status_code}"
        error = re.search(r'<div class="messageBox error">(.*?)</div>', response.text)
        assert not error, f"The login was not successful, error: {error.group(1)}"
        assert f"Hallo<strong>{username}</strong>" in response.text, "The login was not successful, unknown error"

        logger.info("The login was successful")

    def get_anime_from_url(self, url) -> Anime:
        """Get the episodes from all seasons that are unwatched"""

        base_url = self.get_base_url(url)
        self.session.headers.update(self.extra_headers)

        # Get the page
        page = self.session.get(url, timeout=5)

        # Check if the page was fetched successfully
        assert page.status_code == 200, f"The page could not be fetched for the url: {url}"
        soup = BeautifulSoup(page.content, "html.parser")

        new_episodes = []

        seasons = soup.find("div", class_="seasons")
        assert seasons, f"No seasons found for the anime: {url}, pls report this issue"

        # find child with li class that without watched
        for season in seasons.find("div", id="seasons").find_all("li"):
            if "watched" in season["class"]:
                continue

            # New season found
            season_url = base_url + season.find("a")["href"]
            new_episodes.extend(self.get_season_episodes(season_url))

        logger.debug("The new episodes for the anime are: %s", new_episodes)

        # Get Title of the anime
        title = soup.find("div", id="sp_left").find("h2").text.strip().split("\n")[0]
        cover_image = base_url + soup.find("div", id="sp_right").find("img")["src"]
        series_url = re.search(r"https?://bs.to/serie/.*/?[0-9]*/?[a-zA-Z]{0,3}", url).group(0)
        new_episodes = sorted(set(new_episodes))

        return Anime(title, series_url, cover_image, new_episodes)

    def get_season_episodes(self, url):
        """Get the anime details from the website"""
        base_url = self.get_base_url(url)

        # Get the page
        page = self.session.get(url, timeout=5)

        # check if the page was fetched successfully
        assert page.status_code == 200, f"The page could not be fetched for the url: {url}"
        soup = BeautifulSoup(page.content, "html.parser")

        new_episode_links = []

        episodes = soup.find("table", class_="episodes")
        assert episodes, f"No episodes in current season for the anime: {url}"

        for ep in episodes.find_all("tr"):  # Check if the episode is watched
            if "watched" in ep["class"]:
                continue

            link = base_url + ep.find("a")["href"]
            ep_title = ep.find("a")["title"]
            new_episode_links.append(Episode(ep_title, link))

        return new_episode_links
