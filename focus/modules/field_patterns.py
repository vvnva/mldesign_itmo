
import re

CARD_PATTERNS = [
    re.compile(r'\*{12}\d{4}'),       # ************1794    # 12 звёздочек + 4 цифры
    re.compile(r'\d{4}\*+\d{4}'),         # 4 цифры + звёздочки + 4 цифры (e.g., 2200********2086)
    re.compile(r'(?:7825|9000)[\d\*]{12}'),  # 16 знаков, начиная с 7825 или 9000, цифры или *
    re.compile(r'\*+\d{1,4}'),        # *9119, ***1234      #любое количество звёздочек + 1-4 цифры
    re.compile(r'(?:7825|9000)\d{12}')# 7825680601252380    # 16 цифр, начинающихся на 7825 или 9000
]

AZS_PATTERN = re.compile(r'(\d+)', flags=re.IGNORECASE)

ORD_ROOTS = {
    'перв': '1', 'втор': '2', 'трет': '3', 'четв': '4',
    'пят': '5', 'шест': '6', 'седьм': '7', 'восьм': '8',
    'девят': '9', 'десят': '10'
}

TRK_PATTERN = re.compile(
    rf"(?iu)(?P<ord>(?:{'|'.join(ORD_ROOTS.keys())})\w*)"
    r"|(?P<num>(?<!\d)\d{1,2}(?!\d))"
)

FUEL_DT_PATTERNS = [
    re.compile(r'(?i)\bдиз(?:ел|топ)\w*\b'),
    re.compile(r'(?i)\bдиз\.\s*топлив\w*\b'),
    re.compile(r'(?i)\bд/т\b'),
    re.compile(r'(?i)\bдт\b'),
]

FUEL_GAS_PATTERNS = [
    re.compile(r'(?i)\b(?:пропан|газ)\w*\b'),
    re.compile(r'(?i)\bсуг\b'),
]

FUEL_NUM_PATTERN = re.compile(
    r'(?iu)\b'
    r'(?:(?:аи|а|g)[-\s]?)?'    # опционально АИ, А или G
    r'(?P<num>\d{2,3})'         # 2–3 цифры
    r'(?:-м|-?го)?'             # опциональный суффикс
    r'\b'
)
