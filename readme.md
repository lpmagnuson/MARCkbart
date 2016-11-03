Transform an MFHD (MARC format for holdings data) into KBART format for loading
into OCLC's KnowledgeBase.  Written for Python 2.7.

To run, place .mrc records in a /marc directory and run

python marckbart.py

and find tab-delimited output as kbart.txt.

If you have records delivered from OCLC Collection Manager, try marckbartmfhd.py, which is designed for records in which a bib record is followed by one or more holdings records.

