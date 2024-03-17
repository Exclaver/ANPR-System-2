# import easyocr

# # Initialize the EasyOCR reader
# reader = easyocr.Reader(['en'])

# # Path to the image file
# image_path = 'plates\scaned_img_11.jpg'

# # Perform OCR on the image
# result = reader.readtext(image_path)

# # Print the detected text
# for detection in result:
#     text = detection[1]  # Extract the text part from the detection
#     print(text)
import requests
import json


def ocr_space_file(filename, overlay=False, api_key='K87012709288957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': 2
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='K87012709288957', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': 3
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


# test_file = ocr_space_file(
#     filename='plates\image.png', language='eng')
# data = json.loads(test_file)
# parsed_text = data["ParsedResults"][0]["ParsedText"]
# print("Parsed Text:", parsed_text)

# test_url = ocr_space_url(file='plates\scaned_img_0.jpg')
# print(test_file)
