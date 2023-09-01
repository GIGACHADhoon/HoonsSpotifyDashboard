import pandas as pd

class azSqlDF:
    def __init__(self):
        self.dfltr = pd.read_csv('ltr.csv')
        self.dfltr.set_index('id')
        self.dfSnipets = pd.read_csv('snippets.csv')
        self.dfSnipets.set_index('id')
        self.dfImages = pd.read_csv('images.csv')
        self.dfImages.set_index('id')

    def getLTRankings(self):
                return self.dfltr

    def getSnippets(self):
                return self.dfSnipets

    def getImages(self):
                return self.dfImages