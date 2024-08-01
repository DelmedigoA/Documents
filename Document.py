import pdf2image
import numpy as np
import pandas as pd  

class Document:
    def __init__(self, path, img_specs, ocr, langs=['he']):
        self.path = path
        self.relative_path = self.path.split('/')[-1]
        self.name = self.relative_path.split('.')[0]
        self.langs = langs
        self.img_specs = img_specs
        self.length = None
        self.imgs = None
        self.ocr = ocr
        self.pages = []
        self.data_frame = None
        self.dict_ = None

    def to_imgs(self):
        self.imgs = pdf2image.convert_from_path(self.path, size=(self.img_specs.size, self.img_specs.size), dpi=self.img_specs.dpi, grayscale=self.img_specs.is_grayscale)
        self.length = len(self.imgs)
        print(f"Converted {self.length} images of '{self.name}'\n")

    def build_pages(self):
        for idx in range(self.length):
            page_data = self.img_to_data(self.imgs[idx])[['text', 'bbox']]
            page = self.create_page(idx, self.imgs[idx], page_data)
            self.pages.append(page)
            print(f"Built {idx + 1} out of {self.length} pages\n")

    def create_page(self, num, img, data):
        return Page(num, img, data)

    def img_to_data(self, img) -> pd.DataFrame:
        predictions = run_ocr([img], [self.langs], model.det_model, model.det_processor, model.rec_model, model.rec_processor)
        pred_dict = predictions[0].dict()
        df = pd.DataFrame(pred_dict['text_lines'])[["bbox", "text"]]
        df['size'] = [self.img_specs.size] * len(df)
        df['bbox'] = df['bbox'].apply(lambda x: self.ocr.normalize_bbox(x, *(self.img_specs.size, self.img_specs.size)))
        return df

    def to_pandas(self):
        df = pd.DataFrame()
        for page in self.pages:
            tokens = page.tokens
            data = dict(
                name=[self.name] * len(tokens),
                page=[int(page.num)] * len(tokens),
                order=[token.order for token in tokens],
                text=[token.text for token in tokens],
                bbox=[token.bbox for token in tokens],
                vertical_affinity=[int(token.vertical_affinity.order) if token.vertical_affinity is not None else '-1' for token in tokens],
                horizontal_affinity=[int(token.horizontal_affinity.order) if token.horizontal_affinity is not None else '-1' for token in tokens]
            )
            tmp_df = pd.DataFrame(data)
            df = pd.concat([df, tmp_df], ignore_index=True)
        self.data_frame = df
        return df

    def to_dict(self):
        df = self.data_frame.copy()
        doc_names = df.name.unique().tolist()
        df_dict = {}
        for doc_name in doc_names:
            df_dict[doc_name] = df.loc[df.name == doc_name]
        self.dict_ = df_dict
        return df_dict
