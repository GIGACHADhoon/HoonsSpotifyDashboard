#from sql_tools import azSqlDB
from df_tools import azSqlDF
class spotifyTools:

    def __init__(self):
        self.dbcon = azSqlDF()
        self.ltr = self.dbcon.getLTRankings()
        self.snippets = self.dbcon.getSnippets()
        self.images = self.dbcon.getImages()

    def getRankings(self):
        return self.ltr
    
    def getSnippets(self):
        return self.snippets
    
    def getImages(self):
        return self.images