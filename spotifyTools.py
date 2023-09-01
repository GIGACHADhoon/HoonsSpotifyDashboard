#from sql_tools import azSqlDB
from df_tools import azSqlDF
class spotifyTools:

    def __init__(self):
        self.dbcon = azSqlDF()
        self.ltr = self.dbcon.getLTRankings()
        self.mtr = self.dbcon.getMTRankings()
        self.str = self.dbcon.getSTRankings()
        self.snippets = self.dbcon.getSnippets()
        self.images = self.dbcon.getImages()
        self.chosen = self.ltr

    def getltRankings(self):
        return self.ltr
    
    def getmtRankings(self):
        return self.mtr
    
    def getstRankings(self):
        return self.str
    
    def getSnippets(self):
        return self.snippets
    
    def getImages(self):
        return self.images
    
    def getChosen(self):
        return self.chosen

    def updateChosen(self,sel):
        if sel == 'ltr':
            self.chosen = self.ltr
        elif sel == 'mtr':
            self.chosen = self.mtr
        else:
            self.chosen = self.str