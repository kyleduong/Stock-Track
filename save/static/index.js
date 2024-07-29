document.addEventListener('DOMContentLoaded', (event) => {

    function scrapping() {
        window.alert('Scrapping Initiated');
        console.log("This is working and connected just fine");
    }

    document.getElementById("scrapper").addEventListener("click", scrapping);
    

        // Function to show image based on item clicked
        function showImage(itemName) {
            const imageUrls = {
                'ryzen 9 3900x': 'https://c1.neweggimages.com/ProductImageCompressAll1280/14-126-685-14.png',
                '144hz monitor': 'https://th.bing.com/th/id/OIP.N_aDzw35sawDt8CRi-OSDQAAAA?rs=1&pid=ImgDetMain',
                'rtx 4080': 'path_to_image_3.jpg',  // Replace with actual URL
                '55 inch tv': '/static/rymond2.0.png',  // Replace with actual URL
                'ddr4 ram': 'path_to_image_5.jpg',  // Replace with actual URL
                '512gb ssd': 'path_to_image_6.jpg',  // Replace with actual URL
                '750w power supply': 'path_to_image_7.jpg',  // Replace with actual URL
                'keyboard': 'path_to_image_8.jpg'  // Replace with actual URL
            };
    
            const imageUrl = imageUrls[itemName];
            if (imageUrl) {
                document.getElementById('choice-image').src = imageUrl;
                document.getElementById('choice-image').style.display = 'block'; // Show the image
                document.getElementById('image-error-message').style.display = 'none'; // Hide the error message

                // MAKE THE FIRST PIC DISSAPEAR WHEN I CLICK THE BUTTON
                //document.getElementById('graphics-card-image').style.display = 'none';
                
            } else {
                // Handle case where no image URL is defined
                console.log('No image URL defined for ' + itemName);
            }
        }

        // Get the search box and item list elements
        const searchBox = document.getElementById('searchBox');
        const itemList = document.getElementById('itemList');
        const items = itemList.getElementsByTagName('li');

        // Add an input event listener to the search box
        searchBox.addEventListener('input', function() {
            const filter = searchBox.value.toLowerCase();

            // Loop through all list items and hide those that don't match the search query
            for (let i = 0; i < items.length; i++) {
                const item = items[i].getElementsByTagName('div')[0];
                const txtValue = item.textContent || item.innerText;

                if (txtValue.toLowerCase().indexOf(filter) > -1) {
                    items[i].style.display = '';
                } else {
                    items[i].style.display = 'none';
                }
            }
        });

        // Add click event listeners to each item in the scrollable box
        for (let i = 0; i < items.length; i++) {
            const itemName = items[i].getElementsByTagName('div')[0].textContent.toLowerCase();
            items[i].addEventListener('click', function() {
                showImage(itemName);
            });
        }

});

/*
FOR THE MODAL
function showImage(item, date, graphData) {
    var modal = document.getElementById('myModal');
    var modalImg = document.getElementById('modal-image');
    var modalTicker = document.getElementById('modal-ticker');
    var modalDate = document.getElementById('modal-date');
    var graphCanvas = document.getElementById('graph-canvas');

    modalTicker.textContent = item;
    modalDate.textContent = "Last Scrape Date: " + date;
    modalImg.src = getImageSource(item); // Implement getImageSource to return the correct image URL

    // Implement a function to draw the graph using the provided graphData
    drawGraph(graphCanvas, graphData);

    modal.style.display = "flex";
}

// Placeholder function to draw a graph
function drawGraph(canvas, data) {
    var ctx = canvas.getContext('2d');
    // Implement the graph drawing logic here using a library like Chart.js or directly with canvas
    // Example using Chart.js:
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            // Chart options
        }
    });
}

function getImageSource(item) {
    if (item === 'rtx 4080') {
        return "https://th.bing.com/th/id/OIP.kvy6yciEcE6bRs_mhM0HUAAAAA?rs=1&pid=ImgDetMain";
    }
    // Add other cases for different items
    return "";
}
*/