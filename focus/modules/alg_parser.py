
import re


OTRS_CONST = {
    'q_type_n': len('ТИП ОБРАЩЕНИЯ'),
    'q_topic_n': len('ТЕМА ВОПРОСА'),
    'card_n': len('НОМЕР КАРТЫ'),
    'card_old_n': len('НОМЕР СТАРОЙ КАРТЫ'),
    'card_new_n': len('НОМЕР НОВОЙ КАРТЫ'),
    'msg_n': len('СООБЩЕНИЕ'),
    'azs_n': len('НОМЕР АЗС'),
    'trk_n': len('НОМЕР КОЛОНКИ'),
    'fuel_n': len('ВИД ТОПЛИВА'),
    'stars_n': len('*******************************'),
}


HOTLINE_HOTLINE_CONST = {
    'msg_n': len('Текст сообщения:'),
}


HOTLINE_FREE_CONST = {
    'Тема: [☝❗EXTERNAL❗]': {
        'msg_n': len('Тема: [☝❗EXTERNAL❗]'),
    },
    'Тема: ': {
        'msg_n': len('Тема:'),
    },
    'Subject: [☝❗EXTERNAL❗]': {
        'msg_n': len('Subject: [☝❗EXTERNAL❗]'),
    }
}


HOTLINE_FEEDBACK_CONST = {
    'msg_n': len('Ваше сообщение:'),
}


STANDARD_CONST = {
    'order_n': len('Номер заказа:'),
    'special_n': len('Примечание:'),
}


COMPLAINT_CONST = {
    "msg_n": len("Суть обращения"),
    "ans_n": len("Ответ клиенту"),
    "azs_fcs": ["№ Магазина и АЗС", "№ АЗС", "АЗС"],
    "date_fcs": ["Дата обращения клиента", "Дата"],
}


ACCREM_CONST = {
    "card_n": len("Номер карты лояльности №N:"),
}


def clean_field(text: str) -> str:
    """Обрезает лишние пробелы и знаки препинания в начале и конце строки."""
    text = text.strip()
    text = re.sub(r'^[^A-Za-zА-Яа-я0-9]+', '', text)
    return re.sub(r'[^A-Za-zА-Яа-я0-9]+$', '', text)


