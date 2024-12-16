import base64
from openai import OpenAI
from dotenv import load_dotenv
import cv2
import ast
import os


load_dotenv()

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  img = cv2.imread(image_path)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  gray = cv2.resize(gray,None,fx=0.5,fy=0.5)
  buffer = cv2.imencode('.jpg',gray)[1]
  buffer_objects = buffer.tobytes()

  return base64.b64encode(buffer_objects).decode('utf-8')



def get_OCR(image_path):

  base64_image = encode_image(image_path=image_path)
  model = os.getenv("MODEL_NAME")
  response = client.chat.completions.create(
    model=model,
    messages=[{"role":'system','content':"You are ocr agent taking an image and return the brand name only"},
              {"role":'system','content':"The brand could be in Arabic or English or both"},
              {"role":"system",'content':"Your answer should be a python dict only with two keys EN for english name if exist AR for Arabic name if exist"},
              {"role":'system',"content":"There is four cases Ar and EN names so create dict with EN and AR key, Ar name only create dict with AR key only, EN only create dict with EN key only if an able to recognize the brand return emty dict"},

      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What is in this brand?",
          },
          {
            "type": "image_url",
            "image_url": {
              "url":  f"data:image/jpeg;base64,{base64_image}"
            },
          },
        ],
      }
    ],
  )

  
  d = response.choices[0].message.content.replace("```","").replace("python","").replace('json','')
  d = ast.literal_eval(d)

  return d


def get_names(d):
  engs , aras = " "," "
  for k,v in d.items():
    if k == 'EN':
      engs+=v
    elif k == 'AR':
      aras += v


    if 'EN' not in d:
        engs+=""
    if 'AR' not in d:
        aras+=""
  return engs , aras


# start = counter()
# pages,cats = extract('/home/ibrahim/Desktop/freelance/free.pdf')

# aras, engs = [],[]
# images_paths = os.listdir('/home/ibrahim/Desktop/freelance/Images')

# for i,img in enumerate(images_paths):
#     img_path = os.path.join('/home/ibrahim/Desktop/freelance/Images',img)
#     d = get_OCR(img_path)
#     eng , ara = get_names(d)
#     aras.append(ara)
#     engs.append(eng)
#     os.remove(img_path)

# end = counter()
# print((pages),(cats),(aras),(engs))
# df = pd.DataFrame({"Arabic":aras,"English":engs,'Page Number':pages,"Category":cats})

# df.to_excel("names.xlsx")
# print(f"OCR ends after {end - start} sec")
# print(f"Total time take to OCR {len(images_paths)} Image is {end - start} sec")

