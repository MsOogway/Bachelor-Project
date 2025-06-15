import ollama
import pypdf
import time
from pypdf import PdfReader

#Splits file into pages
def read_files(pdf_file):
    pages = []

    with open(pdf_file, "rb") as file:
        reader = PdfReader(file)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)
                #print(text)
                #print("\n\n Next page\n\n")

    return pages

# Runs the ollama model and takes in keyword to search through each page
def find_prompt(pages, prompt):
    result = []

    for index, page in enumerate(pages):

        newPrompt =     f"Based on this text from page {index+1}, answer the question: '{prompt}' If no answer is found, say so. Be specific. Text: {page}"

        response = ollama.chat(model="mistral", messages=[
            {"role": "user", "content": newPrompt}
        ])

        reply = response['message']['content']

        
        result.append(f"--- Page {index + 1} ---\n{reply.strip()}\n")
        
    return result


pdf_file = ""
prompt = "exit"

print("Reading file(s)...")
start_read = time.time()
pages = read_files(pdf_file)
end_read = time.time()
print(f"Done with making pages in {end_read - start_read:.2f} seconds")

while True:
    prompt = input("\n Enter what question you want the model to search for (or type exit to quit): ").strip()
    if prompt.lower() == "exit":
        break

    print(f"\n {prompt}\n")
    start_search = time.time()
    results = find_prompt(pages, prompt)
    end_search = time.time()

    if results:
        print(" Keyword found in the following chunks:\n")
        for r in results:
            print(r)

    else:
        print(" No results found.")

    print(f"\nTime to search was: {end_search - start_search:.2f} seconds.\n")
