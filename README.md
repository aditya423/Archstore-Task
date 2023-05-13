## Task:

Write a Python script that can extract image URLs from Pinterest based on the tags that we provide as input. The script should be able to perform the following tasks:

1. Take input from the user for the Pinterest tags.<br>
2. Scrape Pinterest for images based on the provided tags.<br>
3. Extract the URLs of the images that match the tags.<br>
4. Store the extracted URLs in a CSV file or any other suitable format.

Additionally, script should be efficient and scalable, able to handle a large volume of tags and images. 

<hr>

## Modules Used:
* requests 
* tqdm 
* beautifulsoup4 
* pydotmap 
* opencv-python 
* numpy
<br>

You can install these module using ``` pip install requests tqdm beautifulsoup4 pydotmap opencv-python numpy ``` this command and then run the script ``` pinterest.py ```. It will generate a CSV file ``` urls.csv ``` containing all the image urls on the pinterest for a searched tag.

<hr>
&copy; https://github.com/iamatulsingh/pinterest-image-scrap
<br>Modified the script from the above repository to make it work for this task !
