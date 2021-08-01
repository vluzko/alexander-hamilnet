import csv
import pickle
import requests
import random

from bs4 import BeautifulSoup
from pathlib import Path

DATA = Path(__file__).parent / 'data'
TRAIN = DATA / 'train.txt'
TRAIN_CSV = DATA / 'train.csv'
VALID = DATA / 'validation.txt'
VALID_CSV = DATA / 'validation.csv'


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
    return papers


def dump_text():
    try:
        data = pickle.load((DATA / 'fed_papers.pkl').open('rb'))
    except FileNotFoundError:
        data = scrape_fed()
    train_size = int(len(data) * 0.9)
    train_set = random.sample(list(data.keys()), train_size)
    test_set = [x for x in data.keys() if x not in train_set]
    train_data = [data[k][1] for k in train_set]
    test_data = [data[k][1] for k in test_set]
    train_text = '\n'.join(train_data)
    test_text = '\n'.join(test_data)

    TRAIN.open('w+').write(train_text)
    VALID.open('w+').write(test_text)


def convert_to_csv():
    if not (TRAIN.is_file() and VALID.is_file()):
        dump_text()
    with TRAIN.open('r', encoding='utf-8') as txtfile:
        all_text = txtfile.read()
    with TRAIN_CSV.open(mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'text': all_text})


    with VALID.open(encoding='utf-8') as txtfile:
        all_text = txtfile.read()
    with VALID_CSV.open(mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'text': all_text})

    # print("created train.csv and validation.csv files")


if __name__ == '__main__':
    convert_to_csv()
