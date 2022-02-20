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
    sents = r.split(r"[.!?]", r)

    for sent in sents:
        toks = sent.split(" ")
        final_toks = []
        for t in toks:
            punct = t.search(r"([,:;-])")
            if punct:
                temp = t.split(t.group(1))
                if (len(temp)!=1):
                    final_toks.append(temp[0])
                    final_toks.append(t.group(1))
                    final_toks.append(temp[1])
                elif t.beginswith(",") or t.beginswith(":") or t.beginswith(";") or t.beginswith("-"):
                    final_toks.append(t[0])
                    final_toks.append(t[1:])
                else:
                    final_toks.append(t[0:(len(t)-1)])
                    final_toks.append(t[len(t)-1])

            else:
                final_toks.append(t)
        if len(final_toks) >= n:
            ## create tables here, let's not waste memory