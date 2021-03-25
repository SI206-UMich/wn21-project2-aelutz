#Name: Analese Lutz
#Email: aelutz@umich.edu
#GitHub repository: https://github.com/SI206-UMich/wn21-project2-aelutz

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest




def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    #set up for opening the file
    root_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(root_path, filename)

    #open the file
    with open(filepath, 'r') as f:
        search_results_text = f.read()
    #print(search_results_text[0:30])

    #create soup object
    soup = BeautifulSoup(search_results_text, "html.parser")
    search_results_table = soup.find('table', {'class':'tableList'})
    table_rows = search_results_table.find_all('tr')
    #print(search_results_table)

    #find author name and book titles
    book_author_tups = []
    for row in table_rows:
        #get book title
        title_tag = row.find('a')
        title = title_tag.get('title', None).strip()
        #get author name
        author_tag = row.find('a', {'class':'authorName'})
        author = author_tag.find('span').text.strip()

        book_author_tups.append((title, author))
  
    #print(book_author_tups)

    return book_author_tups
    


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    #create the soup object
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    #get url info
    table_tag = soup.find('table', class_= 'tableList')
    table_rows = table_tag.find_all('tr')[:10]
    link_list = []
    for row in table_rows:
        book_link = row.find('a', class_= 'bookTitle')['href']
        link = "https://www.goodreads.com" + book_link
        link_list.append(link)

    return link_list


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    
    #create soup object
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, "html.parser")

    #get the book title, author, and number of pages
    title = soup.find('h1', id= 'bookTitle' ).text.strip()
    author = soup.find('span', itemprop= "name").text.strip()
    page_number = int(soup.find('span', itemprop= "numberOfPages").text.strip().split()[0])

    summary_tup = (title, author, page_number)
    return summary_tup
    


def summarize_best_books(filename):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    
     #set up for opening the file
    root_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(root_path, filename)

    #open the file
    with open(filepath, 'r') as f:
        search_results_text = f.read()

    #create soup object
    soup = BeautifulSoup(search_results_text, "html.parser")
    
    #find categories, book titles, URLs
    book_summaries = []
    best_books = soup.find_all('div', class_= 'category clearFix')
    for book in best_books:
        category = book.find('h4', class_='category__copy').text.strip()
        book_title = book.find('img', class_='category__winnerImage')['alt']
        url = book.find('a')['href']
        book_summaries.append((category, book_title, url))
    
    return book_summaries






def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    happy = 'hi'
    pass


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    happy = 'hi'
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        search_result_tups = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(search_result_tups), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(search_result_tups), list)
        # check that each item in the list is a tuple
        for tup in search_result_tups:
            self.assertEqual(type(tup), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(search_result_tups[0], ('Harry Potter and the Deathly Hallows', 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(search_result_tups[-1][0], 'Harry Potter: The Prequel')

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)
        #print(TestCases.search_urls)
        # check that each URL in the TestCases.search_urls is a string
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.search_urls:
            self.assertEqual(type(url), str)
            self.assertTrue(url.startswith("https://www.goodreads.com/book/show/"))
        


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
        
        for summary in summaries:
            # check that each item in the list is a tuple
            self.assertEqual(type(summary), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(summary), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(summary[0]), str)
            self.assertEqual(type(summary[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(summary[2]), int)
        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)



    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books_2020 = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books_2020), 20)
        for book in best_books_2020:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(book), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(book), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books_2020[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Antiracist Baby', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books_2020[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable

        # call write csv on the variable you saved and 'test.csv'

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)


        # check that there are 21 lines in the csv

        # check that the header row is correct

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'
        pass


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



