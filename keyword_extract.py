import nltk
import pprint

source_uri = "/Users/shayanmasood/Spark-dev/healthhack2015/raw_data/drugs_map.psv"
url = "https://sentinelprojects-skyttle20.p.mashape.com/"

tokenizer = None
tagger = None

def init_nltk():
    global tokenizer
    global tagger
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
    tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())

def tag(text):
    global tokenizer
    global tagger
    if not tokenizer:
        init_nltk()
    tokenized = tokenizer.tokenize(text)
    tagged = tagger.tag(tokenized)
    # tagged.sort(lambda x,y:cmp(x[1],y[1]))
    return tagged

rows=[]
found_treatment = False
with open(source_uri) as f:
  i=0
  for line in f:
    indications=[]
    found_treatment = False
    row = line.strip().split('|')
    text = row[1]
    if text:
      tagged = tag(text)    
      l = list(tagged)
      for word in l:
        if found_treatment:
          if word[1] == "CC" or word[1] == "IN":
            if word[1] != "-":
              break
            else:
              if word[0] == "-":
                "".append(word[0])
          if word[1] == "NN" or word[1] == None:
            indications.append(word[0])
        if word[0] == "treatment" or word[0] == "treat" or word[0] == "diagnosis":
          found_treatment = True
      appended_row =  "|".join(row) + "|"
      appended_indications = "".join(indications)
    rows.append(appended_row + appended_indications)
    pprint.pprint(l)
  
    
  

    
