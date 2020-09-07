import os
import random
import re
import sys
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Transfor cospus dict into list and get length, after that append the transition page
    # into the list corpus, because if not only the values from the page key will be
    list_copus = list(corpus[page])
    num_links = len(list_copus)
    list_copus.append(page)

    # Probability dict and not damping factor
    dict_prob = {}
    not_damping = 1 - damping_factor

    # Loop to get each page probability as:
    # the key page pass in the argument is only not damping divide by the pagesto where is link plus the current page
    # else the probability is the damping divide by the pages that are link to
    for x in list_copus:
        if x == page:
            dict_prob[x] = not_damping / (num_links+1)
        else:
            dict_prob[x] = (damping_factor / num_links) + (not_damping / (num_links+1))
    
    return dict_prob
    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Start from a random page, to start sampling
    sample_page = random.choice(list(corpus.keys()))

    # Create a list to have the results from sampling
    data = []
    data.append(sample_page)

    # Iterate N times to get N random samples
    for i in range(n-1):
        dict_prob = transition_model(corpus, sample_page, damping_factor)
        list_options = list(dict_prob.keys())
        list_prob =  list(dict_prob.values())
        sample_page = random.choices(list_options,list_prob)
        sample_page = sample_page[0]
        data.append(sample_page)

    # Get how many samples of each page there are
    rank_sample = Counter(data)
    rank = {}

    # Calculate the probability for each page
    for page in rank_sample:
        rank[page] = (rank_sample[page]/n)

    return rank

    # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize pages on the Corpus with 1/N probability
    # Where N is the total number of unique pages in the corpus
    list_copus = list(corpus.keys())
    num_pages = len(list_copus)

    # Dict with probability from the previous iteration
    prev_dict_prob = {}

    # Dict with probabilities
    dict_prob = {}

    # Pages that link to each pages, and how many links has each of those pages
    # eg. pages 4 and 3 link to page 2 and page 4 has a total of 2 links and page 3 has a total of 4
    # then dict would be like {page2: {page4:2, page3: 4}}
    num_links = {}
    not_damping = 1 - damping_factor

    # Difference with previous iteration
    diff = 0

    # First iteration to get probability 1/N for every page
    for x in list_copus:
        dict_prob[x] = 1 / num_pages
        num_links[x] = prob_go_to_page(corpus,x)
    
    prev_dict_prob = dict_prob.copy()
    first_pass = True

    # Iterate until the difference between previous iteration an the current one is less than 0.001
    while first_pass or diff > 0.001:
        diff = 0
        first_pass = False
        temp_dict = {}
        for x in list_copus:
            num_links_x = num_links[x]
            dict_prob[x] = (not_damping / num_pages) + (damping_factor * prob_sum(prev_dict_prob,num_links_x))
            temp_diff = abs(prev_dict_prob[x]-dict_prob[x])
            diff = max(diff,temp_diff)
        
        prev_dict_prob = dict_prob.copy()

    return dict_prob
    # raise NotImplementedError

def prob_go_to_page(corpus,page):
    """ Calculate how many pages linked to the current page in which we are
        and how many total links each of those pages have
    """
    # Calculate the number of pages that link to the page pass in the argument
    # and how many links does each of those pages
    num_links_i = {}

    # Get total number of pages, so when a page has no link to others
    # then we suppose that it links to all of the pages in the corpus
    list_copus = list(corpus.keys())
    num_pages = len(list_copus)

    # Loop to get the number of pages that link to certain page
    for x in corpus:
        if page in corpus[x]:
            list_copus = list(corpus[x])
            num_links = len(list_copus) 
            num_links_i[x] = num_links
        elif corpus[x] == set():
            num_links_i[x] = num_pages
    
    return num_links_i

def prob_sum(pages_prob_dict,num_links):
    """ Calculate the Sumation for the equation to get the probability
        PR(i) / NumLinks(i)
    """
    sum = 0
    for x in num_links:
        temp = pages_prob_dict[x] / num_links[x]
        sum = sum + temp

    return sum


if __name__ == "__main__":
    main()
