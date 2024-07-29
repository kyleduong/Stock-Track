from flask import Flask, jsonify, render_template
from bs4 import BeautifulSoup
import requests

url = "https://www.newegg.com/asus-geforce-rtx-4070-ti-super-tuf-rtx4070tis-o16g-gaming/p/N82E16814126685"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")
picture = BeautifulSoup(result.content, 'html.parser')
#print(doc.prettify())

# Find the image element
image_element = picture.find('img', {'class':'product-view-img-original'})

# Get the image URL
image_url = image_element['src']

# Save the image URL to a file
"""
with open('image_url.txt', 'w') as file:
    file.write(image_url)
    """

print(f"Image URL: {image_url}")

prices = doc.find_all(string="$")
print(prices)

parent = (prices[0].parent)

strong = parent.find("strong")

print(strong.string)

# For the HTML File
"""
under all the style/head
<body>
    <div class="image-container">
        <h1>Graphics Card Image</h1>
        <img id="graphics-card-image" src="" alt="Graphics Card">
    </div>

    <script>
        // Fetch the image URL from the text file
        fetch('image_url.txt')
            .then(response => response.text())
            .then(url => {
                document.getElementById('graphics-card-image').src = url.trim();
            });
    </script>
</body>
"""