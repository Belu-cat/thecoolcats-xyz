import requests
import json
import os
response = requests.get('https://thecoolcats.xyz/cta/indx')
cta = response.text.split('<br>')
response = requests.get('https://cdn.thecoolcats.xyz/main')
response = response.text.replace('<html><head><title>Thecoolcats CDN Index</title></head><body>', '').replace('</body></html>', '')
cdnmain = response.split('<br>')
def downloadfile(url, filename):
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            f.write(chunk)

os.mkdir('cta')
for x in cta:
    downloadfile(f'https://thecoolcats.xyz/cta/{x}', f'cta/{x}.png')

os.mkdir('cdn-main')
cdnIndex = {}
for x in cdnmain:
    cdnIndex[x] = f'{x.replace('/', '$slash$')}.png'
    downloadfile(f'https://cdn.thecoolcats.xyz/main/{x}', f'cdn-main/{x.replace('/', '$slash$')}.png')
with open('cdn-index.json') as f:
    json.dump(cdnIndex, f)

os.mkdir('blogposts')

def askquestion():
    cmd = input('Do you wish to create the start.sh script? [y/n]')
    if cmd == 'y' or cmd == 'Y':
        with open('start.sh', 'w+') as f:
            f.write(""". .venv/bin/activate
screen gunicorn --config gunicorn_config.py thecoolcats-xyz:app --preload -b 0.0.0.0:80""")
    elif cmd == 'n' or cmd == 'N':
        exit()
    else:
        askquestion()

askquestion()