# Film-Site

1) main.py: is the file that runs the api. Use this to start the api on localhost:5000
2) Datasets: contains the files necessary for object detection (training models and weights)
3) static/images/: The images we want to display in our website must go in here
render every image in our static/images folder. 
4) static/detected/: Here is where the images used for open ai api are stored. main.py uses opencv to automatically store the images here. One image will be a resized (1024x1024) version of the original image called "orig_resized", and the other will be the mask, called "detected." They must be saved as .png
5) static/read.js: This is the javascript created by running string_images.js using node js. read.js has javascript our html uses to properly 
6) Templates: Store all our templates here. Our webpage html file is here, as well as string_images.js, which is ran with node.js everytime you add new images to static/images/. This will write a new read.js file that the html will use to render all the images.

Notes:
read.js is already up to date with the images i have saved in static/images/ so it should run fine. If you add new images, you need to run the string_images.js with node js in order to update read.js, so that all the images show up.

You need to have your own openai api key, assign it to api_key in the first line of detect_object() function.

To use the website, select an image, then enter a prompt, then click enter. a url will be displayed, open it to see your new image. If no object is detected, go back and try with another image.

