# Web Scraper Application

## Overview
This is a web scraping application with simple GUI built using Python and Tkinter. The application allows users specify a range of pages to scrape data from https://books.toscrape.com . It retrieves book information, including titles, prices, and availability, and displays the results in a scrollable text area. Users can also save the scraped data to a JSON file.

## Libraries Required
To run this application, you need to install the following libraries:

- `requests`: For making HTTP requests to fetch web pages.
- `beautifulsoup4`: For parsing HTML and extracting data.
- `tkinter`: For creating the graphical user interface (GUI).

You can install the required libraries using pip:

```
$ pip install -r requirements.txt
```

## Running the Script
To run the web scraper application, follow these steps:

1. Ensure you have Python installed on your system (Verified to work properly with Python 3.12.3).
2. Download or clone the repository containing the script.
3. Open a terminal or command prompt and navigate to the directory where the script is located.
4. Run the script using the following command:

```
$ python main.py
```


This will launch the Tkinter GUI, where you can input the URL and page range for scraping.

## Building with PyInstaller
If you want to create a standalone executable for the application, you can use PyInstaller. Follow these steps:

1. Install PyInstaller if you haven't already:

```
$ pip install pyinstaller
```

2. Navigate to the directory containing the `main.py` script.
3. Run the following command to create an executable:

```
pyinstaller main.py
```


This will generate a `dist` folder containing the executable file. You can run this executable without needing to have Python or the required libraries installed on the target machine.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
