import sys
import re
import random

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
        final_toks.append("BOS")
        for t in toks:
            punct = re.search(r"([\“\"—,:;\-\)\(\`/_’])", t)
            if punct:
                for g in range(len(punct.groups())):
                    if punct.group(g).strip() != "":
                        final_toks.append(punct.group(g).strip())

            else:
                if t.strip() != "":
                    final_toks.append(t.strip())
        final_toks.append("EOS")
        if len(final_toks) >= n:
            for n0 in range(n):
                for i in range(len(final_toks)):
                    if i+n0<len(final_toks):
                        if " ".join(final_toks[i:i+n0+1]) not in ngram_tables[n0]:
                            ngram_tables[n0][" ".join(final_toks[i:i+n0+1])] = 1
                        else:
                            ngram_tables[n0][" ".join(final_toks[i:i+n0+1])] += 1
print(len(ngram_tables))
for i in range(m):

    if (n>1):
        options = {}
        toks = []
        toks.append("BOS")
        for k in ngram_tables[1]:

            if k.split(" ")[0] == "BOS":
                options[k] = ngram_tables[1][k]
        choice = random.choices(list(options.keys()), weights=list(options.values()), k=1)[0].split(" ")[-1]
        toks.append(choice)
        while choice != "EOS":
            options = {}
            prev=[]
            if len(toks)> (n-1):
                prev=" ".join(toks[len(toks)-(n-1):])
                for k in ngram_tables[n-1]:
                    if k.startswith(prev):
                        options[k] = ngram_tables[n-1][k]
                choice = random.choices(list(options.keys()), weights=list(options.values()), k=1)[0].split(" ")[-1]
                toks.append(choice)

            else:
                prev = " ".join(toks)
                for k in ngram_tables[len(toks)]:
                    if k.startswith(prev):
                        options[k] = ngram_tables[len(toks)][k]
                choice = random.choices(list(options.keys()), weights=list(options.values()), k=1)[0].split(" ")[-1]
                toks.append(choice)
        print(" ".join(toks))






