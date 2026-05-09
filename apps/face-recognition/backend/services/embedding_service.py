import numpy as np

from core.models import known_embeddings
from utils.similarity import cosine_similarity


def find_embedding_match(embedding):

    best_match_name = "Unknown"

    best_similarity = 0

    for data in known_embeddings:

        similarity = cosine_similarity(

            embedding,
            data["embedding"]
        )

        if similarity > best_similarity:

            best_similarity = similarity

            best_match_name = data["name"]

    if best_similarity < 0.55:

        return "Unknown", best_similarity

    return best_match_name, best_similarity