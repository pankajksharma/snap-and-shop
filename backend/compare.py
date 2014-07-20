import MySQLdb
import cv2, json
from matplotlib import pyplot as plt

db = MySQLdb.connect(
        'localhost',
        'root',
        'root',
        'test'
    )

cur = db.cursor()

def return_top_results(img_path, n=2):
    cur.execute("SELECT * FROM android")
    row_map = {}
    img1 = cv2.imread(img_path,0)          # queryImage
    for row in cur.fetchall():
        print row[5]

        img2 = cv2.imread('hackthon/images/'+row[5], 0) # trainImage

        # Initiate SIFT detector
        sift = cv2.SIFT()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)

        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)

        # Apply ratio test
        good = 0
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good += 1
        row_map[row] = good
    best_results = sorted(row_map, key=(row_map.get))
    best_results.reverse()
    return best_results

def get_json(best_results, n=2):
    brs = []
    for br in best_results[:n]:
        brs.append({
            "name": br[3],
            "description": br[4],
            "url": br[5],
            "sellers": [ 
                br[7], br[9], br[6], br[8]
            ]
        })
    return json.dumps(brs)

# print return_top_results("hackthon/images/beginning-linux-programming-400x400-imadxphz96fwkdxs.jpeg")