import glob
import json
import os
import re
from pathlib import Path
from pprint import pprint


def normalize_line(line):
    """
    Se una riga risulta "sparsa" (ovvero se la maggior parte dei token sono singoli caratteri),
    li unisce in una stringa continua. Altrimenti restituisce la riga stripped.
    """
    tokens = line.strip().split()
    # Se almeno il 50% dei token ha lunghezza 1, assumiamo che la riga sia mal formattata.
    if tokens and (sum(1 for t in tokens if len(t) == 1) / len(tokens)) > 0.5:
        # Uniamo tutti i token senza spazi (o, se si preferisce, si può aggiungere uno spazio solo
        # se il token ha lunghezza > 1 – in questo esempio uniamo tutto)
        return "".join(tokens)
    return line.strip()


def extract_global_info(text):
    """
    Cerca nel testo le informazioni globali:
      - Il nome del ristorante (ricerca di una riga che inizia con “## Ristorante”)
      - Il nome dello chef (ricerca di una riga contenente la parola “Chef”)

    Se la formattazione è non standard (ad esempio “Chef:” oppure scritta in maniera “sparsa”),
    viene utilizzata una regex flessibile. Se non viene trovata alcuna informazione, viene restituita la stringa vuota.
    """
    restaurant_name = ""
    chef_name = ""
    # Per analizzare riga per riga il testo già normalizzato
    for line in text.splitlines():
        norm_line = normalize_line(line)
        # Tenta di individuare il ristorante: si cerca una riga che inizi con "##" seguita da "Ristorante"
        if not restaurant_name and re.search(r"(?i)^##\s*Ristorante", norm_line):
            # La regex tenta di catturare il nome che segue, eventualmente dopo due punti o virgolette
            m = re.search(r'^##\s*Ristorante\s*[:"]?\s*(.+?)\s*["\']?$', norm_line)
            if m:
                restaurant_name = m.group(1).strip()
            else:
                # In fallback, rimuove la parte “##” e “Ristorante”
                restaurant_name = (
                    norm_line.replace("##", "").replace("Ristorante", "").strip(" :\"'")
                )

        # Per lo chef, cerchiamo una riga contenente “chef” (case-insensitive)
        if not chef_name and re.search(r"(?i)chef", norm_line):
            # La regex permette di gestire formati come "Chef:" o "Chef Executive:" o anche "Chef -"
            m = re.search(r"(?i)chef(?:\s*(?:executive)?\s*[:\-])?\s*(.+)", norm_line)
            if m:
                chef_name = m.group(1).strip(" \"'")

        # Se entrambe le informazioni sono state trovate, usciamo dal loop
        if restaurant_name and chef_name:
            break

    if not restaurant_name:
        for line in text.splitlines():
            norm_line = normalize_line(line)
            if norm_line.startswith("##"):
                # Rimuoviamo "##" e eventuali caratteri di punteggiatura/spazi in eccesso
                restaurant_name = norm_line.replace("##", "").strip(" :\"'")

                # Una volta trovato il primo titolo, usciamo dal loop
                break
    return restaurant_name, chef_name


def extract_recipes(text, default_restaurant, default_chef):
    """
    Estrae le sezioni relative alle ricette.
    Si assume che ogni ricetta inizi con un'intestazione di secondo livello (##)
    MA si escludono le intestazioni globali (Ristorante, Chef, Menu, Ingredienti, Tecniche, ecc.).

    Per ciascuna ricetta viene estratto:
      - il titolo (recipe_name)
      - il testo relativo (recipe_text)

    Le informazioni globali (ristorante e chef) vengono aggiunte a ciascun dizionario.
    """
    # Estrae il nome del ristorante (rimuovendo eventuali virgolette)
    restaurant_match = re.search(
        r'^## Ristorante\s+"?([^"\n]+)"?', text, flags=re.MULTILINE
    )
    restaurant_name = restaurant_match.group(1).strip() if restaurant_match else ""
    if restaurant_name == "":
        restaurant_name = default_restaurant

    # Estrae il nome del chef
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
        # Se non siamo all'ultima ricetta, il testo della ricetta va fino all'inizio della successiva ricetta
        if i + 1 < len(recipe_matches):
            end_index = recipe_matches[i + 1].start()
        else:
            end_index = len(recipes_section)
        recipe_body = recipes_section[start_index:end_index].strip()

        # Costruisce il dizionario per la ricetta
        recipe_dict = {
            "recipe_name": recipe_title,
            "recipe_restaurant": restaurant_name,
            "recipe_chef": chef_name,
            "recipe_text": recipe_body,
        }
        recipes.append(recipe_dict)
    return recipes


def process_file(filepath):
    """
    Apre il file markdown, normalizza le righe e ne estrae:
      - le informazioni globali (ristorante e chef)
      - le ricette presenti
    Il tutto avviene in maniera "robusta": se il file è mal formattato o mancano dati,
    il codice non genera errori ma utilizza stringhe vuote come default.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Errore nella lettura del file {filepath}: {e}")
        return []  # In caso di errore, restituiamo una lista vuota

    # Normalizziamo ciascuna riga del file
    lines = content.splitlines()
    normalized_lines = [normalize_line(line) for line in lines]
    normalized_text = "\n".join(normalized_lines)

    # Estraiamo le informazioni globali (ristorante e chef)
    restaurant_name, chef_name = extract_global_info(normalized_text)

    # Estraiamo le ricette presenti nel file, utilizzando i dati globali come default
    recipes = extract_recipes(normalized_text, restaurant_name, chef_name)
    return recipes


def process_directory(input_path: Path | str):
    """
    Scansiona la cartella (path) cercando tutti i file *.md e li elabora.
    Restituisce una lista di dizionari, ciascuno corrispondente a una ricetta estratta.
    """
    path_name = Path(input_path)
    all_recipes = []
    md_files = glob.glob(os.path.join(os.path.join(path_name, "menu_md"), "*.md"))

    for md_file in md_files:
        file_recipes = process_file(md_file)
        all_recipes.extend(file_recipes)

    path_output = path_name / "menu_json.json"
    with path_output.open("w") as f:
        json.dump(all_recipes, f, indent=4)

    return all_recipes


path = "..\data\processed"

recipes = process_directory(path)

# Visualizziamo il risultato (lista di dizionari)
pprint(recipes)
