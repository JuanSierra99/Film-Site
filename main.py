import quart
from quart import Quart
import cv2
import numpy as np
import openai

#static_folder is changed to the folder we have all the images we want to serve. We then use the correct pathname in the html
# other option is to remove the assignment and have a static folder directory with our project, and we copy the image path from there
app = Quart(__name__)

@app.route('/')
async def test():
        return await quart.render_template("home.html"), 200

@app.route('/detect')
async def detect_object():
        #----------detection--------------#
        image = cv2.imread("../Film-Site/static/images/" + quart.request.args.get('image'))
        image = cv2.resize(image, (1024, 1024)) #openai api uses images size 1024 x 1024
        cv2.imwrite('../Film-Site/static/detected/orig_resized.png', image)  # has to be png for transp.
        h = image.shape[0]
        w = image.shape[1]
        coordinates = [] # to store the coordinates of every object detected
        # path to the weights and model files
        weights = "../Film-Site/Datasets/frozen_inference_graph.pb"
        model = "../Film-Site/Datasets/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt.txt"
        # load the MobileNet SSD model trained  on the COCO dataset
        net = cv2.dnn.readNetFromTensorflow(weights, model)

        # create a blob from the image
        blob = cv2.dnn.blobFromImage(image, 1.0 / 127.5, (320, 320), [127.5, 127.5, 127.5])
        # pass the blob through our network and get the output predictions
        net.setInput(blob)
        output = net.forward()
        # loop over the number of detected objects
        for detection in output[0, 0, :, :]:  # output[0, 0, :, :] has a shape of: (100, 7)
                # the confidence of the model regarding the detected object
                probability = detection[2]

                # if the confidence of the model is lower than 50%,
                # we do nothing (continue looping)
                if probability < 0.5:
                        continue

                # perform element-wise multiplication to get
                # the (x, y) coordinates of the bounding box
                box = [int(a * b) for a, b in zip(detection[3:7], [w, h, w, h])]
                box = tuple(box)
                coordinates.append(box)
                #-----------to see what we are cropping out ------------#
                # draw the bounding box of the object
                # cv2.rectangle(image, box[:2], box[2:], (0, 255, 0), thickness=2)

                # extract the ID of the detected object to get its name
                # class_id = int(detection[1])
                # draw the name of the predicted object along with the probability
                # label = f"{probability * 100:.2f}%"
                # cv2.putText(image, label, (box[0], box[1] + 15),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # -----------to see what we are cropping out ------------#
        # ----------detection--------------#
        if len(coordinates) == 0: # if no coordinates, then no object detected. return error
            return {"Objects detected": "0"}, 400
        # ----------masking--------------#
        alpha = np.full((image.shape[0], image.shape[1]), 256) # for rgba
        result = np.dstack((image, alpha))
        for box in coordinates: # for every set of coodinates, we mask it (for when we have multiple objects)
                for i in range(box[1], box[3]):
                        for j in range(box[0], box[2]):
                                result[i, j] = (0, 0, 0, 0)
                cv2.imwrite('../Film-Site/static/detected/detected.png', result) # add mask for every object detected
        # ----------masking--------------#
        #-------------AI--------------#
        prompt = quart.request.args.get('prompt') # get the prompt from frontend url argument
        response = openai.Image.create_edit(api_key="",
                                            n=1,
                                            image=open(
                                                "../Film-Site/static/detected/orig_resized.png",
                                                "rb"),
                                            mask=open("../Film-Site/static/detected/detected.png", "rb"),
                                            prompt=prompt,
                                            size="1024x1024"
                                            )
        image_url = response['data'][0]['url']
        # -------------AI--------------#
        return str(image_url), 200

app.run(debug=True)
