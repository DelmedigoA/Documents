import os
from Documents.Img_Specs import Image_Specifications
from Documents.Page import Page
from Documents.Maazan import Maazan, MaazanPage
from Documents.Document import Document
import pandas as pd

class Documents:
    def __init__(self, dir_path, ocr, image_specifications=Image_Specifications(), test=None):
        self.dir_path = dir_path
        self.image_specifications = image_specifications
        self.files = [os.path.join(self.dir_path, file) for file in os.listdir(self.dir_path) if file.endswith('.pdf')]
        self.documents_num = len(self.files) if test is None else test
        self.ocr = ocr
        self.docs = []
        self.data_frame = pd.DataFrame()
        self.dict_data = {}

    def read_docs(self):
        for file in self.files[:self.documents_num]:
            doc = Maazan(path=file, img_specs=self.image_specifications, ocr=self.ocr)
            doc.to_imgs()
            doc.build_pages()
            self.docs.append(doc)

    def build_data_frame(self):
        df = pd.DataFrame()
        for doc in self.docs:
            tmp_df = doc.to_pandas()
            df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
        self.data_frame = df

    def build_dict(self):
        doc_names = self.data_frame['name'].unique().tolist()
        for doc_name in doc_names:
            self.dict_data[doc_name] = self.data_frame.loc[self.data_frame['name'] == doc_name]

    def print_token_affinity(self, doc_idx, page_idx, tk_idx):
        try:
            token = self.docs[doc_idx].pages[page_idx].tokens[tk_idx]
            print('Token:', token.text)
            if token.vertical_affinity:
                print('Vertical Affinity:', token.vertical_affinity.text)
                print('Vertical Affinity Order:', token.vertical_affinity.order)
            else:
                print('No Vertical Affinity')
            if token.horizontal_affinity:
                print('Horizontal Affinity:', token.horizontal_affinity.text)
                print('Horizontal Affinity Order:', token.horizontal_affinity.order)
            else:
                print('No Horizontal Affinity')
        except IndexError as e:
            print("IndexError:", e)
        except Exception as e:
            print("An error occurred:", e)
