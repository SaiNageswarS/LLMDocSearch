import tika
tika.initVM()
from tika import parser


def __sanitize_column_page_breaks__(paragraphs: [str]):
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

        cleaned_paras.append(para)

    return cleaned_paras


def __sanitize_word_breaks__(paragraph: str):
    lines = paragraph.split("\n")
    cleaned_para = ""

    for line in lines:
        if cleaned_para.endswith("-"):
            cleaned_para = cleaned_para[0:len(cleaned_para)-1] + line
        else:
            cleaned_para = cleaned_para + " " + line

    return cleaned_para


def __get_clean_paragraphs__(content: str):
    if content is None or len(content) == 0:
        return []

    paragraphs = content.split("\n\n")

    paragraphs = [x for x in paragraphs if len(x.strip()) > 0]
    print("Initial para count: " + str(len(paragraphs)))

    paragraphs = __sanitize_column_page_breaks__(paragraphs)
    paragraphs = [__sanitize_word_breaks__(x) for x in paragraphs]
    print("After sanitizing breaks: " + str(len(paragraphs)))

    paragraphs = [x for x in paragraphs if len(x) > 50]
    print("After sanitizing length: " + str(len(paragraphs)) + "\n\n")

    return paragraphs


def chunk_pdf(pdf_path="MedicalHistory/Camphor Poisoning.pdf"):
    print(pdf_path)
    parsed_pdf = parser.from_file(pdf_path)
    content = parsed_pdf["content"]
    paragraphs = __get_clean_paragraphs__(content)
    return paragraphs

