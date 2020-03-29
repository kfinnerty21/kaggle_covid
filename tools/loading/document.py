import errno
import json
import os

from loading.cleaning import clean


class document():
    def __init__(self, file_path):
        if file_path:
            with open(file_path) as file:
                data = json.load(file)
                self.paper_id = data['paper_id']
                self.title = data['metadata']['title']
                self.abstract_tripples = {}
                self.text_tripples = {}
                self.key_phrases = ""
                self.abstract = ""
                self.text = ""
                self.entities = {}

                for section in data['abstract']:
                    self.abstract = self.abstract + "\n" + section["text"]

                for section in data['body_text']:
                    self.text = self.text + "\n" + section['text']

    def clean_text(self):
        self.abstract = clean(self.abstract)
        self.text = clean(self.text)

    def combine_data(self):
        self.data = {'paper_id': self.paper_id,
                     'title': self.title,
                     'abstract': self.abstract,
                     'text': self.text,
                     'abstract_tripples': self.abstract_tripples,
                     'text_tripples': self.text_tripples,
                     'key_phrases': self.key_phrases,
                     'entities': self.entities}

    def extract_data(self):

        self.paper_id = self.data['paperr_id']
        self.title = self.data['title']
        self.abstract = self.data['abstract']
        self.text = self.data['text']
        self.abstract_tripples = self.data['abstract_tripples']
        self.text_tripples = self.data['text_tripples']
        self.key_phrases = self.data['key_phrases']
        self.entities = self.data['entities']

    def save(self, dir):
        self.combine_data()

        if not os.path.exists(os.path.dirname(dir)):
            try:
                os.makedirs(os.path.dirname(dir))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(dir, 'w') as json_file:
            json_file.write(json.dumps(self.data))

    def load_saved_data(self, dir):
        with open(dir) as json_file:
            self.data = json.load(json_file)
        self.extract_data()