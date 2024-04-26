from flask import Flask, request, abort, send_file, Response
from markupsafe import escape
import re
import os
import random
import markdown

app = Flask(__name__)
domains = {r'http://localhost:5000/':'main',r'http://www.localhost:5000/':'main',r'http://blog.localhost:5000/': 'blog',r'http://cdn.localhost:5000/': 'cdn'}
statusCodePages = {404: "<h1>Error 404: Not found</h1>"}

def _unsafe_markdown_to_html(markdown):
    # Convert Markdown to HTML
    html = re.sub(r'^(#{1})\s(.+)$', r'<h1 class="title">\2</h1>', markdown, flags=re.MULTILINE)
    html = re.sub(r'^(#{2,})\s(.+)$', r'<h2 class="subtitle">\2</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    html = re.sub(r'\[(.*?)\]\[(.*?)\]', r'<a href="#\2">\1</a>', html)
    html = re.sub(r'\[(.*?)\]:\s*(.*?)$', r'<a href="\2" id="\1"></a>', html, flags=re.MULTILINE)
    html = re.sub(r'^(?!\s*$)(.+)$', r'<p>\1</p>', html, flags=re.MULTILINE)
    html = re.sub(r'```(.*?)\n(.*?)\n```', r'<code class="codeblock">\2</code>', html, flags=re.DOTALL)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    wow = "<html><link rel=\"stylesheet\" type=\"text/css\" href=\"/styles.css\" /> <title> Thecoolcat's blog</title> </head><body>"
    wow2 = "</body></html>"
    return wow + html + wow2

def remove_header(md_text):
    pattern = r'^---[\s\S]*?^---\n'
    return re.sub(pattern, '', md_text, flags=re.MULTILINE)

def markdown_to_html(markdown_str):
    html = markdown.markdown(remove_header(markdown_str))
    wow = '<html><link rel="stylesheet" type="text/css" href="/styles.css" /> <title>' + "Thecoolcat's blog</title> </head><body>"
    wow2 = "</body></html>"
    return wow + html + wow2

def make_box(url, title, desc):
    box = f"<a href=\"{url}\" class=\"post-link\"> <div class=\"post\"> <h2 class=\"page-title\">{title}</h2> <p class=\"description\">{desc}</p> </div> </a>"
    return box

def extract_title(meta):
    return meta['title'][0]

#def extract_desc_text(markdown):
    ## Find title
    #title_match = re.search(r'^#\s(.+)$', markdown, re.MULTILINE)
    #if title_match:
        #title = title_match.group(1)
    #else:
        #return "Title not found"
    
    ## Find italicized text
    #italicized_text_match = re.search(r'^##\s(.+)$', #markdown[title_match.end():], re.MULTILINE)
    #if italicized_text_match:
        #italicized_text = italicized_text_match.group(1)
        #return italicized_text
    #else:
        #return "Italicized text not found"

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

def remove_md_extension(file_name):
    # pattern = r'\/?([^\/]+)\.md$'
    pattern = r'([^\\\/]+?)(?:\.md)?$'
    match = re.search(pattern, file_name)
    if match:
        return match.group(1)
    else:
        return file_name

def get_pages(directory='blogposts'):
    pages = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            pages.append(f)
    return pages

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
             return Response(markdown_to_html(markdown_str), status=200)
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