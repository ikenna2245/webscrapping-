from bs4 import BeautifulSoup as BS
import requests as req
import pandas as pd

#page url
url = 'https://www.ewg.org/skindeep/search/?search_type=ingredients&per_page=36'

#request source page
page_src = req.get(url)

#generating tree structure(t_s) of the page
t_s = BS(page_src.text, "lxml")

#getting the product listings for the page
product_listings = t_s.find('section', 'product-listings')


#list of products in view
products =  product_listings.find_all('div',  'product-tile')

# name the output file to write to local disk
out_filename = "product_list.csv"

# header of csv file to be written
headers = "name, score \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

for product in products:
    try:
        #pulling the product name an score
        name = product.find('p', 'product-name').a.text
        score = product.find('img', 'product-score-img')['src'][-1]
    except TypeError:
        print('check object pattern')
    except KeyError:
        print('Keyerror in the dict') 
    # writes the dataset to file
    f.write(f'{name}, {score} \n')
#first set of code scrapes the first page


pages =[ 2,3] #to scrap the whole 500 pages set the range (2-499)
for n in pages:
    url = f'https://www.ewg.org/skindeep/search/?page={n}&per_page=36&search_type=ingredients'
    #request source page
    page_src = req.get(url)

    #generating tree structure(t_s) of the page
    t_s = BS(page_src.text, "lxml")

    #getting the product listings for the page
    product_listings = t_s.find('section', 'product-listings')

    #list of products in view
    products =  product_listings.find_all('div',  'product-tile')

    for product in products:
        try:
            #pulling the product name an score
            name = product.find('p', 'product-name').a.text
            score = product.find('img', 'product-score-img')['src'][-1]
        except TypeError:
            print('check object pattern')
        except KeyError:
            print('Keyerror in the dict') 
        # writes the dataset to file
        f.write(f'{name}, {score} \n')
f.close()  # Close the file

#read data from csv in pandas 
df = pd.read_csv("product_list.csv", error_bad_lines=False)

#scrapped more than 50 items limiting to 50 and printing in a table. 
df[:50].to_html("product_list.html")

