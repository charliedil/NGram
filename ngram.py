"""
Charlie Dil - 2/22/2022 - Ngram project

Problem: Can we generate sentences by feeding a program texts from which it will learn the frequency of certain
"n"-word phrases, which it will then use to generate sentences? Apparently we can, to varying degrees of success

Usage Instructions: Run this program from the command line using a python3.10 venv. You must provide n (which ngram model
to use? Unigram? Bigram? Up to you.), m (number of sentences to generate), and a list of filepaths to the txt files
that you want this model to be based upon separated by spaces like so:

python ngram.py n m path/to/file1.txt path/to/file2.txt

But, replace n with your desired number for the ngrams and m for the desired sentences.


Example run:
INPUT:
python ngram.py 5 3 "w_and_p.txt" "c_and_p.txt" "ak.txt"

OUTPUT:
Howdy there! This program utilizes an N-gram model for sentence generation.
Provide the desired value of n, the number of sentences you want, and the texts you would like this to be based on.
Written by Charlie Dil
Command line options: ngram.py 5 3
--------------------------------------------------------------------------------------------------------------------
” said stepan arkadyevitch playfully
more than once they had made him drunk on champagne and , which he could not accustom himself
i will , that i may know what to do

Algorithm: First, I split the text by [.?!] because one of the assumptions we are allowed to make is that sentences
will end with these. We are not concerned with edge cases. I then tokenize these sentences into... well, tokens. These
tokens can be numbers, words (or word-like), and other non-delimiting punctuation. I create a giant dictionary with
n keys. The value of each of these keys is yet another dictionary for each ngram frequency table. I add to these one
sentence at a time. Any sentence with less than n tokens is dropped because we are told to, and it makes everything
much simpler. I preprend "BOS" (beginning of sentence) token to all sentences, and I append "EOS" (end of sentence)
token to all sentences. Once the tables are generated, we begin generating sentences. I start with "BOS" and (if n>1)
I look at the bigram table and pull the frequencies and associated phrases. I use random.choices() to randomly choose
which bigram to go with. I use the frequencies as weights for the funtion, so it is more likely to go with something
common. We continue to use the accumulated phrase for picking the next word until we hit n, upon which we begin using
the latest n words for next word generation. We stop once the "EOS" token is chosen. Once this happens, we print the
sentence, and repeat this process m-1 more times. If n==1, then we simply choose from the unigram table randomly
over and over until "EOS" is picked. Note that with n==1, values of "BOS" that are chosen before "EOS" and after
the inital "BOS" are ignored.
"""





import sys
import re
import random

## Intro prints
print("Howdy there! This program utilizes an N-gram model for sentence generation.")
print("Provide the desired value of n, the number of sentences you want, and the texts you would like this to be based on.\nWritten by Charlie Dil")
n = int(sys.argv[1])## save command line args
m = int(sys.argv[2])

print("Command line options: ngram.py %d %d" % (n, m))
print("--------------------------------------------------------------------------------------------------------------------")

text_names = [] # Used for storing all the textfile paths
raw_texts = [] # Used to store the raw strings returned from reading the files
ngram_tables = {} # used to store the n gram freq tables
for n0 in range(n):
    ngram_tables[n0] = {} # we want n different freq tables, that's what is initialized here

# let's get those text files in!
for i in range(3, len(sys.argv)):
    text_names.append(sys.argv[i])

# reading the text files
for t in text_names:
    temp_file = open(t,"r",encoding='utf-8')
    raw_texts.append(temp_file.read())

for r in raw_texts:
    r = re.sub("\n", " ", r) # turning new lines into spaces for simplicity
    sents = re.split(r"[.!?]", r) # split sentences by . ! or ?

    for sent in sents:
        toks = sent.lower().split(" ") # tokens are white space delimited, for the most part. Handle punct later

        final_toks = [] # tokenized sentence for ngram parsing stored here.
        final_toks.append("BOS") # sentence starts with BOS token
        for t in toks:
            punct = re.search(r"([\“\"—,:;\-\)\(\`/_’])", t) # does our token have punct?
            if punct:
                for g in range(len(punct.groups())): # we want to break it into separate tokens
                    if punct.group(g).strip() != "": # there was a weird edge case of empty strings, this catches that
                        final_toks.append(punct.group(g).strip()) # appending the segemented token here

            else:
                if t.strip() != "": # same weird edge case
                    final_toks.append(t.strip()) # if no punct, we can just add it as is (whitespace stripped though)
        final_toks.append("EOS") # when the sentence is finished, we add the eos token

        if len(final_toks) >= n: # we will only keep it if the sentence is at least n tokens long
            for n0 in range(n):# add freqs to the n ngram tables
                for i in range(len(final_toks)): # we do this by parsing the tokenized sentence
                    if i+n0<len(final_toks): # have to be careful with indexoutofbounds errors
                        # what these next few lines do is initally just extract unigrams, then it will do
                        #bigrams, then trigrams... all the way to n.
                        if " ".join(final_toks[i:i+n0+1]) not in ngram_tables[n0]:
                            ngram_tables[n0][" ".join(final_toks[i:i+n0+1])] = 1
                        else:
                            ngram_tables[n0][" ".join(final_toks[i:i+n0+1])] += 1


## NOW we can generate sentences!
for i in range(m): # m sentences

    if (n>1): #NOT unigram
        options = {}
        toks = []
        toks.append("BOS") # our sentence musts tart with bos
        for k in ngram_tables[1]:# we find all of the possible ways we can start

            if k.split(" ")[0] == "BOS":
                options[k] = ngram_tables[1][k] # if it's possible, add it to "options" and save the freq
        choice = random.choices(list(options.keys()), weights=list(options.values()), k=1)[0].split(" ")[-1] # we choose from options, notice that frequency is used as weights
        toks.append(choice) # add whatever we have chosen
        while choice != "EOS": # keep doing it till we hit the end
            options = {} # kind of the same process
            prev=[]
            if len(toks)> (n-1): # if we have extra....
                prev=" ".join(toks[len(toks)-(n-1):]) #...then we should use the last n-1 tokens
                prev+=" "
                for k in ngram_tables[n-1]: # this is the exact same process of finding what's applicable and choosing a random one (weighted in the same way)
                    if k.startswith(prev):
                        options[k] = ngram_tables[n-1][k]
                choice = random.choices(list(options.keys()), weights=list(options.values()), k=1)[0].split(" ")[-1]
                toks.append(choice)

            else: # otherwise, we can use all the tokens
                prev = " ".join(toks)
                prev+=" "
                for k in ngram_tables[len(toks)]: # we should use the table that matches the num of toks we have
                    if k.startswith(prev):
                        options[k] = ngram_tables[len(toks)][k]
                choice = random.choices(list(options.keys()), weights=list(options.values()), k=1)[0].split(" ")[-1]
                toks.append(choice)
        print(" ".join(toks[1:len(toks)-1]))

    else: # if it's a unigram model, it is functionally very different. We do not care about what was previously
        # generated. We just randomly choose from the unigram table.
        choice = ""
        toks = []
        toks.append("BOS")
        while choice!="EOS":
            choice = random.choices(list(ngram_tables[0].keys()), weights=list(ngram_tables[0].values()), k=1)[0]
            while choice == "BOS":
                choice = random.choices(list(ngram_tables[0].keys()), weights=list(ngram_tables[0].values()), k=1)[0]
            toks.append(choice)
        print(" ".join(toks[1:len(toks) - 1]))

