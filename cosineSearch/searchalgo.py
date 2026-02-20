import math

# -------------------------------
# Sample embeddings
# -------------------------------
E = {
    "king": [0.9, 0.8, 0.1, 0.0],
    "queen": [0.88, 0.82, 0.12, 0.02],
    "man": [0.75, 0.60, 0.05, -0.02],
    "woman": [0.72, 0.62, 0.07, 0.00],
    "chef": [0.10, 0.22, 0.85, 0.40]
}

# -------------------------------
# Cosine Similarity
# -------------------------------
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


# -------------------------------
# Euclidean Distance
# -------------------------------
def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# -------------------------------
# Dot Product
# -------------------------------
def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))


# -------------------------------
# Search Function
# -------------------------------
def nearest_neighbors(query_word, metric="cosine"):
    results = []

    for word, vector in E.items():
        if word != query_word:

            if metric == "cosine":
                score = cosine_similarity(E[query_word], vector)

            elif metric == "euclidean":
                score = euclidean_distance(E[query_word], vector)

            elif metric == "dot":
                score = dot_product(E[query_word], vector)

            results.append((word, score))

    # Sorting logic
    if metric in ["cosine", "dot"]:
        results = sorted(results, key=lambda x: x[1], reverse=True)
    else:
        results = sorted(results, key=lambda x: x[1])

    return results


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    print("Cosine Search:")
    print(nearest_neighbors("queen", "cosine"))
    print()

    print("Euclidean Search:")
    print(nearest_neighbors("queen", "euclidean"))
    print()

    print("Dot Product Search:")
    print(nearest_neighbors("queen", "dot"))
