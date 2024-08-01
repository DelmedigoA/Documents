class Token:
    def __init__(self, text, bbox, order):
        self.text = text
        self.search_text = self.clean_for_search()
        self.bbox = bbox
        self.order = order
        self.tag = None
        self.horizontal_affinity = None
        self.vertical_affinity = None

    def clean_for_search(self):
        return self.text.replace(' ', '').replace('.', '').replace(',', '')
