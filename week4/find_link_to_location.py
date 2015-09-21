#!/usr/bin/env python
# encoding: utf-8
from fetch_html import get_html_content
from numpy import zeros
import re

url       = 'http://fil.nrk.no/yr/viktigestader/noreg.txt'
html_data = get_html_content(url)

#location = raw_input('Please input location [news: wheather]')

html_data_lines = html_data.readlines()

cols = 17; rows = len(html_data_lines)
print len(html_data_lines)
"""
html_data_table = zeros((rows,cols))

for i in range(rows):
    html_data_table[i] = html_data_lines[i].split("\t")

print html_data_table
"""
