import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd
import geopandas as gpd
load_dotenv()

class azSqlDB:
    def __init__(self):
        server = os.getenv("server")
        database = os.getenv("database")
        username = os.getenv("us")
        password = os.getenv("pw")
        self.conString = 'Driver={ODBC Driver 17 for SQL Server};SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+ \
            ';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;'

    def getLTRankings(self):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT ltr.songID,ranking, songName ,artistName,featuring,album,CONVERT(VARCHAR(10),releaseDate,111) as date,popularity \
                    FROM [dbo].[long_termRankings] ltr  \
                    LEFT JOIN [dbo].[SongDetails] sd on (ltr.songID = sd.songID) \
                    LEFT JOIN [dbo].[Artist] a ON (sd.artistID = a.artistID) \
                    ORDER BY ranking"
                cursor.execute(query)   
                rows = cursor.fetchall()
                df_dict = {'id':[],'Ranking':[],'Song Name':[],'Artist':[],'Featuring':[],'Album':[],'Release Date':[],'popularity':[]}
                for row in rows:
                    df_dict['id'].append(row[0])
                    df_dict['Ranking'].append(row[1])
                    df_dict['Song Name'].append(row[2])
                    df_dict['Artist'].append(row[3])
                    df_dict['Featuring'].append(row[4])
                    df_dict['Album'].append(row[5])
                    df_dict['Release Date'].append(row[6])
                    df_dict['popularity'].append(row[7])
                df = pd.DataFrame(df_dict)
                df.set_index('id')
                return df

    def getMTRankings(self):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT mtr.songID,ranking, songName ,artistName,featuring,album,CONVERT(VARCHAR(10),releaseDate,111) as date,popularity \
                    FROM [dbo].[medium_termRankings] mtr  \
                    LEFT JOIN [dbo].[SongDetails] sd on (mtr.songID = sd.songID) \
                    LEFT JOIN [dbo].[Artist] a ON (sd.artistID = a.artistID) \
                    ORDER BY ranking"
                cursor.execute(query)   
                rows = cursor.fetchall()
                df_dict = {'id':[],'Ranking':[],'Song Name':[],'Artist':[],'Featuring':[],'Album':[],'Release Date':[],'popularity':[]}
                for row in rows:
                    df_dict['id'].append(row[0])
                    df_dict['Ranking'].append(row[1])
                    df_dict['Song Name'].append(row[2])
                    df_dict['Artist'].append(row[3])
                    df_dict['Featuring'].append(row[4])
                    df_dict['Album'].append(row[5])
                    df_dict['Release Date'].append(row[6])
                    df_dict['popularity'].append(row[7])
                df = pd.DataFrame(df_dict)
                df.set_index('id')
                return df
            
    def getSTRankings(self):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT str.songID,ranking, songName ,artistName,featuring,album,CONVERT(VARCHAR(10),releaseDate,111) as date,popularity \
                    FROM [dbo].[short_termRankings] str  \
                    LEFT JOIN [dbo].[SongDetails] sd on (str.songID = sd.songID) \
                    LEFT JOIN [dbo].[Artist] a ON (sd.artistID = a.artistID) \
                    ORDER BY ranking"
                cursor.execute(query)   
                rows = cursor.fetchall()
                df_dict = {'id':[],'Ranking':[],'Song Name':[],'Artist':[],'Featuring':[],'Album':[],'Release Date':[],'popularity':[]}
                for row in rows:
                    df_dict['id'].append(row[0])
                    df_dict['Ranking'].append(row[1])
                    df_dict['Song Name'].append(row[2])
                    df_dict['Artist'].append(row[3])
                    df_dict['Featuring'].append(row[4])
                    df_dict['Album'].append(row[5])
                    df_dict['Release Date'].append(row[6])
                    df_dict['popularity'].append(row[7])
                df = pd.DataFrame(df_dict)
                df.set_index('id')
                return df

    def getSnippets(self):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT * FROM [dbo].[Snippets]"
                cursor.execute(query)   
                rows = cursor.fetchall()
                df_dict = {'id':[],'Snippets':[]}
                for row in rows:
                    df_dict['id'].append(row[0])
                    df_dict['Snippets'].append(row[1])
                df = pd.DataFrame(df_dict)
                df.set_index('id')
                return df

    def getImages(self):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT songID,imgURL FROM [dbo].[Images] WHERE imgDims = '640x640'"
                cursor.execute(query)   
                rows = cursor.fetchall()
                df_dict = {'id':[],'imgURL':[]}
                for row in rows:
                    df_dict['id'].append(row[0])
                    df_dict['imgURL'].append(row[1])
                df = pd.DataFrame(df_dict)
                df.set_index('id')
                return df