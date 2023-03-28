import json

import requests
from lxml import etree

from BackEnd.settings import STATIC_ROOT

_pid = 1
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}


def getData():
    url = 'https://gov.163.com/'
    resp = requests.get(url=url, headers=headers)

    tree = etree.HTML(resp.text)
    temps = tree.xpath('//*[@id="topfocus"]/div[1]/div')[0:3:]
    title = temps[0].xpath('//a[1]/img/@alt')[:3:]
    src = temps[0].xpath('//a[1]/img/@src')[1:4:]
    href = []
    for temp in temps:
        href += temp.xpath('a[1]/@href')
    return [
        {"title": title[i], 'img_src': src[i], 'news_href': href[i]} for i in range(len(title))
    ]


def parse_page(text):
    tree = etree.HTML(text)
    head = tree.xpath('//*[@id="container"]/div[1]/h1/text()')[0]
    body = "".join(tree.xpath('//*[@id="content"]/div[2]//p//text()'))
    author = tree.xpath('//*[@id="content"]/div[3]/text()')[0]
    return {
        'head': head,
        'body': body,
        'author': author,
    }


def get_news(url):
    resp = requests.get(url=url, headers=headers)
    return parse_page(resp.text)


def run():
    try:
        a_list = getData()
        data = []
        for item in a_list:
            data.append(
                {
                    'title': item['title'],
                    'content': get_news(item['news_href']),
                    'src': item['img_src']
                }
            )
        del a_list
        return {
            'code': 200,
            'data': data,
        }
    except Exception as e:
        return {
            'Error': e,
            'code': 404,
            'data': 'None'
        }


def save_img(dic):
    global _pid
    img_bytes = requests.get(url=dic['src'], headers=headers).content
    with open(f'{STATIC_ROOT}/{_pid}.jpg', 'wb') as f:
        f.write(img_bytes)
        del dic['src']
    with open(f'{STATIC_ROOT}/{_pid}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False))
    _pid += 1


def main():
    data = run()['data']
    f = open(f'{STATIC_ROOT}/titles.txt', 'w', encoding='utf-8')
    for i in data:
        f.write(i['title'] + '\n')
        save_img(i)
    f.close()


if __name__ == '__main__':
    main()
