import os

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')

from dotenv import load_dotenv
load_dotenv()

import pinecone
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment=os.environ.get("PINECONE_ENVIRONMENT"))

PINECONE_INDEX = "kotlang-vectordb"
PINECONE_COLLECTION = "medical-ert-guideline"
# pinecone.create_index(name=PINECONE_INDEX, dimension=768, metric="cosine")
index = pinecone.Index(PINECONE_INDEX)


def __get_keyword__(filename):
    keyword = filename.split(".")[0]
    keyword = keyword.replace("_", " ").replace("-", " ")
    keyword = keyword.\
        replace("guidelines", "").\
        replace("guideline", "").\
        replace("chart", "").\
        replace("factsheet", "").\
        replace("Guideline", "").\
        replace("Fact sheet", "")

    keyword = keyword.lower()
    if "poisoning" not in keyword:
        keyword = keyword.strip() + " poisoning"

    return keyword.strip()


def embed_file(file_path="MedicalHistoryPreProcessed/Camphor Poisoning.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
        paras_original = file_content.split("\n\n")

        filename = os.path.basename(file_path)
        keyword = __get_keyword__(filename)
        paras_for_embedding = [keyword + " " + x for x in paras_original]

        if len(paras_for_embedding) == 0:
            print("No paras in " + file_path)
            return []

        print("Embedding " + filename)
        para_embeddings = model.encode(paras_for_embedding)
        print("Embedding Finished. Vector Size : " + str(len(para_embeddings[0])))

        pinecone_requests = []
        idx = 0

        for vec, text in zip(para_embeddings, paras_original):
            pinecone_request = {
                'id': keyword + "-" + str(idx),
                'values': vec.tolist(),
                'metadata': {'text': text, 'reference': filename.replace(".txt", ".pdf")}
            }

            pinecone_requests.append(pinecone_request)
            idx += 1

        upsert_response = index.upsert(
            vectors=pinecone_requests,
            namespace=PINECONE_COLLECTION)

        print(upsert_response)
        return para_embeddings


if __name__ == '__main__':
    base_path = "MedicalHistoryPreProcessed/"
    file_list = os.listdir(base_path)

    for file in file_list:
        embed_file(base_path + file)
