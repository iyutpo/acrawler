import multiprocessing as mp

import aiohttp
import asyncio
import requests
import time
import json
from bs4 import BeautifulSoup


async def parse(url, res, session):
    async with session.get(url, ssl=False) as result:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        d = {'twitter': [], 'facebook': [], 'android': [], 'ios': []}
        curr = {
            'twitter': None, 'facebook': None, 'android': None, 'ios': None
        }

        for link in soup.find_all('a'):
            href = link.get('href')
            if 'twitter' in href:
                if href[0] == '/':
                    d['twitter'].append(url + href)
                    curr['twitter'] = href[1:]
                else:
                    d['twitter'].append(href)
                    curr['twitter'] = href.split('.com/')[-1]
            if '/ios' in href:
                if href[0] == '/':
                    d['ios'].append(url + href)
                    download = url + href
                else:
                    d['ios'].append(href)
                    download = href.split('.com/')[-1]
                # once we got download url, we need to go to the url and find out the id:
                if download:
                    # parse url:
                    download_page = requests.get(download)
                    download_soup = BeautifulSoup(download_page.content, 'html.parser')
                    for download_link in download_soup.find_all('a'):
                        download_href = download_link.get('href')
                        if 'itunes.apple.com' in download_href:
                            id = download_href.split('/')[-1][2:]
                            curr['ios'] = id
            if 'android' in href:
                download = None
                if href[0] == '/':
                    d['android'].append(url + href)
                    download = url + href
                else:
                    d['android'].append(href)
                    download = href.split('.com/')[-1]
                # once we got download url, we need to go to the url and find out the id:
                if download:
                    # parse url:
                    download_page = requests.get(download)
                    download_soup = BeautifulSoup(download_page.content, 'html.parser')
                    for download_link in download_soup.find_all('a'):
                        download_href = download_link.get('href')
                        if 'play.google.com' in download_href:
                            id = download_href.split('id=')[-1]
                            curr['android'] = id
            if 'facebook' in href:
                if href[0] == '/':
                    d['facebook'].append(url + href)
                    curr['facebook'] = href[1:]
                else:
                    d['facebook'].append(href)
                    curr['facebook'] = href.split('.com/')[-1]
        res.append(curr)

        await result.release()


async def main(url, res):
    async with aiohttp.ClientSession() as session:
        await parse(url, res, session)

if __name__ == '__main__':
    t1 = time.time()
    URLs = [
        'https://www.zello.com',
        'https://www.zynga.com',
    ]
    res = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(* (main(url, res) for url in URLs))
    )

    # loop.close()
    print("Async total time: ", time.time() - t1)
    print('final: ', json.dumps(res))







