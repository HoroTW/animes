"""The interface for anime details and the methods a plugin should 
implement to get the anime details from a website."""

import re
import yaml


class Anime:
    """Class to store the anime details"""

    def __init__(self, title, cover_url, episode_list):
        self.title = title
        self.cover_url = cover_url
        self.episode_list = episode_list

    def __repr__(self):
        serialized = yaml.dump(
            {
                "Title": self.title,
                "Cover": self.cover_url,
                "Episode_List": list(self.episode_list),
            },
            sort_keys=False,
        )
        return serialized


class AnimeInterface:
    """The interface for the anime details"""

    extra_headers: dict = {}

    def get_anime_from_url(self, url) -> Anime:
        """Get the anime details from the website"""
        raise NotImplementedError("This method should be implemented by the plugin")

    def login(self, username, password):
        """Login to the website"""
        raise NotImplementedError("This method should be implemented by the plugin")

    def add_extra_header(self, extra_header):
        """Add extra header to the extra headers, used for the requests"""
        self.extra_headers.update(extra_header)

    def get_base_url(self, url):
        """Get the base url of the website from the url provided"""
        return re.search(r"https?://[a-zA-Z0-9-.]+/", url).group(0)
