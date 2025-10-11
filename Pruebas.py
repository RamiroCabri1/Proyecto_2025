from Clases import *

medico = Profesional("email@gmail",123,"pancho",20,1)
pediatria = Especialidad(20,"pediatria","atender a nenes")
podologia = Especialidad(20,"podologo","atender los pies")
nutricion = Especialidad(20,"podologo","atender los pies")
medico.setEspecialidades(pediatria)
paciente = Paciente
medico.setEspecialidades(podologia)
print(medico.getEspacialidades())
medico.configurar_dia_horario("lunes","08:30 - 20:30")
print(medico.getHorarios())
turno = Turno(20,paciente,medico)
print(turno.setTurno("lunes",(15,35),nutricion))
print(medico.getTurno())