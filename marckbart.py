#!/usr/bin/env python

import csv
from pymarc import MARCReader
from os import listdir
from re import search

# change this line to match your folder structure
SRC_DIR = 'marc/'

# get a list of all .mrc files in source directory
file_list = filter(lambda x: search('.mrc', x), listdir(SRC_DIR))

csv_out = csv.writer(open('printjournals.txt', 'w'), delimiter = '\t', quotechar = '"', quoting = csv.QUOTE_MINIMAL)

csv_out.writerow(['publication_title', 'print_identifier', 'online_identifier', 'date_first_issue_online', 'num_first_vol_online', 'num_first_issue_online', 'date_last_issue_online', 'num_last_vol_online', 'num_last_issue_online', 'title_url', 'first_author', 'title_id', 'coverage_depth', 'coverage_notes', 'publisher_name', 'location', 'title_notes', 'oclc_collection_name', 'oclc_collection_id', 'oclc_entry_id', 'oclc_linkscheme', 'oclc_number', 'action', 'ownREMOVE'])
     
for item in file_list:
  fd = file(SRC_DIR + '/' + item, 'r')
  reader = MARCReader(fd)
  for record in reader:
    publication_title = print_identifier = online_identifier = date_first_issue_online = num_first_vol_online = num_first_issue_online = date_last_issue_online = num_last_vol_online = num_last_issue_online = title_url = first_author = title_id = coverage_depth = coverage_notes = publisher_name = location = title_notes = oclc_collection_name = oclc_collection_id = oclc_entry_id = oclc_linkscheme = oclc_number = action = ownREMOVE = ''

    # publication_title
    if record['245'] is not None:
      publication_title = record['245']['a']
      if record['245']['b'] is not None:
        publication_title = publication_title + " " + record['245']['b']
    
    # print_identifier
    if record['020'] is not None:
      print_identifier = record['020']['a']
    elif record['022'] is not None:
      print_identifier = record['022']['a']
      
    # online_identifier
    online_identifier = ''
    
    # date_first_issue_online
    if record ['863'] is not None:
      date_first_issue_online = record['863']['i']
    
    # num_first_vol_online
    #if record ['866'] is not None:
      #sep = '-'
      #num_last_vol_online = record['866']['a'].split(sep, 1)[0]
    
    # num_first_issue_online
    if record ['863'] is not None:
      num_first_issue_online = record['863']['b']
    
    # date_last_issue_online
    if record ['863'] is not None:
      date_last_issue_online = record['863']['b']
    
    # num_last_vol_online
    #if record ['866'] is not None:
      #sep = '-'
      #num_last_vol_online = record['866']['a'].split(sep, 1)[-1]
    
    # num_last_issue_online
    num_last_issue_online = ''
    
    #title_url
    if record ['856'] is not None:
      title_url = record['856']['u']
     
    # determine first_author for ebooks
    if record['100'] is not None:
      first_author = record['100']['a']
    elif record['110'] is not None:
      first_author = record['110']['a']
    elif record['700'] is not None:
      first_author = record['700']['a']
    elif record['710'] is not None:
      first_author = record['710']['a']
      
    #titleid
    title_id = ''
    
    #coverage_depth (options fulltext, ebook, print)
    if record['856'] is not None:
      coverage_depth = ('fulltext')
    else: 
      coverage_depth = ('print')
    
    
    #coverage_notes (e.g., graphics excluded)
    if record['852'] is not None:
      coverage_notes = record['852']['z']
    
    # publisher
    if record['260'] is not None:
      publisher_name = record['260']['b']
    
    #location (shelving location, collection, or available online)
    if record['852'] is not None:
      if record['852']['b'] is not None:
        location = record['852']['b']
        if record['852']['c'] is not None:
          location = record['852']['b'] + " " + record['852']['c']
          if record['852']['h'] is not None:
            location = record['852']['b'] + " " + record['852']['c'] + " " + record['852']['h']
            if record['852']['i'] is not None:
              location = record['852']['b'] + " " + record['852']['c'] + " " + record['852']['h'] + " " + record ['852']['i']

    
    #title_notes
    title_notes = ''
    
    #oclc_collection_name
    oclc_collection_name = ''
    
    #oclc_collection_id
    oclc_collection_id = ''
    
    #oclc_entry_id
    oclc_entry_id = ''
    
    #oclc_linkscheme
    oclc_linkscheme = ''
    
    #oclc_number
    if record['035'] is not None:
      if len(record.get_fields('035')[0].get_subfields('a')) > 0:
        oclc_numbers = record['035']['a'].replace('(OCoLC)', '')
        oclc_splitter, sep, tail = oclc_numbers.partition(';')
        oclc_number = oclc_splitter
    
    #action
    action = ('RAW')
    
    #Holding Library - to be remoed
    if record['995'] is not None:
      ownREMOVE = record['995']['a']
       
    csv_out.writerow([publication_title, print_identifier, online_identifier, date_first_issue_online, num_first_vol_online, num_first_issue_online, date_last_issue_online, num_last_vol_online, num_last_issue_online, title_url, first_author, title_id, coverage_depth, coverage_notes, publisher_name, location, title_notes, oclc_collection_name, oclc_collection_id, oclc_entry_id, oclc_linkscheme, oclc_number, action, ownREMOVE])
  fd.close()
  
  
  #todo:  grab volumes/issues;grab collection codes for collection ID (libs to replace); remove 245 after /; test OCLC load.