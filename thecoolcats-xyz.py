from flask import Flask, request, abort, send_file, Response, redirect
from markupsafe import escape
import re
import os
import random
import markdown
import json

app = Flask(__name__)
with open('domains.json') as infile:
    domains1 = json.load(infile)
with open('ssi-webring.html') as file:
    webring = file.read()
domains = {}
for x in domains1:
    domains['http://'+x+'/'] = domains1[x]
    domains['https://'+x+'/'] = domains1[x]
# statusCodePages = {404: "<h1>Error 404: Not found</h1>"}

def remove_header(md_text):
    pattern = r'^---[\s\S]*?^---\n'
    return re.sub(pattern, '', md_text, flags=re.MULTILINE)

def markdown_to_html(markdown_str, title='Thecoolcat\'s blog'):
    html = markdown.markdown(remove_header(markdown_str))
    wow = f'<html><link rel="stylesheet" type="text/css" href="/styles.css" /> <title>{title}</title> </head><body>'
    wow2 = "</body></html>"
    return wow + html + wow2

def make_box(url, title, desc):
    box = f"<a href=\"{url}\" class=\"post-link\"> <div class=\"post\"> <h2 class=\"page-title\">{title}</h2> <p class=\"description\">{desc}</p> </div> </a>"
    return box

def extract_title(meta):
    return meta['title'][0]

def status(code,isCustom=False,custom="There was an error"):
    if isCustom:
        return Response(custom, status=code)
    pages = os.listdir('statuspages/')
    if str(code)+'.html' in pages:
        with open('statuspages/'+str(code)+'.html') as page:
            out = page.read()
        return Response(out, status=code)
    else:
        return Response(custom, status=code)

def extract_desc_text(meta):
    try:
        return meta['summary'][0]
    except:
        return None

def extract_date(markdown_string):
    md = markdown.Markdown(extensions=["meta"])
    md.convert(markdown_string)
    meta = md.Meta
    return meta['date']

def remove_md_extension(file_name):
    # pattern = r'\/?([^\/]+)\.md$'
    pattern = r'([^\\\/]+?)(?:\.md)?$'
    match = re.search(pattern, file_name)
    if match:
        return match.group(1)
    else:
        return file_name

def get_pages(directory='blogposts'):
    pages = {}
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            with open(f) as wow:
                pages[f] = extract_date(wow.read())
    ordered = {k: v for k, v in sorted(pages.items(), key=lambda item: item[1])}
    ordered = list(ordered.keys())
    ordered.reverse()
    return ordered

def blog_main_page():
    pages = get_pages()
    with open('blogStart.html') as blogStart:
        mainPage = blogStart.read()
    for x in pages:
        name = remove_md_extension(x)
        with open('blogposts/'+escape(name)+'.md') as page:
             md = markdown.Markdown(extensions=["meta"])
             md.convert(page.read())
             meta = md.Meta
             mainPage += make_box('posts/'+name,extract_title(meta),extract_desc_text(meta))
             mainPage += '<br>'
    mainPage += webring
    mainPage += '</body></html>'
    return Response(mainPage, status=200)

@app.route("/")
def main():
    pageUrl = domains[request.url_root]
    if pageUrl == 'main':
        with open('main.html') as mainHtml:
            page = mainHtml.read()
        return Response(page, status=200)
    elif pageUrl == 'blog':
        return blog_main_page()

@app.route("/main/<filename>")
def cdnmain(filename):
    pageUrl = domains[request.url_root]
    if pageUrl == 'cdn':
        with open('cdn-index.json') as file:
            cdnIndex = json.load(file)
        try:
            return send_file('cdn-main/'+cdnIndex[filename])
        except KeyError:
            return status(404)
    else:
        return status(404)

@app.route("/main/<foldername>/<filename>")
def cdnmainfolder(foldername, filename):
    pageUrl = domains[request.url_root]
    if pageUrl == 'cdn':
        with open('cdn-index.json') as file:
            cdnIndex = json.load(file)
        try:
            return send_file('cdn-main/'+cdnIndex[f"{foldername}/{filename}"])
        except KeyError:
            return status(404)
    else:
        return status(404)

@app.route('/blog_only')
def blog_only():
    pageUrl = domains[request.url_root]
    if pageUrl == 'blog':
        return Response('<p>only ogs know about mhmdhi</p>', status=200)
    else:
        return status(404)

@app.route('/posts/<post>')
def blog_post(post):
    pageUrl = domains[request.url_root]
    if pageUrl == 'blog':
        try:
             with open('blogposts/'+escape(post)+'.md') as post:
                 markdown_str = post.read()
             return Response(markdown_to_html(markdown_str)+webring, status=200)
        except:
            return status(404)
    else:
        return status(404)

@app.get('/styles.css')
def css():
    return send_file("thecoolcats-xyz.css")

@app.get('/cta')
def cta():
    pageUrl = domains[request.url_root]
    if (pageUrl == 'cdn') or (pageUrl == 'main') or (pageUrl == 'blog'):
        file = random.choice(os.listdir("cta/"))
        return send_file("cta/"+file)
    else:
        return status(404)

@app.get('/cta/<img>')
def ctaImg(img):
    pageUrl = domains[request.url_root]
    if (pageUrl == 'cdn') or (pageUrl == 'main') or (pageUrl == 'blog'):
        file = f"{img}.jpg"
        if file in os.listdir("cta/"):
            print("cta/"+file)
            return send_file("cta/"+file)
        else:
            return status(404)
    else:
        return status(404)
    return status(404)

@app.get('/funny-clip.mp4')
def desjardins():
    return send_file('desjardins.mp4')

@app.errorhandler(404)
def notFound(e):
    with open('statuspages/404.html') as page:
        return page.read()

@app.get('/amogpl')
def amogpl():
    pageUrl = domains[request.url_root]
    if pageUrl == 'main':
        with open('amogpl.md') as file:
            return markdown_to_html(file.read(), 'Amogus Sussy Baka Public License')
    else:
        return status(404)

@app.get('/amogpl/<version>')
def amogplWVersion(version):
    pageUrl = domains[request.url_root]
    if pageUrl == 'main':
        try:
            with open('amogpl/'+escape(version)) as file:
                return markdown_to_html(file.read(), 'Amogus Sussy Baka Public License Version '+escape(version))
        except FileNotFoundError:
            return redirect('/amogpl')
    else:
        return status(404)

@app.get('/pgp')
def pgpPublicSig():
    pageUrl = domains[request.url_root]
    if pageUrl == 'main':
        with open('pgp.pgp') as file:
            return f'<html><head><link rel="stylesheet" type="text/css" href="/styles.css"> <title>Thecoolcat\'s PGP key</title> </head><body><h1>pgp public key</h1>{file.read()}</body></html>'
