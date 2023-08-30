import numpy as np

from EmbedUtil import model, index, PINECONE_COLLECTION
from sentence_transformers import CrossEncoder

re_ranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')
from transformers import pipeline
text2text_generator = pipeline("text2text-generation")


def search(query: str):
    query_embedding = model.encode(query.lower())
    res = index.query(
        vector=query_embedding.tolist(),
        top_k=100,
        namespace=PINECONE_COLLECTION,
        include_values=True,
        include_metadata=True
    )

    # re-rank documents.
    re_ranker_input = [[query, m.metadata['text']] for m in res.matches]
    scores = re_ranker.predict(re_ranker_input)
    score_ranking = np.argsort(scores)[::-1]

    context_arr = [res.matches[x].metadata['text'] for x in score_ranking[:10]]
    references = set([res.matches[x].metadata['reference'] for x in score_ranking[:10]])

    context = ". ".join(context_arr)

    answers = text2text_generator("question: " + query + " context: " + context)
    return answers, references, context


if __name__ == '__main__':
    query = "What dose of Diphenhydramine is toxic and what could be the outcomes"
    search(query)


