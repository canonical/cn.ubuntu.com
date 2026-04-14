import logging
import requests
import yaml

logger = logging.getLogger(__name__)
RELEASES_CACHE_KEY = "releases_data"
RELEASES_URL = (
    "https://raw.githubusercontent.com/canonical/"
    "ubuntu.com/main/releases.yaml"
)


def get_releases(url):
    """Fetch releases.yaml from the given URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = yaml.load(response.text, Loader=yaml.FullLoader)

    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }

    for category, info in data.items():
        if isinstance(info, dict):
            for key in ["release_date", "eol"]:
                if key in info and isinstance(info[key], str):
                    parts = info[key].split()

                    if (
                        len(parts) == 2
                        and parts[0] in month_map
                        and parts[1].isdigit()
                    ):
                        info[key] = f"{parts[1]}年{month_map[parts[0]]}月"

    return data


def get_releases_cached(cache):
    """
    Get releases from cache or fetch and cache if missing.
    """
    cached_data = cache.get(RELEASES_CACHE_KEY)

    if cached_data is not None:
        logger.info("Releases loaded from cache")
        return cached_data

    try:
        logger.info(f"Fetching releases from {RELEASES_URL}...")
        data = get_releases(RELEASES_URL)
        # Cache for one hour
        cache.set(RELEASES_CACHE_KEY, data, timeout=3600)
        logger.debug("Releases fetched and cached successfully")
        return data
    except Exception as e:
        logger.error(f"Failed to fetch releases: {e}")
        raise
