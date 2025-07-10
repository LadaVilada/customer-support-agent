from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher
from .config import SIMILARITY_THRESHOLD

def find_best_match(user_input: str, qa_data: List[Dict[str, str]], threshold: float = SIMILARITY_THRESHOLD) -> Tuple[Optional[str], float]:
    """
    Find the best matching FAQ answer for the user input using fuzzy string matching.
    Args:
        user_input: The user's question.
        qa_data: List of Q&A dicts.
        threshold: Similarity threshold for a match.
    Returns:
        (answer, score) if match found, else (None, best_score)
    """
    best_score = 0.0
    best_answer = None
    for qa in qa_data:
        score = SequenceMatcher(None, user_input.lower(), qa["question"].lower()).ratio()
        if score > best_score:
            best_score = score
            best_answer = qa["answer"]
    if best_score >= threshold:
        return best_answer, best_score
    return None, best_score 