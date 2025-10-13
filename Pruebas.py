from Clases import Profesional, Especialidad

medico = Profesional("1020","cabriramiro","ramiro",10)

medico.password = "@gmail.com"
email = medico.password

print(email)

especialidad = Especialidad(1,"podologo","mira las patas")
a_ver = especialidad.nombre
print(a_ver)

