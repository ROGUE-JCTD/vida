# This is a simple test to check the br_get_filename issue.  Does it
# seg fault?
from brpy import init_brpy
import os

br = init_brpy()
br.br_initialize_default()
br.br_set_property('algorithm', 'FaceRecognition')
br.br_set_property('enrollAll', 'True')

imgfilename = 'testimage1.jpg'
print "Reading file " + imgfilename
imgbuffer = open('testimage1.jpg', 'rb').read()
print "Creating template with br_load_img"
template = br.br_load_img(imgbuffer, len(imgbuffer))
print "Setting file name on template to " + os.path.basename(imgfilename)
br.br_set_filename(template, os.path.basename(imgfilename))
print "Retrieving file name from template"
filename = br.br_get_filename(template)
print filename
print "Done!"