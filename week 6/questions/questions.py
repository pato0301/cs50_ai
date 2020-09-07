import nltk
import sys
import os
import string 
import math 

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    file_cont = dict()
    files_names = os.listdir(directory)

    for file in files_names:
        file_path = os.path.join('./',directory,file)
        with open(file_path) as f:
            contents = f.read()
        
        file_cont[file] = contents

    return file_cont
    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    tmp_token = []
    sentence_token = []
    s_token = nltk.word_tokenize(document)

    for word in range(len(s_token)):
        s_token[word] = s_token[word].lower()
        if speller(s_token[word] ):
            tmp_token.append(s_token[word])

    for word in tmp_token:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            sentence_token.append(word)

    return sentence_token
    # raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    idf = dict()
    num_doc_cont = 1

    for filename in documents:
        for word in documents[filename]:
            if word not in idf:
                for second_file in documents:
                    if filename != second_file:
                        if word in documents[second_file]:
                            num_doc_cont += 1

                idf[word] = math.log(num_doc_cont)

    return idf
    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    tf_idf = dict()
    file_idfs = idfs.copy()
    files_list = []
    token_query = list(query)

    for filename in files:
        value = 0
        for word in token_query:
            if word in files[filename]:
                num_in_doc = files[filename].count(word)
                idf_val = file_idfs[word]
                value += (num_in_doc * idf_val)
        
        tf_idf[filename] = value

    for num_files in range(len(tf_idf)):
        max_file = -math.inf
        for filename in tf_idf:
            if tf_idf[filename] > max_file:
                if filename not in files_list:
                    max_file = tf_idf[filename]
                    max_file_name = filename
        files_list.append(max_file_name)


    if n > len(files_list):
        return files_list
    
    return files_list[:n]
    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    top_sentences= []
    mat_word_meas = dict()
    file_idfs = idfs.copy()
    token_query = list(query)

    for sent_num in sentences:
        value = 0
        q_term_density = 0
        for word in token_query:
            if word in sentences[sent_num]:
                value += file_idfs[word]
                q_term_density += 1
        
        q_term_density /= len(sentences[sent_num])
        mat_word_meas[sent_num] = (value,q_term_density)

    for num_files in range(len(mat_word_meas)):
        max_sent = (-math.inf,-math.inf)

        for sent_num in sentences:
            if mat_word_meas[sent_num][0] > max_sent[0]:
                if sent_num not in top_sentences:
                    max_sent = mat_word_meas[sent_num]
                    max_sent_name = sent_num
            elif mat_word_meas[sent_num][0] == max_sent[0]:
                if sent_num not in top_sentences:
                    if mat_word_meas[sent_num][1] > max_sent[1]:
                        max_sent = mat_word_meas[sent_num]
                        max_sent_name = sent_num

        top_sentences.append(max_sent_name)

    if n > len(top_sentences):
        return top_sentences
    
    return top_sentences[:n]
    # raise NotImplementedError

def speller(word):
    is_word = False
    for c in word:
        if c.isalpha():
            is_word = True
            break
    
    return is_word

if __name__ == "__main__":
    main()
