import sys
import os
from EmbedUtil import model, index, PINECONE_COLLECTION
import cohere
co = cohere.Client(os.environ.get("COHERE_API_KEY"))


def search(query: str):
    query_embedding = model.encode(query.lower())
    res = index.query(
        vector=query_embedding.tolist(),
        top_k=50,
        namespace=PINECONE_COLLECTION,
        include_values=True,
        include_metadata=True
    )

    # for match in res.matches:
    #    print(match.metadata)
    documents = [m.metadata for m in res.matches]
    re_rank_res = co.rerank(query=query, documents=documents, top_n=10, model="rerank-english-v2.0")

    context_arr = [rankedRes.document["text"] for rankedRes in re_rank_res.results]
    references = set([rankedRes.document["reference"] for rankedRes in re_rank_res.results])

    context = ". ".join(context_arr)

    # prepare prompt
    prompt = f"""
        Excerpt from an article: 
        {context}
        Question: {query}

        Extract the answer of the question from the text provided. 
        If the text doesn't contain the answer, 
        reply that the answer is not available."""

    prediction = co.generate(
        prompt=prompt,
        max_tokens=1024,
        model="command-nightly",
        temperature=0.5,
        num_generations=3
    )

    answer = "answer is not available"
    for gen in prediction.generations:
        if "answer is not available" in gen:
            continue

        if len(gen) > len(answer):
            answer = gen

    return answer, references, context


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python search.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    search(query)