def parse_otrs(msg: str) -> dict[str, str]:
    """Extract text from OTRS Pattern message."""
    res = {}
    # parse question type
    qtype_start = msg.index('ТИП ОБРАЩЕНИЯ\n*')
    qtype_end = msg.index('ТЕМА ВОПРОСА\n*')
    res['request_type'] = (
        msg[qtype_start + OTRS_CONST['q_type_n']+1
        + OTRS_CONST['stars_n']+1 : qtype_end]
    )
    res['request_type'] = clean_field(res['request_type'])
    # parse question topic
    qtopic_start = msg.index('ТЕМА ВОПРОСА\n*')
    qtopic_end = msg.index('ТИП ВОПРОСА\n*')
    res['request_topic'] = (
        msg[qtopic_start + OTRS_CONST['q_topic_n']+1
        + OTRS_CONST['stars_n']+1 : qtopic_end]
    )
    res['request_topic'] = clean_field(res['request_topic'])
    # parse cards numbers
    cards = []
    # card main
    card_start = msg.index('НОМЕР КАРТЫ\n*')
    card_end = msg.index('КАК К ВАМ ОБРАЩАТЬСЯ?\n*')
    card_main = (
        msg[card_start + OTRS_CONST['card_n']+1
        + OTRS_CONST['stars_n']+1 : card_end]
    )
    cards.append(clean_field(card_main))
    # card old
    card_old_start = msg.index('НОМЕР СТАРОЙ КАРТЫ\n*')
    card_old_end = msg.index('НОМЕР НОВОЙ КАРТЫ\n*')
    card_old = (
        msg[card_old_start + OTRS_CONST['card_old_n']+1
        + OTRS_CONST['stars_n']+1 : card_old_end]
    )
    cards.append(clean_field(card_old))
    # card new
    card_new_start = msg.index('НОМЕР НОВОЙ КАРТЫ\n*')
    card_new_end = msg.index('СООБЩЕНИЕ\n*')
    card_new = (
        msg[card_new_start + OTRS_CONST['card_new_n']+1
        + OTRS_CONST['stars_n']+1 : card_new_end]
    )
    cards.append(clean_field(card_new))
    # all cards
    res['card'] = ", ".join(sorted([crd for crd in cards if crd]))
    # parse text
    msg_start = msg.index('СООБЩЕНИЕ\n*')
    msg_end = msg.index('ФАЙЛ\n*')
    res['text'] = (
        msg[msg_start + OTRS_CONST['msg_n']+1
        + OTRS_CONST['stars_n']+1 : msg_end]
    )
    res['text'] = clean_field(res['text'])
    # parse azs
    azs_start = msg.index('НОМЕР АЗС\n*')
    azs_end = msg.index('НОМЕР КОЛОНКИ\n*')
    res['azs'] = (
        msg[azs_start + OTRS_CONST['azs_n']+1
        + OTRS_CONST['stars_n']+1 : azs_end]
    )
    res['azs'] = clean_field(res['azs'])
    # parse trk
    trk_start = msg.index('НОМЕР КОЛОНКИ\n*')
    trk_end = msg.index('ВИД ТОПЛИВА\n*')
    res['trk'] = (
        msg[trk_start + OTRS_CONST['trk_n']+1
        + OTRS_CONST['stars_n']+1 : trk_end]
    )
    res['trk'] = clean_field(res['trk'])
    # parse fuel
    fuel_start = msg.index('ВИД ТОПЛИВА\n*')
    fuel_end = msg.index('ДАТА ПОСЕЩЕНИЯ АЗС\n*')
    res['fuel'] = (
        msg[fuel_start + OTRS_CONST['fuel_n']+1
        + OTRS_CONST['stars_n']+1 : fuel_end]
    )
    res['fuel'] = clean_field(res['fuel'])
    return res


def parse_hotline_hotline(msg: str) -> dict[str, str]:
    """Extract text from Hotline Hotline Pattern message."""
    res = {}
    # parse message content
    msg_start = msg.index('Текст сообщения:')
    msg_end = msg.index('Сообщение сгенерировано автоматически.')
    res['text'] = msg[msg_start + HOTLINE_HOTLINE_CONST['msg_n']+1 : msg_end]
    res['text'] = clean_field(res['text'])
    return res


def parse_hotline_feedback(msg: str) -> dict[str, str]:
    """Extract text from Hotline Feedback Pattern message."""
    res = {}
    # parse message content
    msg_start = msg.index('Ваше сообщение:')
    msg_end = msg.index('Я ознакомлен(-а) с положением')
    res['text'] = msg[msg_start + HOTLINE_FEEDBACK_CONST['msg_n']+1 : msg_end]
    res['text'] = clean_field(res['text'])
    return res


def parse_hotline_free(msg: str) -> dict[str, str]:
    """Extract text from Hotline Free Pattern message."""
    res = {}
    for key in HOTLINE_FREE_CONST.keys():
        if key in msg:
            # parse message content
            msg_start = msg.index(key)
            res['text'] = msg[msg_start + HOTLINE_FREE_CONST[key]['msg_n']+1 :]
            res['text'] = clean_field(res['text'])
            return res
    raise Exception('No key was found for Hotline Free Pattern message.')


