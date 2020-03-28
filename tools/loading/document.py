import json
from loading.extract import clean

class document():
    def __init__(self, file_path):
        with open(file_path) as file:
            data = json.load(file)
            self.paper_id = data['paper_id']
            self.title = data['metadata']['title']
            self.abstract_tripples = {}
            self.text_tripples = {}
            self.abstract = ""
            self.text = ""

            for section in data['abstract']:
                self.abstract = self.abstract + "\n" + section["text"]

            for section in data['body_text']:
                self.text = self.text + "\n" + section['text']


    def clean_text(self):
        self.abstract = clean(self.abstract)
        self.text = clean(self.text)

    def save(self, dir):
        self.data = {'paper_id':self.paper_id,
                     'title':self.title,
                     'abstract':self.abstract,
                     'text':self.text,
                     'abstract_tripples':self.abstract_tripples,
                     'text_tripples':self.text_tripples}

        with open(dir, 'w') as json_file:
            json.dump(self.data, json_file)







