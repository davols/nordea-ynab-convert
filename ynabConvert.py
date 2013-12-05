import csv
import argparse

def repr_data(hdr, data):
  return ', '.join('%s: %s' % (col, val) for col, val in zip(hdr,data))
# How Nordea.no exports it
# Kategori  Beskrivelse Dato  Belop
# Bolig;"IKEA";02.12.2013;-100
sourceEncoding = "iso-8859-1"
targetEncoding = "utf-8"


BANK_HDR = ['Category', 
            'Description', 
            'Date', 
            'Amount']

class BankTransaction(object):
  """Transaction as read from the Nordea CSV file"""
  
  def __init__(self, row):
    self.category=unicode(row[0],'iso-8859-1').encode(targetEncoding)
    self.desc=unicode(row[1],'iso-8859-1').encode(targetEncoding)
    self.date=unicode(row[2],'iso-8859-1').encode(targetEncoding)
    self.amt = unicode(row[3],'iso-8859-1').encode(targetEncoding)


    self.data = [self.date, 
                 self.desc, 
                 self.category, 
                 self.amt]

  def __repr__(self):
    return repr_data(BANK_HDR, self.data)
# How YNAB wants it. 
# Date,Payee,Category,Memo,Outflow,Inflow
# 01/25/12,Sample Payee,,Sample Memo for an outflow,100.00,
# 01/26/12,Sample Payee 2,,Sample memo for an inflow,,500.00
YNAB_HDR = ['Date',  
            'Payee', 
            'Category', 
            'Memo', 
            'Outflow', 
            'Inflow']

class YnabTransaction(object):
  """Transaction to be read into YNAB"""

  def __init__(self, bank_tx):
    self.date = bank_tx.date
    self.payee = bank_tx.desc
    self.category = bank_tx.category
    self.memo = None
    
    self.inflow = None
    self.outflow = None
    if bank_tx.amt.startswith('-'):
      self.outflow = bank_tx.amt[1:]
    else:
      self.inflow = bank_tx.amt

    self.data = [self.date, 
                 self.payee, 
                 self.category, 
                 self.memo, 
                 self.outflow, 
                 self.inflow]

  def __repr__(self):
    return repr_data(YNAB_HDR, self.data)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-o', '--output')
  parser.add_argument('-i', '--input')
  args = parser.parse_args()

  hdr_written = False
  if(args.output==None):
    writer = csv.writer(open('ynabImport.csv', 'w'))
  else :
    writer = csv.writer(open(args.output, 'w'))
  if(args.input==None):
    print 'Error. Needs input csv'
    exit
  else :
    reader = csv.reader(open(args.input, 'r'),delimiter=';')
    for row in reader:
      if not hdr_written:
        writer.writerow(YNAB_HDR)
        hdr_written = True
        continue

      bank_tx = BankTransaction(row)
      #print 'bank: (%s)' % bank_tx

      ynab_tx = YnabTransaction(bank_tx)
      #print 'ynab: (%s)' % ynab_tx

      writer.writerow(ynab_tx.data)

    if(args.output==None):
      print "Printed to ynabImport.csv"
      writer = csv.writer(open('ynabImport.csv', 'w'))
    else :
      print "Printed to %s" %(args.output)