def filter_standard_service_lines(text: str) -> str:
    """
    Удаляет служебные строки с маркерами, а также извлекает комментарий после 'Номер заказа:'.
    Переводы строк вставляются перед маркерами для гарантированного разделения, даже если текст "склеен".
    """
    order_marker = "Номер заказа:"
    other_markers = ["Контактный телефон:", "Номер карты", "Объект:", "Адрес:", "Отправлено"]
    special_marker = "Примечание:"
    # Вставляем перенос строки перед всеми маркерами
    for marker in other_markers + [order_marker, special_marker]:
        text = re.sub(r'\s*' + re.escape(marker), r'\n' + marker, text)
    filtered = []
    for line in text.splitlines():
        line = line.strip()
        conditions_to_skip = [
            not line,
            line.startswith(">"),
            re.match(r'^\d{2}:\d{2},\s+\d+\s+\w+\s+\d+\s+г\.,', line),
            re.search(r'<[^>]+>', line),
            "«АЗС Газпромнефть" in line,
        ]
        if any(conditions_to_skip):
            continue
        if line.startswith(order_marker):
            content = line[STANDARD_CONST['order_n']:].strip()
            if content:
                filtered.append(content)
        elif line.startswith(special_marker):
            content = line[STANDARD_CONST['special_n']:].strip()
            if content and not content.startswith("Сообщение подано"):
                filtered.append(content)
        elif any(line.startswith(m) for m in other_markers):
            continue
        else:
            filtered.append(line)
    return " ".join(filtered).strip()


def parse_standard(msg: str) -> dict[str, str]:
    """Extract text from Standard Pattern message."""
    res = {}
    pattern = r'(Напишите\s+ваши\s+пожелания.*?Нам\s+это\s+очень\s+важно\.?)'
    match = re.search(pattern, msg, flags=re.IGNORECASE | re.DOTALL)
    rest_text = msg.replace(match.group(1), "").strip() if match else msg.strip()
    res['text'] = clean_field(filter_standard_service_lines(rest_text))
    return res


def extract_udc_field(msg: str, pattern: str) -> str:
    """
    Ищет по заданному шаблону, очищает найденный текст с помощью clean_field,
    и возвращает результат, если в нём есть буквы или цифры, иначе — пустую строку.
    """
    m = re.search(pattern, msg, re.DOTALL)
    if m:
        field = clean_field(m.group(1).strip())
        return field if re.search(r'[A-Za-zА-Яа-я0-9]', field) else ""
    return ""


def parse_udc(msg: str) -> dict[str, str]:
    """Extract text from UDC Pattern message."""
    res = {}
    # parse request topic
    reason_pattern = r'Причина обращения:\s*(.*?)(?=,?\s*Номер ОРТ)'
    res['request_topic'] = extract_udc_field(msg, reason_pattern)
    # parse text
    message_pattern = r'Краткое описание обращения\(хронология\):\s*(.*?)(?=\n\n|\n>[^\n]*|\nНомер обращения:|\nС уважением|\nИнициатор:|$)'
    res['text'] = extract_udc_field(msg, message_pattern)
    # parse trk
    trk_pattern = r'Номер ТРК:\s*(.*?)(?=,?\s*Вид НП)'
    res['trk'] = extract_udc_field(msg, trk_pattern)
    # parse fuel
    fuel_pattern = r'Вид НП:\s*(.*?)(?=,?\s*Сумма внесённых денежных средств)'
    res['fuel'] = extract_udc_field(msg, fuel_pattern)
    return res


def parse_corpres(msg: str) -> dict:
    """Extract text from CorpRes Pattern message."""
    res = {}
    markers = ["Subject: [☝❗EXTERNAL❗]", "Subject: [??EXTERNAL?]", "Subject:"]
    last_pos, chosen = max(((msg.rfind(m), m) for m in markers), key=lambda x: x[0], default=(-1, None))
    text_after = msg[last_pos + len(chosen):] if chosen and last_pos != -1 else msg
    for cutoff in ["С уважением", "Отправлено", "--"]:
        pos = text_after.find(cutoff)
        if pos != -1:
            text_after = text_after[:pos]
            break
    text_after = clean_field(text_after)
    lines = [l.strip() for l in text_after.splitlines()]
    cleaned_lines = [
        line + ("" if re.search(r'[.!?]$', line) else ".")
        for line in lines if line
    ]
    res["text"] = " ".join(cleaned_lines)
    return res


def first_valid_idx(idxs: list[int], names: list[str]) -> tuple[int, str]:
    for idx, name in zip(idxs, names):
        if idx != -1:
            return idx, name
    return -1, ""


