# Email Scraper for PubMed

## Background
[PubMed](https://pubmed.ncbi.nlm.nih.gov/) is essentially a repository of research articles that scientists have published. This allows scientists to read various articles that have been published in their research field by performing a simple query. Every article contains a list of authors with their associated university affiliations and sometimes these authors have email addresses. This allows other scientists to get in contact with the author for various reasons e.g. requesting a copy of the paper, or inquiring about details of the research. This project is a webscraper that returns the email addresses of authors found in the research articles of a PubMed search query. 

## Motivation
A sales representative from [ThermoFisher](https://www.thermofisher.com/) had previously reached out to me on LinkedIn asking to send me information on HLPC solvents. High-Performance Liquid Chromatography (HLPC) is, in layman's terms, a fancy machine that separates chemicals; you need the solvents to make it work. The problem was that, even though I have a PhD in Biochemistry, I had never used an HPLC. I politely communicated this to the sales representative and she responded with a thumbs-up emoji; this left a bad impression of her in my mind. This made me think that their had to be a better way to identify potential clients that have used HPLC's before. Whenever scientists publish a research article, they include methods, materials and equipment that was used; scientists include a corresponding author that can be contacted for various inquiries on the research, and there is sometimes an attached email address. Therefore, if a sales representative wanted to find potential clients, they could search for "HLPC" in the article text in their sales location, look at the list of authors and see if their is an email address. However, this is tedious to manually do, but we can automate it.

## Aim
To develop a python script that retrieves all of the email addresses within a PubMed search.

## Methods
This project uses Python and the library BeautifulSoup for webscraping and Pandas to handle the data. The user first inputs their search query into PubMed and copies the url to the script. The script then retrieves the html content and finds the number of pages in the search results. It then iterates through every search result page and retrieves the articles IDs. These IDs (e.g. "31148079") form part of the url (e.g. "https://pubmed.ncbi.nlm.nih.gov/31148079/") that the script goes to and extracts that authors that are associated with the article. Finally, the script iterates through the pages and only returns authors that contain an email address.

## Prerequisites
- **Python**: This script was last tested with Python 3.12.3 available on Python's official [website](https://www.python.org/downloads/)
- **Pip**: The package installer that should already be installed with Python

## Installation and Use
1. Clone the respository 
```bash
git clone https://github.com/DrVenter/pubmed_scraper.git 
```
2. Navigate to the project directory
```bash
cd pubmed_scraper
```
3. Create a virtual environment
```bash
python -m venv venv
```
4. Activate the virtual environment
```bash
source venv/bin/activate
```
5. Install the dependencies
```bash
pip install -r requirements.txt
```

## Contact
Colin Venter - ventercolin3@gmail.com

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
I acknowledge that ChatGPT was used to help create this project. However, the problem was mine and I did put the code together.

## Lessons Learned

While developing this project, I gained new knowledge in these areas:

### 1. Writing README files
- How to structure the file and using the Markdown syntax.

### 2. Creating Virtual Environments
- The importance of using environments to isolate packages.