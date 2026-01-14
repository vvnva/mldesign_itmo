
import re


def remove_links(text: str) -> str:
    """Remove HTTP/HTTPS links from the input text."""
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.sub('', text)


def remove_digits_in_brackets(text: str) -> str:
    """Remove all occurrences of [digits] from the text."""
    return re.sub(r'\[\d+\]', '', text)


REM_SYMBOLS = ["\xa0", ">", "<", "❗", "☝", "[", "]"]
TRANS_TABLE = str.maketrans('', '', "".join(REM_SYMBOLS))

def remove_symbols(text: str) -> str:
    return text.translate(TRANS_TABLE)


FILES_EXTS = ["pdf", "png", "jpg"]

def remove_filenames(text: str) -> str:
    ext_pattern = "|".join(re.escape(ext) for ext in FILES_EXTS)
    pattern = re.compile(
        rf"\b[\w\-\_]+\.({ext_pattern})\b", 
        re.VERBOSE | re.IGNORECASE
    )
    cleaned = pattern.sub('', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)  # normalize spaces
    return cleaned.strip()


def remove_substrings(text: str) -> str:
    subs = ["EXTERNAL"]
    res = text
    for s in subs:
        res = res.replace(s, "")
    return res
    

TEXT_TRANSFORMS = [
    remove_links,
    remove_digits_in_brackets,
    remove_symbols,
    remove_filenames,
    remove_substrings,
]


def clear_text(text: str) -> str:
    res = text
    for tr in TEXT_TRANSFORMS:
        res = tr(res)
    return res.strip(" \t")
