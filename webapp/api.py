import requests
import yaml


def get_releases(url):
    response = requests.get(url)
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
