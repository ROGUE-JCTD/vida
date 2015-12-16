from brpy import init_brpy

br = init_brpy()
br.br_initialize_default()
br.br_set_property('algorithm', 'FaceRecognition')
br.br_set_property('enrollAll', 'true')
