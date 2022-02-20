import sys

n = sys.argv[1]
m = sys.argv[2]
text_names = []
raw_texts = []
ngram_tables = {}
print(sys.argv)
for i in range(3, len(sys.argv)):
    text_names.append(sys.argv[i])

print(text_names)


for t in text_names:
    temp_file = open("r", t)
    raw_texts.append(temp_file.read())

for r in raw_texts:
    sent = r.split(r'[.!?]')
    toks = sent.split(" ")
    for t in toks:

