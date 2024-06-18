from bs4 import BeautifulSoup
import requests, json , lxml
import os  
from PIL import Image

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
}

def GatherImage(query):
    params = {
        "q": query,
        "first": 1
    }


    response = requests.get("https://www.bing.com/images/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, "lxml")
    count = 0
    for index, url in enumerate(soup.select(".iusc"), start=1):
        img_url = json.loads(url["m"])["murl"]
        image = requests.get(img_url, headers=headers, timeout=30)
        query = query.lower().replace(" ", "_")
        
        if image.status_code == 200:
            with open(f"gatheredimages/{query}_image_{index}.jpg", 'wb') as file:
                file.write(image.content)
            count+=1
        if count>=2:
            break


path = "D:/Project-Clg/voice assistant/gatheredimages/"
def ShowGatheredImages():
    for i in os.listdir("gatheredimages"):
        a=Image.open(path+i)
        a.show()
        break
