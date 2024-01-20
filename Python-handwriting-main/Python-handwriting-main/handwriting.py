import pywhatkit as kit
import cv2
Handwritten = input("Enter the handwriting: ")
kit.text_to_handwriting(Handwritten, save_to="handwriting.png")
img = cv2.imread("handwriting.png")
cv2.imshow("Handwritten", img)
cv2.waitKey(0)
cv2.destroyAllWindows()