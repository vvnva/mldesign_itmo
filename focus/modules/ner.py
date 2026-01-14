
from typing import Any
from loguru import logger
from transformers import (
    pipeline,
    AutoModelForTokenClassification as AMFTC,
    AutoTokenizer,
)


NER_FIELDS_MAP = {
    "entity_group": "cat",
    "score": "p",
    "start": "beg",
    "end": "end",
    "word": "word",
}


class Ner:
    def __init__(self, model_p: str, device: str):
        self.model_p = model_p
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_p)
        logger.warning(f'NER tokenizer: {self.model_p}')
        self.model = AMFTC.from_pretrained(self.model_p)
        logger.warning(f'NER model: {self.model_p}')
        self.model.to(self.device)
        self.model.eval()
        self.ner_pipe = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
        )
        self.ner_pipe

    @staticmethod
    def _post_proc(ner_raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ner_proc = []
        for ent in ner_raw:
            ent_proc = {NER_FIELDS_MAP[k]: v for k, v in ent.items()}
            del ent_proc["word"]
            ent_proc["p"] = ent_proc["p"].item()
            ner_proc.append(ent_proc)
        return ner_proc

    def __call__(self, text: str):
        ner_raw = self.ner_pipe(text)
        ner_proc = self._post_proc(ner_raw)
        return ner_proc
