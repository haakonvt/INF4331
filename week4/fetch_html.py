#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib

def get_html_content(url):
    response = urllib.urlopen(url)
    html     = response.read()
    return html
