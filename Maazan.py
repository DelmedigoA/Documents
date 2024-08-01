from Documents.Page import Page
from Documents.Document import Document

class MaazanPage(Page):
    def __init__(self, num, img, data):
        super().__init__(num, img, data)
        self.beur_tokens = []
        self.found_beur_tokens = 0
        self.find_beur_tokens()

    def find_beur_tokens(self):
        if self.found_beur_tokens <= 2:
            for token in self.tokens:
                if any(str(i) in token.search_text for i in ['אור', 'באור', 'ביאור', 'מידע נוסף', 'נוסף']) and len(token.search_text) < 12:
                    token.tag = 'beur'
                    self.beur_tokens.append(token)
                    self.found_beur_tokens += 1

class Maazan(Document):
    def __init__(self, path, img_specs, ocr):
        super().__init__(path, img_specs, ocr)

    def create_page(self, num, img, data):
        return MaazanPage(num, img, data)
