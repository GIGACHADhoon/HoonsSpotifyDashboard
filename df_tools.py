import pandas as pd

class azSqlDF:
    def __init__(self):
        self.dfltr = pd.read_csv('ltr.csv')
        self.dfltr.set_index('id')
        self.dfmtr = pd.read_csv('mtr.csv')
        self.dfmtr.set_index('id')
        self.dfstr = pd.read_csv('str.csv')
        self.dfstr.set_index('id')
        self.dfSnipets = pd.read_csv('snippets.csv')
        self.dfSnipets.set_index('id')
        self.dfImages = pd.read_csv('images.csv')
        self.dfImages.set_index('id')

    def getLTRankings(self):
                return self.dfltr
    
    def getMTRankings(self):
                return self.dfmtr
    
    def getSTRankings(self):
                return self.dfstr

    def getSnippets(self):
                return self.dfSnipets

    def getImages(self):
                return self.dfImages