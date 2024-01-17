import argparse
import requests
import json
import time

import cv2
import numpy as np



def url_to_image(url, readFlag=cv2.IMREAD_COLOR) -> cv2.typing.MatLike:
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Could not download image")
        return np.empty()
    #
    image = np.asarray(bytearray(resp.content), dtype="uint8")
    image = cv2.imdecode(image, readFlag)
    # return the image
    return image


def detect_blur(image_url: str, threshold: float, output_name: str, write_output: bool = False) -> str:
    """Largely inspired by https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/"""
    
    # Read the image
    image = url_to_image(image_url)
    if image.size==0:
        return 'not processed'
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Laplacian filter for edge detection
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    # Calculate maximum intensity and variance
    laplacian_variance = laplacian.var()

    # Initialize result variables
    blur_text = f"not blurry ({laplacian_variance})"

    # Check blur condition based on variance of Laplacian image
    if laplacian_variance < threshold:
        blur_text = f"blurry ({laplacian_variance})"

    

    # Display the image
    if write_output:
        # Add labels to the image
        cv2.putText(image, blur_text, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imwrite(output_name, image)

    return blur_text



def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type = str, help="input url")
    parser.add_argument("-j", type = str, default="assets/list_images.json", help="path to json file with list of urls")
    parser.add_argument("-t", type=float, default=25.42, help="blur threshold")
    args = parser.parse_args()

    # Get list of image URLs
    if args.j:
        with open(args.j,'r') as fn:
            raw_json = json.load(fn) 
            image_paths = raw_json['img_lst']
    elif args.i:
        image_paths = [args.i]  
    else:
        image_paths = []
        print("You don't give me anything to process, so I am doing nothing.")          
    # Process each image
    for idx_img, image_path in enumerate(image_paths):
        st = time.time()
        decision = detect_blur(
            image_url = image_path, 
            threshold = args.t, 
            output_name=f"examples/output_{idx_img:03d}.jpg",
            write_output=True
            )
        print(f"- output {idx_img:03d} -> {decision} -> done in {int(1000*(time.time()-st))} ms")


if __name__ == "__main__":
    main()