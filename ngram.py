import sys
import re

n = int(sys.argv[1])
m = int(sys.argv[2])
text_names = []
raw_texts = []
ngram_tables = {}
for n0 in range(n):
    ngram_tables[n0] = {}

print(sys.argv)
for i in range(3, len(sys.argv)):
    text_names.append(sys.argv[i])

print(text_names)


for t in text_names:
    temp_file = open(t,"r",encoding='utf-8')
    raw_texts.append(temp_file.read())

for r in raw_texts:
    r = re.sub("\n", " ", r)
    sents = re.split(r"[.!?]", r)

    for sent in sents:
        toks = sent.split(" ")
        final_toks = []
        for t in toks:
            punct = re.search(r"([\“\"—,:;\-\)\(\`/_’])", t)
            if punct:
                for g in range(len(punct.groups())):
                    if punct.group(g).strip() != "":
                        final_toks.append(punct.group(g).strip())

            else:
                if t.strip() != "":
                    final_toks.append(t.strip())
        if len(final_toks) >= n:
            for n0 in range(n):
                for i in range(len(final_toks)):
                    if i+n0<len(final_toks):
                        if " ".join(final_toks[0:n0+1]) not in ngram_tables[n0]:
                            ngram_tables[n0][" ".join(final_toks[0:n0+1])] = 1
                        else:
                            ngram_tables[n0][" ".join(final_toks[0:n0 + 1])] += 1
print(ngram_tables)
            ## create tables here, let's not waste memory