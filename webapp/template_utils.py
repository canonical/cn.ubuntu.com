def shorten_acquisition_url(acquisition_url):
    """
    Shorten the acquisition URL sent when submitting forms
    """

    if len(acquisition_url) > 255:
        url_without_params = acquisition_url.split("?")[0]
        url_params_string = acquisition_url.split("?")[1]
        url_params_list = url_params_string.split("&")

        for param in url_params_list:
            if param.startswith("fbclid") or param.startswith("gclid"):
                url_params_list.remove(param)

        new_acquisition_url = (
            url_without_params + "?" + "&".join(url_params_list)
        )

        return new_acquisition_url

    return acquisition_url
