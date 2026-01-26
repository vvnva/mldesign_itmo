

import os


# Topics

TOPT_MODELS_ROOT_P = "./models/msg-cls_2025-07-31/topic_top-low"
os.makedirs(TOPT_MODELS_ROOT_P, exist_ok=True)

TOPT_TOKENIZER_PATH = os.path.join(TOPT_MODELS_ROOT_P, "tokenizer.bin")

TOPT_MODELS_PATHS = {
    "top-binary": {
        "model": os.path.join(TOPT_MODELS_ROOT_P, "model_top.bin"),
        "labels": os.path.join(TOPT_MODELS_ROOT_P, "labels_top.json"),
    },
    "low-rest": {
        "model": os.path.join(TOPT_MODELS_ROOT_P, "model_low.bin"),
        "labels": os.path.join(TOPT_MODELS_ROOT_P, "labels_low.json"),
    },
}


# Subtopics

SUBT_MODELS_ROOT_P = "./models/msg-cls_2025-07-31/subtopic"
os.makedirs(SUBT_MODELS_ROOT_P, exist_ok=True)

SUBT_TOKENIZER_PATH = os.path.join(SUBT_MODELS_ROOT_P, "tokenizer.bin")

SUBT_MODELS_PATHS = {
    "Программа лояльности": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_pro.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_pro.json"),
    },
    "Мобильное приложение": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_mob.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_mob.json"),
    },
    "Акции": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_acc.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_acc.json"),
    },
    "Качество обслуживания": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_kach.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_kach.json"),
    },
    "Онлайн Оплата": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_onl.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_onl.json"),
    },
    "ЧаВо": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_chav.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_chav.json"),
    },
    "Нецелевой звонок": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_nec.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_nec.json"),
    },
    "Использование ААЗС": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_isp.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_isp.json"),
    },
    "Топливо": {
        "model": os.path.join(SUBT_MODELS_ROOT_P, "model_top.bin"),
        "labels": os.path.join(SUBT_MODELS_ROOT_P, "labels_top.json"),
    },
}
