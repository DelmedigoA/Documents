from surya.ocr import run_ocr
from surya.model.detection import model as segformer
from surya.model.recognition.model import load_model
from surya.model.recognition.processor import load_processor

class OCR:
  def __init__(self):
    self.det_processor, self.det_model = (None, None)
    self.rec_model, self.rec_processor = (None, None)

  def load(self):
    self.det_processor, self.det_model = segformer.load_processor(), segformer.load_model()
    self.rec_model, self.rec_processor = load_model(), load_processor()
    print("Model Loaded Successfully")

  @staticmethod
  def normalize_bbox(bbox, width, height):
    return [
        int(1000 * (bbox[0] / width)),
        int(1000 * (bbox[1] / height)),
        int(1000 * (bbox[2] / width)),
        int(1000 * (bbox[3] / height)),
    ]

model = OCR()
model.load()
