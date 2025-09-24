import yaml

# Read secondary-navigation.yaml
with open("secondary-navigation.yaml") as navigation_file:
    secondary_navigation_data = yaml.load(
        navigation_file.read(), Loader=yaml.FullLoader
    )

# These are built once at module load time
_bubble_path_lookup = {}  # Maps bubble paths to bubble data
_child_path_lookup = {}  # Maps child paths to bubble data
_fallback_paths = []  # Sorted list of bubble paths for fallback

for bubble_name, bubble_data in secondary_navigation_data.items():
    bubble_path = bubble_data.get("path", "")

    # Build bubble path lookup
    if bubble_path:
        _bubble_path_lookup[bubble_path] = bubble_data
        _fallback_paths.append(bubble_path)

    # Build child path lookup
    for child in bubble_data.get("children", []) or []:
        child_path = child.get("path")
        if child_path:
            _child_path_lookup[child_path] = bubble_data

# Sort fallback paths by length
# (longest first) for proper prefix matching
_fallback_paths.sort(key=len, reverse=True)


def get_current_page_bubble(path):
    """
    Create the "page_bubble" dictionary containing information
    about the current page and its child pages from
    secondary-navigation.yaml (if it exists). This dictionary is
    made globally available to all templates.
    """
    current_page_bubble = None

    # Priority order for selecting the bubble:
    # 1) Exact match on a bubble's own path
    if path in _bubble_path_lookup:
        current_page_bubble = _bubble_path_lookup[path]

    # 2) Exact match on any child path
    elif path in _child_path_lookup:
        current_page_bubble = _child_path_lookup[path]

    # 3) Fallback match on a bubble's path
    else:
        for bubble_path in _fallback_paths:
            if path.startswith(bubble_path):
                current_page_bubble = _bubble_path_lookup[bubble_path]
                break

    # Mark active child if current page bubble exists
    if current_page_bubble:
        children = current_page_bubble.get("children", [])
        if children:
            # Create a copy to avoid modifying the original data
            current_page_bubble = current_page_bubble.copy()
            current_page_bubble["children"] = []

            for child in children:
                child_copy = child.copy()
                if child_copy.get("path") == path:
                    child_copy["active"] = True
                current_page_bubble["children"].append(child_copy)

    return {"page_bubble": current_page_bubble}
