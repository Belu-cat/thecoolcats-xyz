from flask import Flask, request, abort, send_file, Response, redirect
from markupsafe import escape
import re
import os
import random
import markdown
import json

app = Flask(__name__)

def remove_header(md_text):
    pattern = r'^---[\s\S]*?^---\n'
    return re.sub(pattern, '', md_text, flags=re.MULTILINE)

def markdown_to_html(markdown_str, title='Thecoolcat\'s blog'):
    html = markdown.markdown(remove_header(markdown_str))
    wow = f'<html><link rel="stylesheet" type="text/css" href="/styles.css" /> <title>{title}</title> </head><body>'
    wow2 = "</body></html>"
    return wow + html + wow2

@app.route("/")
def main():
    with open('1.19.84.md') as infile:
        return markdown_to_html(infile.read())

@app.errorhandler(404)
def notFound(e):
    with open('statuspages/404.html') as page:
        return page.read()

@app.get('/styles.css')
def css():
    return send_file("thecoolcats-xyz.css")