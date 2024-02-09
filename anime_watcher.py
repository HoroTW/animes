#!/usr/bin/env python3
"""
This module is used to get the new episodes of the animes that are currently being watched
"""

import os
import logging
import importlib.util
import yaml
from anime_interface import AnimeInterface
from static_site_generator import generate_static_site

PLUGIN_FOLDER = "plugins"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


with open("animes.yaml", encoding="utf-8") as file:
    anime_file = yaml.load(file, Loader=yaml.FullLoader)
    curr_watching = anime_file["currently_watching"]
    assert curr_watching, "No animes are currently being watched, please add animes to the list"
logger.debug("The animes that are currently being watched are: %s", curr_watching)


def get_plugin(plugin_identifier) -> AnimeInterface:
    """Get the plugin class from the plugin identifier"""
    # Get a list of files in the plugin folder
    plugin_files = os.listdir(PLUGIN_FOLDER)

    for file_name in plugin_files:
        if file_name.endswith(".py"):  # Consider only Python files
            # Remove the '.py' extension to get the plugin name
            plugin_name = file_name[:-3]
            if plugin_name.replace(".", "_") != plugin_identifier.replace(".", "_"):
                continue

            # Generate the module name
            module_name = f"{PLUGIN_FOLDER}.{plugin_name}"

            # Import the module dynamically using importlib
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(PLUGIN_FOLDER, file_name))
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)

            # Find the AnimePlugin class within the module
            for name in dir(plugin_module):
                if name == "AnimePlugin":
                    obj = getattr(plugin_module, name)
                    # Instantiate the class and return it
                    return obj()


def main():
    """The main function"""
    anime_list = []

    for plugin_identifier in curr_watching:
        plugin = get_plugin(plugin_identifier)
        username = curr_watching[plugin_identifier].get("username")
        password = curr_watching[plugin_identifier].get("password")
        if username and password:
            plugin.login("username", "password")

        extra_headers = curr_watching[plugin_identifier].get("extra_headers", None)
        if extra_headers:
            for key, value in extra_headers.items():
                plugin.add_extra_header({key: value})

        for anime_url in curr_watching[plugin_identifier]["series"]:
            logger.info("\n%s: %s", plugin_identifier, anime_url)
            anime_obj = plugin.get_anime_from_url(anime_url)
            print(anime_obj)
            if anime_obj.episode_list:
                anime_list.append(anime_obj)

    result_path = generate_static_site(anime_list)
    os.system(f"xdg-open {result_path}")


if __name__ == "__main__":
    main()
