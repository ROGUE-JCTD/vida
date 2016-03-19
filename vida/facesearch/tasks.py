from vida.celery import app
import brpy2
import logging
import fileservice.helpers
import sys
logger = logging.getLogger(__name__)


@app.task
def index_face(image):
    logger.debug("Calling index_face on " + image)


# Re-index all of the files, need to do this on startup since we are maintaining the gallery in memory now
@app.task
def reindex_files():
    # TODO: I am not absolutely sold that the __init.py__ code runs only once, so we'll do some checking to save time
    # If the gallery has not been populated, or if the gallery has fewer files than in the folder we need to re-index
    logger.debug("Gallery is empty, Reindexing all pictures")
    result = []
    try:
        brpy2.initialize()
        brpy2.setAlgorithm("Read(Grayscale)+Cascade")
        brpy2.setGlobal("enrollAll", "true")
        file_names = fileservice.helpers.get_fileservice_files()
        logger.debug(file_names)
        for currFile in file_names:
            logger.debug("Indexing:" + currFile)
            result.append(brpy2.Template(currFile))

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    return result
