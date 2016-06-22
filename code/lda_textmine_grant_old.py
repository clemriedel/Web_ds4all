from __future__ import print_function
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import csv
import numpy as np
import textmining
import lda
import numpy as np
import textmining
import nltk.corpus


input_file = csv.DictReader(open("test.csv"))

title, abstract, money, abstractW, awardnum = [], [], [], [], []

for row in input_file:
    title.append(row["Title"])
    abstractW.append(row["Abstract"])
    money.append(row["AwardedAmountToDate"])
    awardnum.append(row["AwardNumber"])

d = len(abstractW)
n_topics = 30

B=[]
for amount in money: 
    B.append(str(amount).replace("$", "").replace(",", "").replace(".00", ""))

f = open('money.csv', 'w')
f.write("\n".join(B))


f = open('awardnum.csv', 'w')
f.write("\n".join(awardnum))


stop=[]
f = open('stopwords.txt', 'r')
for word in f:
    stop.append(word.replace('\n',''))


print("Text mining (tokenizing, removing stop words, stemming) \nPlease wait.")
p_stemmer = PorterStemmer()
for i in range(d):
    sentence = abstractW[i].lower()
    A = [i for i in sentence.split() if i not in stop]
    #A = [p_stemmer.stem(i) for i in A]
    A = str(A).replace('<br/>','').replace('s ','').replace('S_','').replace('dr','').replace('behaviors','behavior').replace('networks','network').replace('populations','population').replace('fungal','fungi').replace('structures','structure').replace('chromosomes','chromosome').replace('rnas','rna').replace('enzymes','enzyme').replace('ecosystems','ecosystem').replace('forests','forest').replace('networs','network').replace('models','model').replace('modeling','model').replace('streams','stream').replace('evolutionary','evolution').replace('males','male').replace('females','female').replace('microbial','microbes').replace('collections','collection').replace('crops','crop').replace('developmental','development').replace('hosts','host').replace('nervous','neurons').replace('structural','structure').replace('behavioral','behavior').replace('biodiversity','diversity').replace('changes','change').replace('soils','soil').replace('bacterial','bacteria').replace('proteins','protein').replace('developed','develop').replace('plants','plant').replace('cells','cell').replace('animals','animal').replace('scientists','researchers').replace('biological','biology').replace('genome','gene').replace('genes','gene').replace('genetic','gene').replace('proteins','protein').replace('metabolic','metabolism').replace('trees','tree').split()
    C = ' '.join(A)
    A = [i for i in sentence.split() if i not in stop]
    abstract.append(C)


# print(abstractW[1])
# print(abstract[1])

tdm = textmining.TermDocumentMatrix()

for i in range(d):
    tdm.add_doc(abstract[i])



# # Create some very short sample documents
# doc1 = abstract[1]
# doc2 = 'John went to the store. The store was closed.'
# doc3 = 'Bob went to the store too.'

# print("\n**These are the 'documents', making up our 'corpus':")
# for n, doc in enumerate([doc1, doc2, doc3]):
    # print("document {}: {}".format(n+1, doc))

# print("-- In real applications, these 'documents' "
      # "might be read from files, websites, etc.")

# # make a titles tuple 
# # -- these should be the "titles" for the "documents" above
# titles = ("Brothers.",
          # "John to the store.",
          # "Bob to the store.")

# print("\n**These are the 'document titles':")
# for n, title in enumerate(titles):
    # print("title {}: {}".format(n+1, title))

# print("-- In real applications, these 'titles' might "
      # "be the file name, the story title, webpage title, etc.")

# # Initialize class to create term-document matrix
# print("\n** The textmining packages is one tool for creating the "
      # "'document-term' matrix, 'vocabulary', etc."
      # "\n   You can write your own, if needed.")
# tdm = textmining.TermDocumentMatrix()

# # Add the documents

# for i in range(d):
    # tdm.add_doc(abstract[i])



# # create a temp variable with doc-term info
temp = list(tdm.rows(cutoff=1))

# get the vocab from first row
vocab = tuple(temp[0])

# # get document-term matrix from remaining rows
X = np.array(temp[1:])

##
## print out info, as in blog post with a little extra info
##
## post: http://bit.ly/1bxob2E
##
# print("\n** Output produced by the textmining package...")

# # document-term matrix
# print("* The 'document-term' matrix")
# print("type(X): {}".format(type(X)))
# print("shape: {}".format(X.shape))
# print("X:", X, sep="\n" )
# print("-- Notice there are 3 rows, for 3 'documents' and\n"
      # "   12 columns, for 12 'vocabulary' words\n"
      # "-- The number of rows and columns depends on the number of documents\n"
      # "   and number of unique words in -all- documents")


# # the vocab
# print("\n* The 'vocabulary':")
# print("type(vocab): {}".format(type(vocab)))
# print("len(vocab): {}".format(len(vocab)))
# print("vocab:", vocab, sep="\n")
# print("-- These are the 12 words in the vocabulary\n"
      # "-- Often common 'stop' words, like 'and', 'the', 'to', etc are\n"
      # "   filtered out -before- creating the document-term matrix and vocab")

# # titles for each story
# print("\n* Again, the 'titles' for this 'corpus':")
# print("type(titles): {}".format(type(titles)))
# print("len(titles): {}".format(len(titles)))
# print("titles:", titles, sep="\n", end="\n\n")

tdm.write_csv('matrix.csv', cutoff=1)

model = lda.LDA(n_topics, n_iter=1500, random_state=1)
model.fit(X)  # model.fit_transform(X) is also available
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 8
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    print('Topic {}: {}'.format(i+1, ' '.join(topic_words)))

f, ax= plt.subplots(5, 1, figsize=(8, 6), sharex=True)
for i, k in enumerate([0, 1, 2, 3, 4]):
    ax[i].stem(topic_word[k,:], linefmt='b-',
               markerfmt='bo', basefmt='w-')
    ax[i].set_xlim(-50,4350)
    ax[i].set_ylim(0, 0.08)
    ax[i].set_ylabel("Prob")
    ax[i].set_title("topic {}".format(k))

ax[4].set_xlabel("word")

plt.tight_layout()
plt.show()	
# get results
topic_word = model.topic_word_ 
doc_topic = model.doc_topic_
	
#print(money)
# print topic probabiities for each document


with open('topic_table.csv', 'w') as f:
    # create header
    #header = 'document'
    #for k in range(n_topics):
    #   header += ', pr_topic_{}'.format(k)
    #f.write(header + '\n')

    # write one row for each document
    # col 1 : document number
    # cols 2 -- : topic probabilities
    for k in range(d):
        # format probabilities into string
        str_probs = ','.join(['{:.5e}'.format(pr) for pr in doc_topic[k,:]])
        # write line to file
        #f.write('{}, {}\n'.format(k, str_probs))
        f.write('{}\n'.format(str_probs))
		

