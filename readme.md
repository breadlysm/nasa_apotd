# Nasa Astronomy picture of the day
Quick python script that downloads Nasa Astronomy picture of the day. 

## Features
* Download Location Selector
* Specify amount of historic APOTD's to grab


## Basics
Running script with no arguments will download today's image

Using -d or --day and an integer, will download X days from their page. 

Downloads 30 days of images.
>python nasa_apotd.py -d 30

Using -l or --location will open up a gui on start to allow you to select a download folder.
>python nasa_apotd.py -l

