import re
from pathlib import Path
from typing import Dict, List


def normalize_line(line):
    """
    If a line is "sparse" (i.e., most tokens are single characters),
    it joins them into a continuous string. Otherwise, it returns the stripped line.
    """
    tokens = line.strip().split()
    # If at least 50% of the tokens are of length 1, we assume the line is poorly formatted.
    if tokens and (sum(1 for t in tokens if len(t) == 1) / len(tokens)) > 0.5:
        # Join all tokens without spaces (or, if preferred, add a space only if the token length > 1)
        return "".join(tokens)
    return line.strip()


def extract_global_info(text):
    """
    Searches the text for global information:
      - The name of the restaurant (search for a line starting with "## Ristorante")
      - The name of the chef (search for a line containing the word "Chef")

    If the formatting is non-standard (e.g., "Chef:" or written in a "sparse" manner),
    a flexible regex is used. If no information is found, an empty string is returned.
    """
    restaurant_name = ""
    chef_name = ""
    # Analyze the text line by line after normalization
    for line in text.splitlines():
        norm_line = normalize_line(line)
        # Attempt to identify the restaurant: look for a line starting with "##" followed by "Ristorante"
        if not restaurant_name and re.search(r"(?i)^##\s*Ristorante", norm_line):
            # The regex attempts to capture the name that follows, possibly after a colon or quotes
            m = re.search(r'^##\s*Ristorante\s*[:"]?\s*(.+?)\s*["\']?$', norm_line)
            if m:
                restaurant_name = m.group(1).strip()
            else:
                # As a fallback, remove the "##" and "Ristorante" parts
                restaurant_name = (
                    norm_line.replace("##", "").replace("Ristorante", "").strip(" :\"'")
                )

        # For the chef, look for a line containing "chef" (case-insensitive)
        if not chef_name and re.search(r"(?i)chef", norm_line):
            # The regex handles formats like "Chef:", "Chef Executive:", or even "Chef -"
            m = re.search(r"(?i)chef(?:\s*(?:executive)?\s*[:\-])?\s*(.+)", norm_line)
            if m:
                chef_name = m.group(1).strip(" \"'")

        # If both pieces of information are found, exit the loop
        if restaurant_name and chef_name:
            break

    if not restaurant_name:
        for line in text.splitlines():
            norm_line = normalize_line(line)
            if norm_line.startswith("##"):
                # Remove "##" and any excess punctuation/spaces
                restaurant_name = norm_line.replace("##", "").strip(" :\"'")

                # Once the first title is found, exit the loop
                break
    return restaurant_name, chef_name


def extract_recipes(text, default_restaurant, default_chef):
    """
    Extracts sections related to recipes.
    Assumes each recipe starts with a second-level header (##)
    BUT excludes global headers (Ristorante, Chef, Menu, Ingredienti, Tecniche, etc.).

    For each recipe, it extracts:
      - the title (recipe_name)
      - the related text (recipe_text)

    Global information (restaurant and chef) is added to each dictionary.
    """
    # Extract the restaurant name (removing any quotes)
    restaurant_match = re.search(
        r'^## Ristorante\s+"?([^"\n]+)"?', text, flags=re.MULTILINE
    )
    restaurant_name = restaurant_match.group(1).strip() if restaurant_match else ""
    if restaurant_name == "":
        restaurant_name = default_restaurant

    # Extract the chef's name
    chef_match = re.search(r"^## Chef\s+(.+)$", text, flags=re.MULTILINE)
    chef_name = chef_match.group(1).strip() if chef_match else ""
    if chef_name == "":
        chef_name = default_chef

    menu_index = text.find("## Menu")
    if menu_index != -1:
        recipes_section = text[menu_index:]
    else:
        recipes_section = text

    recipe_pattern = r"^## (?!Ristorante|Chef|Menu|Ingredienti|Tecniche)(.+)$"
    recipe_matches = list(
        re.finditer(recipe_pattern, recipes_section, flags=re.MULTILINE)
    )

    recipes = []
    for i, match in enumerate(recipe_matches):
        recipe_title = match.group(1).strip()
        start_index = match.end()
        # If not the last recipe, the recipe text goes up to the start of the next recipe
        if i + 1 < len(recipe_matches):
            end_index = recipe_matches[i + 1].start()
        else:
            end_index = len(recipes_section)
        recipe_body = recipes_section[start_index:end_index].strip()

        # Build the dictionary for the recipe
        recipe_dict = {
            "recipe_name": recipe_title,
            "recipe_restaurant": restaurant_name,
            "recipe_chef": chef_name,
            "recipe_text": recipe_body,
        }
        recipes.append(recipe_dict)
    return recipes


def extract_restaurant_text(text: str) -> str:
    """
    Extracts the text from immediately after the chef header up to (but not including) the "## Menu" header.

    This function searches for a line that contains the word "Chef" (case-insensitive) and, if found,
    extracts all subsequent text (i.e. text following the entire line that contains "Chef")
    until the "## Menu" header is encountered.
    Neither the chef header line nor the menu header is included in the result.

    If the chef header is not found, extraction starts from the beginning of the text.
    If the menu header is not found, extraction continues to the end of the text.
    """
    # Find the line that contains "Chef" (case-insensitive).
    chef_line_match = re.search(r"(?im)^.*Chef.*$", text)
    if chef_line_match:
        # Start extraction after the entire chef line.
        start_index = chef_line_match.end()
    else:
        start_index = 0

    # Find the "## Menu" header.
    menu_match = re.search(r"(?im)^##\s*Menu.*$", text)
    if menu_match:
        end_index = menu_match.start()
    else:
        end_index = len(text)

    # Extract and return the text between the chef line and the menu header.
    return text[start_index:end_index].strip()


def process_file(filepath):
    """
    Opens the markdown file, normalizes the lines, and extracts:
      - global information (restaurant and chef)
      - the recipes present
    All in a "robust" manner: if the file is poorly formatted or data is missing,
    the code does not generate errors but uses empty strings as defaults.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []  # In case of error, return an empty list

    # Normalize each line of the file
    lines = content.splitlines()
    normalized_lines = [normalize_line(line) for line in lines]
    normalized_text = "\n".join(normalized_lines)

    # Extract global information (restaurant and chef)
    restaurant_name, chef_name = extract_global_info(normalized_text)

    # Extract the recipes present in the file, using global data as defaults
    recipes = extract_recipes(normalized_text, restaurant_name, chef_name)
    restaurant = {
        "restaurant_name": restaurant_name,
        "chef_name": chef_name,
        "restaurant_text": extract_restaurant_text(normalized_text),
    }
    return recipes, restaurant


def ingest_md_to_json(input_path: Path | str) -> List[Dict]:
    """
    Processes the recipe data from markdown files in the input directory and saves the result to a JSON file.
    Args:
        input_path (str): Path to the input directory containing markdown files.
        output_path (str): Path to the output JSON file.
    Returns:
        list: A list of dictionaries containing the processed recipe data.
    """
    input_dir = Path(input_path)

    all_recipes = []
    all_restaurants = []
    md_files = list(input_dir.glob("*.md"))

    for md_file in md_files:
        file_recipes, file_restaurant = process_file(md_file)

        all_recipes.extend(file_recipes)
        all_restaurants.append(file_restaurant)

    output = {"recipes": all_recipes, "restaurants": all_restaurants}

    return output
