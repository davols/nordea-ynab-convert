Nordea's csv to YNAB converter
================================

Small python converter for csv files from Nordea, only tried with Nordea.no to import to YNAB (YouNeedABudget) 
Will output ynabImport.csv

Fork from https://github.com/phildopus/bbt-ynab-convert

Example Usage
------------
    python ynabConvert.py -i FileFromNordea.csv 

Flags
------------------------
* -i or --input to specify input csv file.
* -o or --output to specify output csv. (OPTIONAL)

It will output an ynabImport.csv by default.     