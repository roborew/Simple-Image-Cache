## Simple Image Cache

Small flask App that process and caches images from a given URL using Open CV and Redis.

This is only a proof of concept and should not be used in production as 
there are no additional security measures in place.

The image can exist either within the chosen image directory configured 
in the env variables or can be fetched from a remote URL.

Usage:
       
        <img class="testImage" alt="image.jpg"
             src="http://127.0.0.1:8000/insecure/rs:500:500/c:200:200:200:200/ft:png/cp:40/test_image.jpeg">

        <img class="testImage" alt="image.jpg"
             src="http://127.0.0.1:8000/insecure/rs:400:400/ft:jpg/cp:90/https://images.pexels.com/photos/1330219/pexels-photo-1330219.jpeg">

Four operations are supported:
1. resize; rs: width:height
2. crop; c: x:y:width:height
3. format; ft: jpg|png|webp
4. compression; cp: 0-100


### Installation

Add and configure a .env file with the following variables:

```bash

CACHE_DIR="/PATH/NAME_OF_CACHE_DIR"
IMAGE_DIR="/PATH/NAME_OF_SRC_IMAGE_DIR"

IMAGE_FORMAT_DEFAULT="webp"
IMAGE_QUALITY_DEFAULT="80"



