import urllib2

base_url = "http://canchallena.lanacion.com.ar/_ui/desktop/imgs/escudos/{0}.png"
escudos_ids = [1295, 2, 3, 895, 4, 671, 5, 6, 7, 132, 10, 12, 13, 863, 16, 862, 19, 136, 897, 20]
escudos_ids = [72]

for escudo_id in escudos_ids:
    for tipo in range(1, 5):
        escudo_nombre = str(escudo_id) + "_" + str(tipo)
        escudo = urllib2.urlopen(base_url.format(escudo_nombre))
        escudo_file = open("escudo_{0}.png".format(escudo_nombre), "wb")
        escudo_file.write(escudo.read())
        escudo_file.close()