def complaint_find_azs_borders(msg: str) -> tuple[int, str, int, str]:
    azs_fc_idxs = [
        (msg.index(azs_fc) if azs_fc in msg else -1)
        for azs_fc in COMPLAINT_CONST["azs_fcs"]
    ]
    date_fc_idxs = [
        (msg.index(date_fc) if date_fc in msg else -1)
        for date_fc in COMPLAINT_CONST["date_fcs"]
    ]
    azs_idx, azs_name = first_valid_idx(azs_fc_idxs, COMPLAINT_CONST["azs_fcs"])
    d_idx, d_name = first_valid_idx(date_fc_idxs, COMPLAINT_CONST["date_fcs"])
    return azs_idx, azs_name, d_idx, d_name


def parse_complaint(msg_src: str) -> dict[str, str]:
    msg_parts = [
        part.replace("\n", "").strip()
        for part in msg_src.split("\n")
        if part.replace("\n", "").strip()
    ]
    msg = "\n".join(msg_parts)
    """Extract text from OTRS Pattern message."""
    res = {}
    # parse text
    msg_start = msg.index("Суть обращения")
    msg_end = msg.index("Принятые меры")
    res["text"] = msg[msg_start + COMPLAINT_CONST["msg_n"]+1: msg_end]
    res["text"] = clean_field(res["text"])
    # parse answer
    answer_start = msg.index("Ответ клиенту")
    res["answer"] = msg[answer_start + COMPLAINT_CONST["ans_n"]+1:]
    res["answer"] = clean_field(res["answer"])
    # parse azs
    azs_idx, azs_name, d_idx, d_name = complaint_find_azs_borders(msg)
    if all([azs_idx != -1, d_idx != -1]):
        res["azs"] = msg[azs_idx + len(azs_name) : d_idx].replace("\n", "")
        res["azs"] = clean_field(res["azs"])
    else:
        res["azs"] = ""
    return res


def parse_acc_removal(msg: str) -> dict[str, str]:
    res = {}
    # parse cards
    cards_none_field = "Карты лояльности отсутствуют"
    if cards_none_field in msg:
        res["card"] = ""
    else:
        cards = []
        for numb in range(1, 2+1):
            field = f"Номер карты лояльности №{numb}:"
            if field not in msg:
                break
            else:
                card_start = msg.index(field)
                idx = card_start + 1
                while msg[idx] != "\n":
                    idx += 1
                card_end = idx
                card = msg[card_start+ACCREM_CONST["card_n"]+1 : card_end]
                cards.append(card.strip())
        res["card"] = ", ".join(cards)
    # parse phone
    phone_pattern = r'\b[78]\d{10}\b'
    res["phone"] = re.findall(phone_pattern, msg)[0]
    # parse text
    res["text"] = ""
    return res


PARSERS = {
    'OTRS': parse_otrs,
    'HotlineHotline': parse_hotline_hotline,
    'HotlineFeedback': parse_hotline_feedback,
    'HotlineFree': parse_hotline_free,
    'Standard': parse_standard,
    'UDC': parse_udc,
    'CorpRes': parse_corpres,
    'ComplaintBook': parse_complaint,
    'AccRemoval': parse_acc_removal,
}


PARSABLE = {
    "OTRS", "HotlineHotline", "HotlineFeedback", "HotlineFree",
    "UDC", "CorpRes", "ComplaintBook", "AccRemoval",
}


def parse_msg(pat_name: str, msg: str) -> tuple[str, dict[str, str]]:
    """Return parsed text and initial fields."""
    if pat_name in PARSABLE:
        parsed_fields = PARSERS[pat_name](msg)
    elif pat_name in ["NoText", "HotlineEmpty"]:
        parsed_fields = {"text": ""}
    else:
        parsed_fields = {"text": msg}
    parsed_text = clean_field(parsed_fields["text"])
    del parsed_fields["text"]
    return parsed_text, parsed_fields
