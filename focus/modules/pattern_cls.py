
from typing import Any, Callable
from dataclasses import dataclass


def classify_no_text(msg_text: str) -> bool:
    """Classify 0_no-text pattern."""
    key = 'no text message => see attachment'
    return key in msg_text


def classify_otrs(msg_text: str) -> bool:
    """Classify 1_otrs pattern."""
    keys = [
        'Письмо сгенерировано автоматически',
        'ДАННЫЕ ДЛЯ OTRS',
        'СООБЩЕНИЕ',
    ]
    return all([key in msg_text for key in keys])


def classify_accremoval(msg_text: str) -> bool:
    """Classify 2_accremoval pattern."""
    key = 'УДАЛИТЬ АККАУНТ'
    return key in msg_text


def classify_standard(msg_text: str) -> bool:
    """Classify 3_standard pattern."""
    keys = [
        # 'Номер заказа',
        'Контактный телефон',
        'Номер карты ПЛ',
        'Объект',
        'Адрес',
        'Примечание',
    ]
    return all([key in msg_text for key in keys])


def classify_udc(msg_text: str) -> bool:
    """Classify test udc pattern."""
    keys = [
        'Причина обращения',
        'Номер ОРТ',
        # 'Номер ТРК',
        'ТРК',
        'Вид НП',
        'Наличие транзакции',
        'Краткое описание обращения(хронология)'
    ]
    return all([key in msg_text for key in keys])


def classify_hotline_hotline_empty(msg_text: str) -> bool:
    """Classify test hotline-hotline empty pattern."""
    keys_hotline = [
        "пересылаем на рассмотрение сообщение Горячей линии",
        "Оператор Горячей линии по противодействию мошенничеству, коррупции и другим нарушениям Корпоративного кодекса",
        ": Hot-line <hot-line@gazprom-neft.ru>",
        
    ]
    keys_empty = [
        "Voice message 800 700 6500",
        "The letter was sent automatically, please do not reply to this message.",
    ]
    hotline_q = all([key in msg_text for key in keys_hotline])
    if not hotline_q:
        return False
    emty_q = any([key in msg_text for key in keys_empty])
    return emty_q


def classify_hotline_hotline(msg_text: str) -> bool:
    """Classify test hotline-hotline pattern."""
    keys = [
        'пересылаем на рассмотрение сообщение Горячей линии',
        'Оператор Горячей линии по противодействию мошенничеству, коррупции и другим нарушениям Корпоративного кодекса',
        ': Hot-line <hot-line@gazprom-neft.ru>',
        'Сообщение из формы HOTLINE',
    ]
    return all([key in msg_text for key in keys])


def classify_hotline_free(msg_text: str) -> bool:
    """Classify test hotline-free pattern."""
    keys = [
        'пересылаем на рассмотрение сообщение Горячей линии',
        'Оператор Горячей линии по противодействию мошенничеству, коррупции и другим нарушениям Корпоративного кодекса',
        'Hot-line <hot-line@gazprom-neft.ru>',
    ]
    return all([key in msg_text for key in keys])


def classify_hotline_feedback(msg_text: str) -> bool:
    """Classify test hotline-feedback pattern."""
    keys = [
        'Информационное сообщение сайта www.gazprom-neft.ru',
        'Вам было отправлено сообщение через форму обратной связи',
        'Сообщение сгенерировано автоматически.',
    ]
    return all([key in msg_text for key in keys])


def classify_corp_res(msg_text: str) -> bool:
    """Classify CorpRes pattern."""
    keys = [
        'Информационная служба',
        'ПАО "ГАЗПРОМ НЕФТЬ"',
        'Россия, 190000, Санкт-Петербург, ул. Почтамтская, д.3-5',
        'WWW.GAZPROM-NEFT.RU',
    ]
    return all([key in msg_text for key in keys])


def classify_other(msg_text: str) -> bool:
    """Dummy classify any other pattern. Always True."""
    return True


def classify_complaint(msg_text: str) -> bool:
    """Classify 1_otrs pattern."""
    keys = [
        'Суть обращения',
        'Принятые меры',
        'Ответ клиенту',
    ]
    return all([key in msg_text for key in keys])


@dataclass
class PatternClassifierUnit:
    idx: int
    name: str
    func: Callable[[str], bool]


def pattern_classifier(
        msg_text: str,
        pattern_classifiers: list[PatternClassifierUnit]
    ) -> tuple[int, str]:
    """Classify text message pattern consequently. Return pat (idx, name)."""
    for classifier in pattern_classifiers:
        if classifier.func(msg_text):
            return classifier.idx, classifier.name
    return OTHER_UNIT.idx, OTHER_UNIT.name


PAT_CLS_UNITS = [
    PatternClassifierUnit(idx=0, name='NoText', func=classify_no_text),
    PatternClassifierUnit(idx=1, name='OTRS', func=classify_otrs),
    PatternClassifierUnit(idx=2, name='AccRemoval', func=classify_accremoval),
    PatternClassifierUnit(idx=3, name='Standard', func=classify_standard),
    PatternClassifierUnit(idx=4, name='UDC', func=classify_udc),
    PatternClassifierUnit(idx=5, name='HotlineEmpty', func=classify_hotline_hotline_empty),
    PatternClassifierUnit(idx=6, name='HotlineHotline', func=classify_hotline_hotline),
    PatternClassifierUnit(idx=7, name='HotlineFree', func=classify_hotline_free),
    PatternClassifierUnit(idx=8, name='HotlineFeedback', func=classify_hotline_feedback),
    PatternClassifierUnit(idx=9, name='CorpRes', func=classify_corp_res),
    PatternClassifierUnit(idx=10, name='ComplaintBook', func=classify_complaint),
    PatternClassifierUnit(idx=11, name='Other', func=classify_other),
]
OTHER_UNIT = PAT_CLS_UNITS[-1]


IDX_TO_PAT = {pcu.idx: pcu.name for pcu in PAT_CLS_UNITS}
PAT_TO_IDX = {pcu_name: pcu_idx for pcu_idx, pcu_name in IDX_TO_PAT.items()}
