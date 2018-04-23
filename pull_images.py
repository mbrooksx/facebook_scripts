import requests
import json
import argparse

from sys import exit

parser = argparse.ArgumentParser(description='Pull all tagged images from Facebook')
parser.add_argument('access_token', help='Access Token from Facebook (Generate '
        'at https://developers.facebook.com/tools/explorer/')

args = parser.parse_args()

# Import the first data.
tagged = requests.get("https://graph.facebook.com/v2.12/me/photos?fields=images&limit=25&access_token=" + args.token).json()

# Loop until all pagination is complete.
images = 0

if not "data" in tagged:
    print("Your token is invalid. Please generate a new token at "
    "https://developers.facebook.com/tools/explorer/, ensuring user_photos and "
    "user_posts are granted.")
    exit(0)

while True:
    for pics in tagged["data"]:
        images += 1
        # Select image with the max width.
        best_image = max(pics["images"], key = lambda x: x["width"])
        # Download image, keeping FB's terrible filenames
        url = best_image["source"]
        filename = url.split("/")[-1]
        filename = filename.split("?")[0]
        r = requests.get(url, timeout=0.5)

        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)

    # Break out of loop if there are no more pages.
    if not "next" in tagged["paging"]:
        break
    # Otherwise, proceed to next page.
    tagged = requests.get(tagged["paging"]["next"]).json()

print("Total photos downloaded: %d" % images)


