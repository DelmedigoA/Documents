import numpy as np
import pandas as pd

class Page:
    def __init__(self, num, img, data):
        self.num = num
        self.img = img
        self.data = data
        self.tokens = []
        self.build_tokens()

        self.year_tokens = []
        self.found_year_tokens = 0
        self.find_year_tokens()

        self.number_tokens = []
        self.found_number_tokens = 0
        self.find_number_tokens()
        self.find_vertical_connection()
        self.find_horizontal_connection()

    def build_tokens(self):
        for row in self.data.itertuples():
            token = Token(row.text, row.bbox, row.Index)
            self.tokens.append(token)

    def find_year_tokens(self):
        if self.found_year_tokens <= 2:
            for token in self.tokens:
                if any(str(i) in token.search_text for i in range(2015, 2025)):
                    token.tag = 'year'
                    self.year_tokens.append(token)
                    self.found_year_tokens += 1

    def find_number_tokens(self):
        if self.found_number_tokens <= 2:
            for token in self.tokens:
                try:
                    int(token.search_text)
                    if token.tag != 'year':
                        token.tag = 'number'
                        self.number_tokens.append(token)
                        self.found_number_tokens += 1
                except:
                    pass

    def find_vertical_connection(self):
        for token in self.tokens:
            if token.tag == 'number':
                diffs = [np.abs(token.bbox[0] - year_token.bbox[0]) for year_token in self.year_tokens]
                token.vertical_affinity = self.year_tokens[np.argmin(diffs)]

    def find_horizontal_connection(self):
        for token in self.tokens:
            if token.tag == 'number':
                other_tokens_list = [t for t in self.tokens if t.tag is None]
                diffs = [np.abs(token.bbox[1] - other_token.bbox[1]) for other_token in other_tokens_list]
                token.horizontal_affinity = other_tokens_list[np.argmin(diffs)]
