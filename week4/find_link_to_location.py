#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fetch_html import get_html_content
import re


# USE THIS IN FINAL
#url  = 'http://fil.nrk.no/yr/viktigestader/noreg.txt'
#html = get_html_content(url)

"""
1-Kommunenummer	  2-Stadnamn	     3-Prioritet 4-Stadtype nynorsk
5-Stadtype bokmål 6-Stadtype engelsk 7-Kommune	 8-Fylke
9-Lat	          10-Lon	         11-Høgd	 12-Nynorsk
13- Bokmål	      14-Engelsk

101	Asak kirke	55	Kyrkje	Kirke	Church	Halden	Østfold	59.14465	11.45458
http://www.yr.no/stad/Noreg/Østfold/Halden/Asak_kirke/varsel.xml
http://www.yr.no/sted/Norge/Østfold/Halden/Asak_kirke/varsel.xml
http://www.yr.no/place/Norway/Østfold/Halden/Asak_kirke/forecast.xml


101	Idd	45	Bygd	Bygd	Village area	Halden	Østfold	59.09491	11.42928
http://www.yr.no/stad/Noreg/Østfold/Halden/Idd/varsel.xml
http://www.yr.no/sted/Norge/Østfold/Halden/Idd/varsel.xml
http://www.yr.no/place/Norway/Østfold/Halden/Idd/forecast.xml
"""

html = open('noreg.txt', 'r').read()
list_of_results = re.findall('http.*Idd.*forecast.xml', html)
#location = raw_input('Please input location [news: wheather]')

pprint list_of_results
