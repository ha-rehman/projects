import urllib

a = 5
b = 0

try:
    c = a+b
    print(c)
    try:
        c=a/b
        print(c)
    except:
        print("Inner Exception")
    finally:
        print("Inner Final")
except:
    print("Outer Exception")
finally:
    print("Outer Final")

import re


# Function to find currency symbol
# in a text using regular expression
# def findCurrencySymbol(text):
#     # Regex to find any currency
#     # symbol in a text
#     regex = "\\₹"
#
#     # for m in re.finditer(regex, text):
#     #     print(text[m.start(0)], "-", m.start(0))
#     lst = re.find(regex, text).to_list()
#     print(lst)
# # Driver code
# txt = "$27 - ₹21.30equal to $5.70"
# findCurrencySymbol(txt)

# currencies = ['$', '£']
# txt = "$27 - ₹21.30equal to $5.70"
# for currency in currencies:
#     if txt.contains(currency):
#         txt.str.strip(currency)
#         txt = currency

# from price_parser import Price
# print(Price.fromstring("Price: ₹119.00"))

# img = "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcT1sDbsqyEK9dDayK5nPY-VqOpbLVps5Q8dDbOx7QxdLra9xYY3"
# import urllib.request
# MyUrl = "www.google.com" #Your url goes here
# urllib.request.urlretrieve(img, "visual/1.png")

import os
os.mkdir(os.path.join("visual", str(2)))