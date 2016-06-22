from __future__ import print_function
import pandas as pd
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import textmining
import lda
import textmining
import nltk.corpus

def clem_lda(a):



	with open(a) as f:
		Header = f.next().split(',')
	number_name = Header[0]
	text_name = Header[1][:-2]

	#Read the input file
	input_file = csv.DictReader(open(a))

	text = []
	number = []

	for row in input_file:
	    number.append(row[number_name])
	    text.append(row[text_name])

	d = len(text)
	n_topics = 30

	text_stop = []
	stop = set(stopwords.words('english'))

	for i in range(len(text)):
	    sentence = text[i].lower()
	    A = [i for i in sentence.split() if i not in stop]
	    text_stop.append(' '.join(A))

	tdm = textmining.TermDocumentMatrix()

	for i in range(d):
	    tdm.add_doc(text_stop[i])

	# # create a temp variable with doc-term info
	temp = list(tdm.rows(cutoff=1))

	# get the vocab from first row
	vocab = tuple(temp[0])

	# # get document-term matrix from remaining rows
	X = np.array(temp[1:])


	#tdm.write_csv('matrix.csv', cutoff=1)

	Topics = []

	model = lda.LDA(n_topics, n_iter=100, random_state=1)
	model.fit(X)  # model.fit_transform(X) is also available
	topic_word = model.topic_word_  # model.components_ also works
	n_top_words = 8
	for i, topic_dist in enumerate(topic_word):
	    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
	    Topics.append('Topic {}: {}'.format(i+1, ' '.join(topic_words)))
	    print('Topic {}: {}'.format(i+1, ' '.join(topic_words)))

	# get results
<<<<<<< HEAD
	topic_word = model.topic_word_ 
	doc_topic = model.doc_topic_


=======
	# topic_word = model.topic_word_ 
	# doc_topic = model.doc_topic_

	x=np.arange(1, 31, 1)
	y=np.abs(np.random.randn(30))

	ax = sns.barplot(x, y, color='Blue')
	ax.set(xlabel='Topics', ylabel='M$')
	sns.plt.savefig('static/test_image.png')
>>>>>>> origin/master
		
	return Topics, text_name

	
	with open('static/topic_table', 'w') as f:
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
			
	dat = np.genfromtxt ('static/topic_table', delimiter=",")

	M = []
	for i in range(len(number)):
    		M.append(dat[i,:]*int(number[i]))

	M = sum(M)

	x=np.arange(1, n_topics+1, 1)
	y=M



	ax = sns.barplot(x, y, color='Blue')
	ax.set(xlabel='Topics', ylabel=number_name)
	sns.plt.savefig('static/test_image2.png', dpi=1200)


