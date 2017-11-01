# -*- coding: utf-8 -*-
"""
    proofchecker
    ~~~~~
    :copyright: (c) 2014-2016 by Halfmoon Labs, Inc.
    :copyright: (c) 2016 blockstack.org
    :license: MIT, see LICENSE for more details.
"""


from bs4 import BeautifulSoup
from .sites import SITES

GITHUB_CONTENT_TAG = 'blob-wrapper'
GITHUB_DESCRIPTION_TAG = 'repository-meta-content'
GITHUB_FILE_TAG = 'user-select-contain gist-blob-name css-truncate-target'

def get_github_text(raw_html):

    html = BeautifulSoup(raw_html, "html.parser")

    gist_description = html.find('div', {'class': GITHUB_CONTENT_TAG})

    if gist_description is not None:
        gist_description = gist_description.text
    else:
        gist_description = html.find('div', {'class': GITHUB_DESCRIPTION_TAG})

        if gist_description is not None:
            gist_description = gist_description.text
        else:
            gist_description = ''

    file_text = html.find('div', {'class': GITHUB_FILE_TAG})

    if file_text is not None:
        file_text = file_text.text
    else:
        file_text = ''

    search_text = gist_description + ' ' + file_text

    return search_text

def get_instagram_identity(raw_html):
    try:
        html = BeautifulSoup(raw_html, 'html.parser')
        username = html.find("meta", {"property": "og:description"})['content']
        if username:
            parts = username.split(':')
            if len(parts) > 1:
                lets_match = parts[0]
                parens_open = lets_match.index("(")
                parens_close = lets_match.index(")")
                return lets_match[parens_open+2:parens_close]
    except Exception as e:
        import traceback as tb; tb.print_exc()
        return None

def get_linkedin_identity(raw_html):
    try:
        html = BeautifulSoup(raw_html, 'html.parser')
        profileLink = html.find("article").find(class_='post-meta__profile-link')
        if profileLink:
            return profileLink.get('href').split('/')[-1]
    except Exception as e:
        import traceback as tb; tb.print_exc()
        return None

def get_search_text(service, raw_html):

    if service == 'facebook':
        raw_html = raw_html.replace('<!--', '').replace('-->', '')

    html_soup = BeautifulSoup(raw_html, "html.parser")

    if service in SITES:
        query_data = SITES[service]['html_query']
        search_text = ''
        if 'class' in query_data:
            search_results = html_soup.body.find('div', class_=query_data['class'])
            if search_results:
                search_text = search_results.text
        elif 'title' in query_data:
            search_results = html_soup.title.string
        else:
            search_results = html_soup.body
            if search_results:
                search_text = search_results.text

    return search_text


def get_twitter_url(raw_html):

    soup = BeautifulSoup(raw_html, "html.parser")

    try:
        url = soup.find("meta", {"property": "og:url"})['content']
    except:
        url = ''

    return url
