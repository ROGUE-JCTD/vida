from vida.celery import app
# import brpy2
import logging
# import fileservice.helpers
import sys
logger = logging.getLogger(__name__)


@app.task
# def index_face(image):
#    logger.debug("Calling index_face on " + image)


# Re-index all of the files, need to do this on startup since we are maintaining the gallery in memory now
# This would be used for an admin, create a new end point so that the templates can be regenerated in case
# something goes wrong, all the templates can be cleared from DB, then re-created
@app.task
def reindex_files():
    # TODO: I am not absolutely sold that the __init.py__ code runs only once, so add some checking to save time
    # If the gallery has not been populated, or if the gallery has fewer files than in the folder we need to re-index
    result = []
    try:
 #       brpy2.initialize()
 #       brpy2.setAlgorithm("Read(Grayscale)+Cascade")
 #       brpy2.setGlobal("enrollAll", "true")
        file_names = fileservice.helpers.get_fileservice_files()
        for currFile in file_names:
            logger.debug("Indexing:" + currFile)
 #           result.append(brpy2.Template(currFile))
 #       brpy2.finalize()

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    return result


@app.task
def index_face(filename):
    # whenever a file is uploaded (in fileservice upload)
    # generate a template in openbr
    # write templet to posgres (somehow serialize as a blob)
    i=0

@app.task
def load_gallery():
    # Pull all templates from postgres and return
    # as an array of templates, and an array of corresponding filenames
    i=0