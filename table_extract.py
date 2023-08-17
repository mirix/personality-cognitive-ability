import camelot
import ast
import numpy as np

# Extract table from PDF

supp = '/home/emoman/Downloads/pnas.2212794120.sapp.pdf'
table = camelot.read_pdf(supp, pages='422', flavor='stream')

df = table[0].df
df.drop(df.tail(1).index, inplace=True)

# Process headers

header = df.iloc[:10].copy()

headers = header.apply(lambda x: ' '.join(x)).reset_index()[0].to_list()
headers = [i.strip(' ') for i in headers]
headers.pop(0)

headers[0] = 'General Mental Ability'
headers[1] = 'Non_Invested Abilities'
headers[10] = 'Invested_Acquired Abilities'
headers[-1] = 'Mean across All Abilities'

# Process content

df = df.iloc[10:].copy()

main_traits = ['Neuroticism', 'Agreeableness', 'Conscientiousness', 'Extraversion', 'Openness', 'General Factor of Personality']

for trait in main_traits:
	df[0] = df[0].replace(trait, trait.upper())

df.set_index(0, inplace=True)
df.index.name = None

# Add headers

df.columns = headers

# Strings to tuples

df = df.replace('', '0 , 0')
for col in df:
	df[col] = df[col].apply(ast.literal_eval)

# Save 
#print(df)

df.to_csv('pnas_2212794120_S89.csv')
df.to_excel('pnas_2212794120_S89.xlsx')

# Averages

def tuple_mean(row):
	return round((row[0] + row[1]) / 2, 2)
	
df2 = df.applymap(tuple_mean)

df2.to_csv('pnas_2212794120_S89_MEAN.csv')
df2.to_excel('pnas_2212794120_S89_MEAN.xlsx')

# Extract figures

from PyPDF2 import PdfReader, PdfWriter

pdf = PdfReader(supp)

pages = [70, 71]
pdfWriter = PdfWriter()

for page in pages:
    pdfWriter.add_page(pdf.pages[page])

with open('pnas_2212794120_S1_S2.pdf', 'wb') as f:
    pdfWriter.write(f)
    f.close()
