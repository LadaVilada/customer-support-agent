import difflib
from typing import List, Dict, Tuple, Optional

def find_best_match(user_input: str, qa_data: List[Dict[str, str]], threshold: float = 0.75) -> Tuple[Optional[str], float]:
    """
    Returns the answer and similarity score if a match is found above the threshold, else (None, 0.0)
    """
    best_score = 0.0
    best_answer = None
    for qa in qa_data:
        score = difflib.SequenceMatcher(None, user_input.lower(), qa["question"].lower()).ratio()
        if score > best_score:
            best_score = score
            best_answer = qa["answer"]
    if best_score >= threshold:
        return best_answer, best_score
    return None, best_score 