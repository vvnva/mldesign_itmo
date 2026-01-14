
from dataclasses import dataclass


@dataclass
class Entity:
    beg: int
    end: int
    cat: str


@dataclass
class Text:
    text: str
    entities: list[Entity]


def dict_to_text(data: dict) -> Text:
    ents = [
        Entity(ent["beg"], ent["end"], ent["cat"])
        for ent in data["entities"]
    ]
    return Text(data["text"], ents)
