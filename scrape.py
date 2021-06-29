import pickle
import requests

from bs4 import BeautifulSoup
from pathlib import Path

DATA = Path(__file__).parent / 'data'


def scrape_fed():
    urls = (*(f'https://guides.loc.gov/federalist-papers/text-{i*10+1}-{(i+1)*10}' for i in range(8)), 'https://guides.loc.gov/federalist-papers/text-81-85')
    results = (requests.get(url) for url in urls)
    parsed = [BeautifulSoup(res.text) for res in results]

    divs = [y for page in parsed for y in page.find_all('div', id=lambda x: x and x.startswith('s-lg-content-'))[1:]]
    assert len(divs) == 85

    papers = {}
    for i, div in enumerate(divs):
        just_pars = div.findChildren('p')
        # Don't ask me why they changed formatting.
        author_index = 2 if i < 77 and i != 57 else 1
        author = just_pars[author_index].text[8:]
        if 'Hamilton' in author:
            text = (x.text for x in just_pars[author_index+1:])
            full_text = '\n'.join(text)
            papers[i+1] = (author, full_text)
    pickle.dump(papers, (DATA / 'fed_papers.pkl').open('wb'))


if __name__ == '__main__':
    scrape_fed()
