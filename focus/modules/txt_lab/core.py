
from .struct import Text, Entity


def concat(first: Text, second: Text, sep: str = ' ') -> Text:
    """Concatenates two `Text` objects and returns a new instance.

    Args:
        first: The first Text object to concatenate.
        second: The second Text object to concatenate. Its entities'
            positions will be shifted by the length of the first text.
        sep: Separator to add between first and second text.

    Returns:
        A new Text instance containing:
        - Combined text (first.text + sep + second.text)
        - All entities from both texts (with second's entities positions adjusted)
    """
    combined_text = f'{first.text}{sep}{second.text}'
    shift = len(first.text) + len(sep)
    first_entities = first.entities.copy()
    second_entities = [
        Entity(beg=entity.beg + shift, end=entity.end + shift, cat=entity.cat)
        for entity in second.entities
    ]
    return Text(
        text=combined_text,
        entities=first_entities + second_entities
    )


def split_by_idx(text: Text, split_idx: int) -> tuple[Text, Text]:
    """Splits a `Text` at the specified space character into two parts.
    
    The character at split_idx will be removed. Entities are divided between
    the two parts, with those in the right part having their positions adjusted.
    Entities spanning the split point are divided into two separate entities.
    
    Args:
        text: The `Text` object to split.
        split_idx: The index of the character where the split should occur.
            The character at this index will be removed.
    
    Returns:
        A tuple containing:
        - Left Text (text before the split_idx)
        - Right Text (text after the split_idx, with positions adjusted)
    
    Raises:
        ValueError: If split_idx is invalid (negative, out of bounds, or not pointing to a space or '\n').
    """
    if split_idx < 0 or split_idx >= len(text.text) or (text.text[split_idx] not in [' ', '\n']):
        raise ValueError("split_idx must point to a valid space or '\\n' character in the text")
    left_text = text.text[:split_idx]
    right_text = text.text[split_idx + 1:]
    left_entities = []
    right_entities = []
    for entity in text.entities:
        if entity.end <= split_idx:
            # Entity is completely in the left part
            left_entities.append(entity)
        elif entity.beg >= split_idx + 1:
            # Entity is completely in the right part (shifted)
            right_entities.append(Entity(
                beg=entity.beg - (split_idx + 1),
                end=entity.end - (split_idx + 1),
                cat=entity.cat
            ))
        else:
            # Entity spans across the split point - need to split it
            if entity.beg < split_idx:
                left_entities.append(Entity(
                    beg=entity.beg,
                    end=split_idx,
                    cat=entity.cat
                ))
            if entity.end > split_idx + 1:
                right_entities.append(Entity(
                    beg=0,  # Starts at beginning of right part
                    end=entity.end - (split_idx + 1),
                    cat=entity.cat
                ))
    left_part = Text(text=left_text, entities=left_entities)
    right_part = Text(text=right_text, entities=right_entities)
    return left_part, right_part


def insert(first: Text, second: Text, space_idx: int, sep: str = ' ') -> Text:
    """Inserts the second labeled text into the first one at the specified space index.

    Args:
        first: The `Text` object to insert into.
        second: The `Text` object to be inserted.
        space_idx: The index of the space character (in first.text) where insertion should occur.
            The space character at this index will be replaced by the second text.

    Returns:
        A new `Text` instance with the second text inserted at the specified position,
        with all entities properly adjusted.

    Raises:
        ValueError: If space_idx is invalid (negative, out of bounds, or not pointing to a space).
    """
    left_part, right_part = split_by_idx(first, space_idx)
    temp = concat(left_part, second)
    result = concat(temp, right_part, sep)
    return result


def split_by_symbol(text: Text, symbol: str) -> list[Text]:
    """Splits a `Text` into multiple `Text` objects by given symbol.
    
    Each `symbol` is removed during splitting.
    
    Args:
        text: The `Text` object to split.
    
    Returns:
        A list of `Text` objects.
        `symbol` characters are not included in the resulting texts.

    Raises:
        ValueError: If `symbol` is not pointing to a space or '\n'.
    """
    result = []
    current_text = text
    while True:
        split_pos = current_text.text.find(symbol)
        if split_pos == -1:
            result.append(current_text)
            break
        left_part, right_part = split_by_idx(current_text, split_pos)
        result.append(left_part)
        current_text = right_part
    return result


def concat_list(texts: list[Text], sep: str = ' ') -> Text:
    """Concatenates a list of `Text` objects into a single `Text`.
    
    Args:
        texts: List of `Text` objects to concatenate.
        sep: Separator to add between consecutive texts.
    
    Returns:
        A new `Text` instance containing:
        - Combined text from all input texts (with separators in between)
        - All entities from all texts with proper position adjustments
    """
    if not texts:
        return Text("", [])
    result = texts[0]
    for text in texts[1:]:
        result = concat(result, text, sep)
    return result


def split_by_indices(text: Text, split_indices: list[int]) -> list[Text]:
    """Splits a `Text` into multiple parts at specified indices.
    
    The characters at split indices will be removed. Entities are divided between
    the parts, with positions adjusted accordingly. Entities spanning split points
    are divided into separate entities for each part.
    
    Args:
        text: The `Text` object to split.
        split_indices: List of indices where splits should occur (must be sorted in ascending order).
            The characters at these indices will be removed.
    
    Returns:
        A list of `Text` objects resulting from the splits.
    
    Raises:
        ValueError: If any split index is invalid (negative, out of bounds, or not
            pointing to space/newline), or if indices are not in ascending order.
    """
    if any(i >= j for i, j in zip(split_indices, split_indices[1:])):
        raise ValueError("Split indices must be in strictly ascending order")
    current_text = text
    result = []
    cumulative_shift = 0
    for split_idx in split_indices:
        adjusted_idx = split_idx - cumulative_shift
        left_part, right_part = split_by_idx(current_text, adjusted_idx)
        result.append(left_part)
        current_text = right_part
        cumulative_shift += len(left_part.text) + 1  # +1 for the removed character
    result.append(current_text)
    return result


def drop_empty_lines(text: Text) -> Text:
    """Removes empty lines from text.

    Args:
        text: A Text object

    Returns:
        A new Text object with entities whose cats are not in the drop set.
    """
    lines = split_by_symbol(text, "\n")
    lines_text = [line for line in lines if line.text.strip(" \t")]
    return concat_list(lines_text, sep="\n")


def drop_cats(text: Text, drop: set[str], drop_empty: bool = True) -> Text:
    """Filters out entities of specified categories while preserving text structure.

    Args:
        text: A Text object containing the original text and its entity annotations
        drop: A set of category strings to filter out from the entities
        drop_empty: Flag either to drop empty lines. Default: True.

    Returns:
        A new Text object with entities whose cats are not in the drop set.
    """
    new_text = ""
    new_ents = []
    old_left = 0
    for ent in text.entities:
        if ent.beg != old_left:
            new_text = f"{new_text}{text.text[old_left:ent.beg]}"
        old_left = ent.beg
        if ent.cat not in drop:
            cat_beg = len(new_text)
            new_text = f"{new_text}{text.text[ent.beg:ent.end]}"
            keep_ent = Entity(cat_beg, len(new_text), ent.cat)
            new_ents.append(keep_ent)
        old_left = ent.end
    new_text = f"{new_text}{text.text[old_left:]}"
    new_text_lab = Text(new_text, new_ents)
    if drop_empty:
        new_text_lab = drop_empty_lines(new_text_lab)
    return new_text_lab
