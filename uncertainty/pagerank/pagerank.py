import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 100000


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
    if not corpus[page]: #checks if there are no outgoing links
        return_dict = {site: float(1 / len(corpus)) for site in corpus}
        return return_dict
    
    linked_pages = corpus[page]
    return_dict = {site: None for site in linked_pages}
    num_linked_pages = len(linked_pages)
        
    chance_to_choose_links = damping_factor / num_linked_pages
    for linked_page in linked_pages:
        return_dict[linked_page] = chance_to_choose_links
    for key in return_dict:
        return_dict[key] += (1 - damping_factor) / len(return_dict)
    return return_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    starting_page = random.choice(list(corpus.keys()))
    return_dict = {site: float(0) for site in corpus}
    probs = transition_model(corpus, starting_page, damping_factor)
    
    for i in range(SAMPLES):
        keys_list = list(probs.keys())
        weights_list = list(probs.values())
        random_page = random.choices(keys_list, weights= weights_list, k=1)[0]
        return_dict[random_page] += 1
        probs = transition_model(corpus, random_page, damping_factor)
    for key in return_dict:
        return_dict[key] /=  SAMPLES
    
    print(sum(return_dict.values()))
    return return_dict        
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages_in_corpus = len(corpus)
    return_dict = {page: float(1 / num_pages_in_corpus) for page in corpus}
    link_dict = {page: set() for page in corpus.keys()} #key: page, value: set of pages that link to the key-page
    for page in corpus:
        for other_page in corpus:
            if page in corpus[other_page]:
                link_dict[page].add(other_page)

    keep_iterating = True
    while keep_iterating:
        old_dict = return_dict.copy()
        for page in corpus:
            #pages_that_link_to_page = [p for p in corpus if page in corpus[p]]
            pages_that_link_to_page = link_dict[page]
            sum_in_formula = 0
            for p in pages_that_link_to_page:
                if corpus[p]:
                    sum_in_formula += (return_dict[p] / len(corpus[p]))
                else:
                    sum_in_formula += return_dict[p] / num_pages_in_corpus
            return_dict[page] = ((1 - damping_factor) / num_pages_in_corpus) + damping_factor * sum_in_formula
        for page in old_dict:
            keep_iterating = False
            if abs(old_dict[page] - return_dict[page]) > 0.001:
                keep_iterating = True
                break
    total = sum(return_dict.values()) 
    return_dict = {k: v / total for k, v in return_dict.items()}
    print(sum(return_dict.values()))
    return return_dict
   # raise NotImplementedError


if __name__ == "__main__":
    main()
