from Clases import *




medico = Profesional("email@gmail",123,"pancho",20,1)
especialidad = Especialidad(1,"podologo","mira los pies")
cirujano = Especialidad(1,"podologo","mira los pies")
medico.setEspecialidades(especialidad)
medico.configurar_dia_horario("martes","08:30 - 20:30")
paciente = Paciente(1,"rmairo","cabri",230,"cabri@algo","OSDE platinum")

print(paciente.solicitar_turno(1,medico,"martes",(12,30),cirujano))
print(medico.getTurno())

