import os

import tika
tika.initVM()
from tika import parser

from typing import List


def __sanitize_column_page_breaks__(paragraphs: List[str]):
    cleaned_paras = []

    for para in paragraphs:
        # if first character of para is lower, then it is a column break or page break.
        # append it to earlier para.
        if len(cleaned_paras) > 0 and para[0].islower():
            last_para = cleaned_paras[len(cleaned_paras) - 1]

            if last_para.endswith("-"):
                last_para = last_para[0:len(last_para) - 1] + para
            else:
                last_para = last_para + " " + para

            cleaned_paras[len(cleaned_paras) - 1] = last_para
            continue
        elif len(cleaned_paras) > 0 and para[0] == '(':
            last_para = cleaned_paras[len(cleaned_paras) - 1]
            last_para = last_para + " " + para

            cleaned_paras[len(cleaned_paras) - 1] = last_para
            continue
        # bullets of same context
        elif len(cleaned_paras) > 0 and cleaned_paras[len(cleaned_paras) - 1][0].isdigit() and para[0].isdigit():
            last_para = cleaned_paras[len(cleaned_paras) - 1]
            last_para = last_para + " " + para

            cleaned_paras[len(cleaned_paras) - 1] = last_para
            continue

        cleaned_paras.append(para)

    return cleaned_paras


def __sanitize_word_breaks__(paragraph: str):
    lines = paragraph.split("\n")
    cleaned_para = ""

    for line in lines:
        if cleaned_para.endswith("-"):
            cleaned_para = cleaned_para[0:len(cleaned_para) - 1] + line
        else:
            cleaned_para = cleaned_para + " " + line

    return cleaned_para.strip()


def __remove_references__(paragraphs: List[str]):
    res = []

    for para in paragraphs:
        if para.startswith("REFERENCES"):
            break

        res.append(para)

    return res


def __get_clean_paragraphs__(content: str):
    if content is None or len(content) == 0:
        return []

    paragraphs = content.split("\n\n")

    paragraphs = [x for x in paragraphs if len(x.strip()) > 0]
    print("Initial para count: " + str(len(paragraphs)))

    paragraphs = __sanitize_column_page_breaks__(paragraphs)
    paragraphs = [__sanitize_word_breaks__(x) for x in paragraphs]
    print("After sanitizing breaks: " + str(len(paragraphs)))

    # remove paragraphs with length less than 3 times standard deviation from mean.
    # para_len_arr = np.array([len(x) for x in paragraphs])
    # mean_length = np.mean(para_len_arr)
    # std_deviation = np.std(para_len_arr)
    min_length = 100

    # print("Mean para length " + str(mean_length) + " Std para length " + str(std_deviation))
    print("Discarding all paragraphs of length less than " + str(min_length))

    paragraphs = [x for x in paragraphs if len(x) > min_length]
    paragraphs = [x for x in paragraphs if not x.lower().startswith("disclaimer")]
    paragraphs = [x for x in paragraphs if not ("©" in x.lower() or "copyright" in x.lower())]
    paragraphs = [x for x in paragraphs if "to cite this article" not in x.lower()]
    paragraphs = [x for x in paragraphs if "this article maybe used for" not in x.lower()]
    paragraphs = [x for x in paragraphs if "the publisher does not give any warranty" not in x.lower()]
    paragraphs = [x for x in paragraphs if "address correspondence to american association" not in x.lower()]

    paragraphs = __remove_references__(paragraphs)
    print("After sanitizing length: " + str(len(paragraphs)) + "\n\n")

    return paragraphs


def chunk_pdf(pdf_path="MedicalHistory/Camphor Poisoning.pdf"):
    print(pdf_path)
    parsed_pdf = parser.from_file(pdf_path)
    content = parsed_pdf["content"]
    paragraphs = __get_clean_paragraphs__(content)

    return paragraphs


if __name__ == '__main__':
    base_path = "MedicalHistory/"
    file_list = os.listdir(base_path)
    pdf_file_list = [x for x in file_list if x.endswith(".pdf")]
    chunked_files = [chunk_pdf(base_path + x) for x in pdf_file_list]

    if not os.path.exists("MedicalHistoryPreProcessed"):
        os.makedirs("MedicalHistoryPreProcessed")

    for filename, chunked_file in zip(pdf_file_list, chunked_files):
        with open("MedicalHistoryPreProcessed/" + filename.replace(".pdf", ".txt"), "w",
                  encoding="utf-8") as output_file:
            for para in chunked_file:
                output_file.write(para)
                output_file.write("\n\n")
