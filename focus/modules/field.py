
import re
from typing import Any

from .field_patterns import (
    CARD_PATTERNS, AZS_PATTERN,
    ORD_ROOTS, TRK_PATTERN,
    FUEL_DT_PATTERNS, FUEL_GAS_PATTERNS,
    FUEL_NUM_PATTERN
)


TARGET_FIELDS = {"card", "azs", "trk", "fuel", "payment"}


def clean_card(content: str) -> list[str]:
    norm = re.sub(r'[^0-9\*]', '', content)
    matches = []
    for pat in CARD_PATTERNS:
        matches.extend([m.group() for m in pat.finditer(norm)])
    if not matches:
        m = re.search(r'[\d\*]+', norm)
        if m:
            matches = [m.group()]
    seen = set()
    uniq = [x for x in matches if x not in seen and not seen.add(x)]
    filtered = [x for x in uniq if not any(x != y and x in y for y in uniq)]
    return filtered


def clean_azs(snippet: str) -> list[str]:
    nums = AZS_PATTERN.findall(snippet)
    seen = set()
    uniq = [x for x in nums if x not in seen and not seen.add(x)]
    return uniq


def clean_trk(snippet: str) -> list[str]:
    norm = snippet.lower()
    matches = []
    for m in TRK_PATTERN.finditer(norm):
        if m.group('num'):
            matches.append(m.group('num'))
        else:
            tok = m.group('ord')
            for root, num in ORD_ROOTS.items():
                if tok.startswith(root):
                    matches.append(num)
                    break
    seen = set()
    uniq = [x for x in matches if x not in seen and not seen.add(x)]
    return uniq


def clean_fuel(snippet: str) -> list[str]:
    matches = []
    # дизельные виды - ДТ
    for pat in FUEL_DT_PATTERNS:
        if pat.search(snippet):
            matches.append('ДТ')
            break
    # пропан/газ и СУГ - ГАЗ
    for pat in FUEL_GAS_PATTERNS:
        if pat.search(snippet):
            matches.append('ГАЗ')
            break
    # сотый и однокоренные - 100
    if re.compile(r'(?i)\bсот\w*\b').search(snippet):
        matches.append('100')
    # бензинные варианты топлива
    for m in FUEL_NUM_PATTERN.finditer(snippet):
        matches.append(m.group('num'))
    seen = set()
    uniq = [x for x in matches if x not in seen and not seen.add(x)]
    return uniq


def clean_payment(snippet: str) -> list[str]:
    return [re.sub(r'\s+', ' ', snippet).strip()]


CLEAN_FUNCS = {
    "card": clean_card,
    "azs": clean_azs,
    "trk": clean_trk,
    "fuel": clean_fuel,
    "payment": clean_payment,
}

def extract_fields(
        text: str,
        ner_res: list[dict[str, Any]],
        alg_fields: dict[str, str],
    ) -> dict[str, str]:
    # TODO: Алгоритмический парсер должен возвращать строчку из сущностей через
    # специальный разделитель <|ENT_SEP|>. Чтобы их можно было здесь разделить, 
    # обработать и почистить через CLEAN_FUNCS.
    parsed_fields = {targ_f: set() for targ_f in TARGET_FIELDS}
    # alg ents
    ent_sep = "<|ENT_SEP|>"
    for targ_f in TARGET_FIELDS:
        contents = alg_fields.get(targ_f, "").split(ent_sep)
        for cont in contents:
            contents_clear = CLEAN_FUNCS[targ_f](cont)
            parsed_fields[targ_f].update(contents_clear)
    # ner ents
    for ent in ner_res:
        if ent["cat"] in TARGET_FIELDS:
            content = text[ent["beg"]:ent["end"]]
            contents_clear = CLEAN_FUNCS[ent["cat"]](content)
            parsed_fields[ent["cat"]].update(contents_clear)
    # post process
    parsed_fields = {k: ", ".join(sorted(v)) for k, v in parsed_fields.items()}
    return parsed_fields
