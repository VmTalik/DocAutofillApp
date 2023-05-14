import cv2
import easyocr

image_name = "5_image.jpg"
image = cv2.imread(image_name)
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def rotation():
    (h, w) = image.shape[:2]
    center = (int(w / 2), int(h / 2))
    if w > h:
        rotated = cv2.rotate(img_gray, cv2.ROTATE_90_CLOCKWISE)
    else:
        rotation_matrix = cv2.getRotationMatrix2D(center, 90, 0.6)
        rotated = cv2.warpAffine(img_gray, rotation_matrix, (w, h))
    cv2.imshow("Rotated image", rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return rotated


def ocr_recognition(path_img):
    reader = easyocr.Reader(["ru"])
    result = reader.readtext(path_img, detail=0, paragraph=True, text_threshold=0.8)
    return result


if __name__ == "__main__":
    print(ocr_recognition(image))
    print(ocr_recognition(rotation()))
