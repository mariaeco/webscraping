# 📌 Webscraping Bidding Exemptions in the State of Paraíba


Here we performed a web scraping of the bidding waivers between the years 2018 to 2024 available on the Paraíba Transparency Portal "https://transparencia.pb.gov.br/relatorios/?rpt=licitacoes".

The web scraping is found in the scraping.py file.

Additionally the data was processed:
- first joining the data of the years:
    
        data_join.csv
- then we standardized the data:

        data_standardization.ipynb file

    In standardization, 
    
    First unified the departments and agencies by the main acronyms.

    Second, we standardized the bidding objects using an <span style="color:#FF5733;">*AI agent*</span>.
    The AI agent is working well needs improvement.


Scraping is slow, as access to the site takes a long time and its server goes down a lot, in addition to several non-standardizations in the data structure. But it is working even with brute force.

Used libriries:

    requests
    selenium
    openpyxl
    openai
    pandas
    glob


## 📌 Important Notes
The projects respect the websites' access policies. If any scraping is not available, it is possible that the website has updated its settings.
This repository is educational. Always consult the websites' terms of use before performing automatic data collections.