import cv2
import numpy as np
img = cv2.imread('../OPEN-CV/photos/monety.jpg')
if img is None:
    raise FileNotFoundError("Nie znaleziono pliku 'monety.jpg'!")
output = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=23,
    param1=100,
    param2=35,
    minRadius=20,
    maxRadius=55
)
if circles is not None:
    circles = np.uint16(np.around(circles))
    print(f"Znaleziono {len(circles[0])} monet(y).")
    for i in circles[0, :]:
        cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 3)
        cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)
else:
    print("Nie znaleziono żadnych monet.")
cv2.imshow("Monety - wykrywanie", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
