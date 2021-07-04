
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
import xmltodict as xtd
import json,requests
import regex as re
def noPlateRecognization(img_path):
    try:
        img = cv2.imread(img_path,cv2.IMREAD_COLOR)
    except Exception as e:
        print(e)
        return None
    img = cv2.resize(img, (600,400) )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    edged = cv2.Canny(gray, 30, 200) 
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None


    for c in contours:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        return None
    
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

    mask = np.zeros(gray.shape,np.uint8)

    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1)

    new_image = cv2.bitwise_and(img,img,mask=mask)

    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    text = pytesseract.image_to_string(Cropped, config='--psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    print("License Plate Recognition\n")
    print("Detected license plate Number is:",text)
    text=text.replace(' ','')
    print("Detected 2 license plate Number is:",text)

    return text


def getVehicalInfo(plt_no,username,returnJson=False):
        r=requests.get(f"http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={plt_no}&username={username}")
        data=xtd.parse(r.content)
        jsonData=data['Vehicle']['vehicleJson']
        if returnJson:
            return jsonData
        dt=json.loads(jsonData)
        return {
            
            "Description": dt["Description"],
            "RegistrationYear": dt["RegistrationYear"],
            "CarMake": dt["CarMake"]['CurrentTextValue'],
            "CarModel": dt["CarModel"]['CurrentTextValue'],
            "Variant": dt["Variant"],		
            "Owner": dt["Owner"],
            "Insurance": dt["Insurance"],
            "Location": dt["Location"],
            "RegistrationDate": dt["RegistrationDate"],
            "EngineNumber": dt["EngineNumber"],
            "VechileIdentificationNumber": dt["VechileIdentificationNumber"],
            "VehicleType": dt["VehicleType"],
            "ImageUrl": dt["ImageUrl"]

        }