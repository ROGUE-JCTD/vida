import os
from vida import br
from vida.fileservice.helpers import get_fileservice_files_abs, get_gallery_file
import logging
logger = logging.getLogger(__name__)

def index_face(image):
    # NOTE: This commented out code appears to do the exact same as br_enroll
    # gal = br.br_make_gallery(get_gallery_file()+'[append=true]')
    # imgbuffer = open(image, 'rb').read()
    # template = br.br_load_img(imgbuffer, len(imgbuffer))
    # tlist = br.br_enroll_template(template)
    # num = br.br_num_templates(tlist)
    # # br.br_add_template_list_to_gallery(gal, tlist)
    # NOTE: This commented out code is the same as br_add_template_list_to_gallery
    # for x in range(0, num):
    #     t = br.br_get_template(tlist, x)
    #     br.br_set_filename(t, image)
    #     #fn = br.br_get_filename(t)
    #     br.br_add_template_to_gallery(gal, t)
    #
    # br.br_free_template(template)
    # br.br_free_template_list(tlist)
    # br.br_close_gallery(gal)
    br.br_enroll(image, get_gallery_file()+'[append=true]')


# reset the OpenBR Gallery
def reindex_gallery():
    logger.debug("Reindexing entire gallery to " + get_gallery_file())
    if os.path.isfile(get_gallery_file()):
        os.remove(get_gallery_file())

    allfiles = get_fileservice_files_abs()
    logger.debug(allfiles)
    br.br_enroll_n(len(allfiles), allfiles, get_gallery_file())