
from loguru import logger

from focus import ModelRes
from .pattern_cls import pattern_classifier, PAT_CLS_UNITS
from .alg_parser import parse_msg
from .ner import Ner
from .field import extract_fields
from .target_text import extract_target_text
from .cls_clear_text import clear_text
from .cls import Cls
from .cls_cfg import (
    TOPT_TOKENIZER_PATH as CLS_TOPT_TOKENIZER_PATH,
    TOPT_MODELS_PATHS as CLS_TOPT_MODELS_PATHS,
    SUBT_TOKENIZER_PATH as CLS_SUBT_TOKENIZER_PATH,
    SUBT_MODELS_PATHS as CLS_SUBT_MODELS_PATHS,
)


NER_MODEL_P = "./models/ner_2025-07-29_3-shuffle.bin"
DEVICE = "cpu"


class ExtrClsHandler:
    def __init__(self):
        self.ner_pipe = Ner(NER_MODEL_P, DEVICE)
        self.cls_pipe = Cls(
            CLS_TOPT_TOKENIZER_PATH,
            CLS_TOPT_MODELS_PATHS,
            CLS_SUBT_TOKENIZER_PATH,
            CLS_SUBT_MODELS_PATHS,
            DEVICE,
        )

    def __call__(self, text: str) -> ModelRes:
        logger.warning(f"Input text: {text}")

        pat_idx, pat_name = pattern_classifier(text, PAT_CLS_UNITS)
        logger.warning(f"Pattern: ({pat_idx}, {pat_name})")

        alg_text, alg_fields = parse_msg(pat_name, text)
        logger.warning(f"Alg parsed text: {alg_text}")
        logger.warning(f"Alg parsed fields: {alg_fields}")

        ner_res = self.ner_pipe(alg_text)
        logger.warning(f"NER res: {ner_res}")

        target_fields = extract_fields(alg_text, ner_res, alg_fields)
        logger.warning(f"Target fields: {target_fields}")
        
        target_text, target_ents = extract_target_text(alg_text, ner_res)
        logger.warning(f"Target text: {target_text}")
        logger.warning(f"Target ents: {target_ents}")

        target_text_clear = clear_text(target_text)
        logger.warning(f"Target text Clear: {target_text_clear}")

        text_topic, text_sub = self.cls_pipe.inf(text)
        logger.warning(f"Text topic: {text_topic}")
        logger.warning(f"Text sub: {text_sub}")

        res = ModelRes(
            card=target_fields["card"],
            azs=target_fields["azs"],
            trk=target_fields["trk"],
            fuel=target_fields["fuel"],
            topic=text_topic,
            sub=text_sub,
        )

        return res
