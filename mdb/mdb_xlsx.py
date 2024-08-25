import pandas as pd
import warnings

class CMdbXlsx:
    KEY_TITLE = 'Title'
    KEY_POSTER = 'Poster'
    KEY_TAGLINE = 'Tagline'
    KEY_GENRES = 'Genres'
    KEY_RELEASE_YEAR = 'Release Year'
    KEY_FORMAT = 'Format'
    KEY_MY_RATING = 'My rating'
    KEY_DESCRIPTION = 'Description'
    KEY_BARCODE = 'Barcode'
    KEY_COUNTRIES = 'Countries'
    KEY_DURATION = 'Duration'
    KEY_TOOK = 'Took'
    KEY_WATCHED = 'Watched'
    KEY_BOX = 'box'
    KEY_TITEL_IN_SAMMLUNG = 'Titel in Sammlung'
    KEY_BACKDROPS = 'Backdrops'
    KEY_DIRECTOR = 'Director'
    KEY_ACTORS = 'Actors'
    KEY_PRODUCER = 'Producer'
    KEY_PRODUCTION_COMPANIES = 'Production companies'
    KEY_IMDB_LINK = 'IMDb Link'
    KEY_HOMEPAGE = 'Homepage'
    KEY_TRAILER = 'Trailer'
    KEY___ID = '__id'

    KEY_BOX_UNSPECIFIED = 'unspecified'

    def __init__(self, database) -> None:
        '''Constructor'''
        self.database = database
        self.data = None

        pass

    def read(self):
        ''' Read in the database '''
        df = pd.read_excel(self.database)

        # Change data frame in dictionary 
        self.data = df.to_dict(orient='records')

    def sort_box_oriented_titles(self):
        '''Return the data oriented by boxes and titles'''
        db_box = {}

        for record in self.data:
            box = record[self.KEY_BOX]
            if box == None:
                warnings.warn(f"box for {record} is not specified")
                box = self.KEY_BOX_UNSPECIFIED 
            elif record[self.KEY_BOX] not in db_box.keys():
                db_box[record[self.KEY_BOX]] = []
            db_box[record[self.KEY_BOX]].append(record[self.KEY_TITLE])            
        return db_box