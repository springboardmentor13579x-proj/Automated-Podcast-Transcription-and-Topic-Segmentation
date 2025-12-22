import re

input_file = "../ground_truth/pg1661.txt"
output_file = "../ground_truth/pg1661_clean.txt"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Remove Gutenberg header & footer
start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")

clean_text = text[start:end]

# Remove extra spaces
clean_text = re.sub(r'\n{2,}', '\n\n', clean_text)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(clean_text)

print("Cleaned text saved as pg1661_clean.txt")