
import string
from typing import Any
from dataclasses import asdict

from focus import txt_lab


NOISE_CATS = {'corp_info', 'mail_info', 'tech_info', 'greetings'}
MEANINGFUL_CATS = {
    'address', 'azs', 'card', 'company', 'date', 'fuel',
    'litr', 'money', 'phone', 'time', 'trk', 'payment',
}
PUNCTUATION = string.punctuation + "«»—…" + "0123456789"


def concat_new_line_ents(text: txt_lab.Text) -> txt_lab.Text:
    txt = text.text
    txt_new = ""
    left = 0
    for ent in text.entities:
        ent_text = txt[ent.beg:ent.end]
        if ent.cat not in NOISE_CATS and "\n" in ent_text:
            ent_text = ent_text.replace("\n", " ")
        txt_new = f"{txt_new}{txt[left:ent.beg]}{ent_text}"
        left = ent.end
    txt_new = f"{txt_new}{txt[left:]}"
    return txt_lab.Text(txt_new, text.entities)


def has_text(line: txt_lab.Text) -> bool:
    clear = txt_lab.drop_cats(line, MEANINGFUL_CATS)
    clear_text = clear.text.strip(PUNCTUATION + " \t").strip()
    return bool(clear_text)


def form_tlab(text: str, ner_ents: list[dict[str, Any]]):
    return txt_lab.Text(
        text=text,
        entities=[
            txt_lab.Entity(ent["beg"], ent["end"], ent["cat"])
            for ent in ner_ents
        ],
    )

def extract_target_text(
        text: str,
        ner_ents: list[dict[str, Any]],
    ) -> tuple[str, list[dict[str, Any]]]:
    text_lab = form_tlab(text, ner_ents)
    concat_ents = concat_new_line_ents(text_lab)
    noise_clear = txt_lab.drop_cats(concat_ents, NOISE_CATS)
    clear_lines = txt_lab.split_by_symbol(noise_clear, "\n")
    target_lines = [line for line in clear_lines if has_text(line)]
    target_text_lab = txt_lab.concat_list(target_lines, " ")
    target_ents = [asdict(ent) for ent in target_text_lab.entities]
    return target_text_lab.text, target_ents
