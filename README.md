Project Overview

This project is a GUI web scraping desktop application tool developed to extract specific information from targeted website efficiently. 
The scraper is built using Python and relies heavily on libraries like BeautifulSoup, Pandas, openpyxl, Selenium and others. 
The extracted data is processed and stored in a structured format, typically in a Pandas DataFrame, later on it is svaed to an EXCEL FILE making it easy to analyze and manipulate for various purposes.

![Screenshot 2024-11-04 221822](https://github.com/user-attachments/assets/c80f06d2-9c4e-4119-bc14-8b473f1478f5)

As seen in the image above for each available product there is specific info that needs to be extracted.
Info such as date of delivery, total number of expected delivers etc...


![Screenshot 2024-10-13 055905](https://github.com/user-attachments/assets/9ca404ae-812d-4052-b385-3338420defaa)

Once the application is running there are few options.

Firstly a directory where the excel file with all the scraped info will be saved should be selected.
Then we are given two options.

"Schrapen" which means SCRAPE. This will scrape all the info and save it to an excel file. 
If a directory is not selected the file will be saved in the directory of the app.
Make sure you also have the necessary permissions otherwise you may encounter errors.

![Screenshot 2024-10-11 195756](https://github.com/user-attachments/assets/a5944c1e-cd83-4b20-8374-e2b3f28d11b8)

Once the scrape is successful you will be notified.

The excel file with the scraped info should look like that

![Screenshot 2024-09-04 200650](https://github.com/user-attachments/assets/168e797c-098c-4dc0-8690-66a998de2194)

Same thing goes for the "Overdrachten" functionality.

The only difference is that you need to provide a file with scraped info.
After all the main goal of the app is to transfer the necessary scraped info into a pre-defined template file and make all the work with it easier.

![Screenshot 2024-10-11 201526](https://github.com/user-attachments/assets/0bae9680-7c93-4ff9-8785-95a792c7f4c2)

Once the transfer is done, there will be a whole new file in the selected directory.

It  will contain all the neccessary info from the scraped data file.
It should look like that: 

![Screenshot 2024-11-04 221051](https://github.com/user-attachments/assets/ad1c7602-8713-46d7-9264-4f50e1c75c93)

THIS APPLICATION WILL ONLY RUN IF THE WEBSITE LINK AND ALL THE NECESSARY CREDENTIALS ARE PROVIDED.
THEY WILL NOT BE PRESENT IN THIS REPOSITORY.

