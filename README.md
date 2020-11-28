This program is designed to get information of products from the amazon webpage via a webdriver and some
webscraping and display it on a php webpage, with formatting.

This is done with a python script as the webscraper (which gathers the information and writes it into a CSV), and php
(which reads from the CSV and formats the relevant information into the webpage).

Usage:
    Simply open a command line and execute the python script with:
    `products.py --searchTerm="**YourSearchTerm**"`
    The default is one product per search, however you can manually specify a quantity of items to search for using an
    additional argument, `--quantity` like so
    `products.py --searchTerm="**YourSearchTerm**" --quantity=**Integer**`
    
Development:
    The IDE I use is Intellij IDEA, so if you use Jetbrains IDEs you can instantly open the repository as an 
    intellij project with run configurations pre configured. I apologise in advance if there's any project
    configurations that are specific to my device that you may need to change.