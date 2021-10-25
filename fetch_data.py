from bs4 import BeautifulSoup
import urllib.request as request

BASE = 'https://founders.archives.gov'
MAIN_INDEX = 'https://founders.archives.gov/volumes/Hamilton'
NUM_SUB_INDICES = 27


def process_page(link: str) -> str:
    result = request.urlopen(link).read()
    parsed = BeautifulSoup(result)

    paper_title = parsed.find('h1', {'class': 'title'})
    document = parsed.find('div', {'class': 'docbody'})

    all_text = ''.join(document.findAll(text=True))
    return all_text


# https://founders.archives.gov/?q=Volume%3AHamilton-01-01&s=1511311112&r=1
# https://founders.archives.gov/?q=Volume%3AHamilton-01-01&s=1511211112&r=31
# https://founders.archives.gov/?q=Volume%3AHamilton-01-01&s=1511211112&r=61
def process_volume(index_url):
    result = request.urlopen(index_url).read()
    parsed = BeautifulSoup(result)

    all_links = parsed.findAll('a')
    # Link to the next page in this volume
    next_link = [x for x in all_links if x.text == '>']

    papers = parsed.findAll('div', {'class': 'search-result-header'})
    paper_links = []
    for paper in papers:
        links = paper.findAll('a')
        assert len(links) == 1
        paper_query = links[0].attrs['href']
        paper_link = f'{BASE}/{paper_query}'

        paper_links.append(paper_link)
        process_page(paper_link)

    import pdb
    pdb.set_trace()


def main():

    for i in range(1, 1 + NUM_SUB_INDICES):
        sub_index = f'{MAIN_INDEX}/01-{str(i).zfill(2)}'
        process_volume(sub_index)



if __name__ == '__main__':
    main()