import json
import os

def load_card_rules(card_name):
    path = os.path.join("cards", "cards.json")
    with open(path, "r") as file:
        cards = json.load(file)
    for card in cards:
        if card["card_name"] == card_name:
            return card
    raise ValueError(f"Card '{card_name}' not found")

def list_card_names():
    path = os.path.join("cards", "cards.json")
    with open(path, "r") as file:
        cards = json.load(file)
    return [card["card_name"] for card in cards]
