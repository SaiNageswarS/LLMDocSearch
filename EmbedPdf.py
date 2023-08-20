import os
from ChunkPdf import chunk_pdf


def __process_pdfs_to_txt__(base_path="MedicalHistory/"):
    file_list = os.listdir(base_path)
    pdf_file_list = [x for x in file_list if x.endswith(".pdf")]
    chunked_files = [chunk_pdf(base_path + x) for x in pdf_file_list]

    if not os.path.exists("MedicalHistoryPreProcessed"):
        os.makedirs("MedicalHistoryPreProcessed")

    for filename, chunked_file in zip(pdf_file_list, chunked_files):
        with open("MedicalHistoryPreProcessed/" + filename.replace(".pdf", ".txt"), "w", encoding="utf-8") as output_file:
            for para in chunked_file:
                output_file.write(para)
                output_file.write("\n\n")

    return chunked_files


def embed_pdfs():
    __process_pdfs_to_txt__()


if __name__ == '__main__':
    embed_pdfs()
