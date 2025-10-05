import cv2
import pytesseract



pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


img = cv2.imread("../OPEN-CV/photos/herbata.jpg")
if img is None:
    print(" Nie można wczytać obrazu.")
    exit()


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)


custom_config = r'--oem 3 --psm 6'
data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT, config=custom_config)


target_phrase = "lipton"
target_words = target_phrase.lower().split()

print(" Wykryte słowa przez OCR:")
for i, word in enumerate(data['text']):
    print(f"{i}: '{word}'")

matched_boxes = []
found_words = []
reference_center = None

for i, word in enumerate(data['text']):
    clean_word = word.lower().strip().replace(" ", "").replace(".", "").replace(",", "")
    if clean_word in target_words:
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        center = (x + w // 2, y + h // 2)

        if reference_center is None and clean_word == target_words[0]:
            reference_center = center
            matched_boxes.append((x, y, x + w, y + h))
            found_words.append(clean_word)
            cv2.putText(img, word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        elif reference_center is not None and clean_word in target_words[1:]:
            dx = abs(center[0] - reference_center[0])
            dy = abs(center[1] - reference_center[1])
            if dx < 150 and dy < 100:
                matched_boxes.append((x, y, x + w, y + h))
                found_words.append(clean_word)
                cv2.putText(img, word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)


if all(word in found_words for word in target_words):
    print(f" Znaleziono frazę: {target_phrase}")
    x1 = min(box[0] for box in matched_boxes)
    y1 = min(box[1] for box in matched_boxes)
    x2 = max(box[2] for box in matched_boxes)
    y2 = max(box[3] for box in matched_boxes)

    padding = 40
    x = max(x1 - padding, 0)
    y = max(y1 - padding, 0)
    w = min((x2 - x1) + 2 * padding, img.shape[1] - x)
    h = min((y2 - y1) + 2 * padding, img.shape[0] - y)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
else:
    print(f" Nie znaleziono pełnej frazy: {target_phrase}")


cv2.imshow("Wykryty produkt", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
