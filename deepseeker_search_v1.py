import ollama
import pypdf
import time
from pypdf import PdfReader

def read_files(pdf_file):
    pages = []

    with open(pdf_file, "rb") as file:
        reader = PdfReader(file)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)
                print(text)
                print("\n\n Next page\n\n")

    return pages


def find_keyword(pages, keyword):
    result = []

    for index, page in enumerate(pages):
        prompt = f"Does this text mention or diskuss the keyword '{keyword}'? If yes, return the sentence(s) or paragraph(s) with it: \n\n{page}"

        response = ollama.chat(model="deepseek-r1", messages=[
            {"role": "user", "content": prompt}
        ])

        reply = response['message']['content']

        if "Yes, the keyword" in reply:
            clean_start = reply.find("Yes, the keyword")
            cleaned_reply = reply[clean_start:].strip()
            result.append(f"--- Page {index + 1} ---\n{cleaned_reply}\n")

        elif keyword.lower() in reply.lower():
            # fallback if structure is different
            result.append(f"--- Page {index + 1} ---\n{reply.strip()}\n")

    return result


pdf_file = "report1.pdf"
keyword = ""


print("Reading file(s)...")
start_read = time.time()
pages = read_files(pdf_file)
end_read = time.time()
print(f"Done with making pages in {end_read - start_read:.2f} seconds")


while True:
    keyword = input("\n Enter what word to search for (or type exit to quit): ").strip()
    if keyword.lower() == "exit":
        break

    print(f"\n Searching for: {keyword}...\n")
    start_search = time.time()
    results = find_keyword(pages, keyword)
    end_search = time.time()

    if results:
        print(" Keyword found in the following chunks:\n")
        for r in results:
            print(r)

    else:
        print(" No results found.")

    print(f"\nTime to search was: {end_search - start_search:.2f} seconds.\n")
