from dataclasses import dataclass

from pywin32_testutil import non_admin_error_codes


class Usuario:
    def __init__(self,  email, password, id=None):
        self.id = id
        self.email = email
        self.password=password

    def __repr__(self):
        return f"Usuario(id={self.id}, email='{self.email}')"

    """
    faltan metodos que no se como crearlos
    reemplazar por decoradores
    faltan validadores
    """
   # setter

    """
    agregar validadores
    
    """

    def setModificar_email(self, email):
        self.email = email
    def setModificar_password(self, password):
        self.password = password


    # getter

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

@dataclass
class Especialidad:
    id: int
    nombre: str
    descripcion: str = ""


#Clase Profesional
# hereda de usuario password y email.
class Profesional(Usuario):
    def __init__(self, email, password, nombre, matricula, id=None):
        super().__init__(email, password, id)
        #hereda id de usuario
        self.nombre=nombre
        self.matricula = matricula
        #las especialidades se crean desde la clase
        self.especialidades = []
        #los turnos vienen por otro lado
        self.turnos = []
        self.horarios =  {
           "lunes": None,
            "martes":None,
            "miercoles":None,
            "jueves": None,
            "viernes": None,
            "sabado":None,
        }



    def __repr__(self):
        return (f"Medico(id={self.id}, nombre='{self.nombre}', matricula='{self.matricula}, horarios disponibles"
                f"={self.horarios}', especialidades = {self.especialidades})")

    """
    reemplazar por decoradores,
    faltan validadores
    
    """

    def getMatricula(self):
        return self.matricula

    def getEspacialidades(self):
        return  self.especialidades

    def getTurno(self):
        return self.turnos

    def getNombre(self):
        return  self.nombre

    def getHorarios(self):
        return  self.horarios



    def setMatricula(self,matricula):
        self.matricula = matricula

    def setNombre(self,nombre):
        self.nombre = nombre

    def setEspecialidades(self, especialidad):

        if isinstance(especialidad, Especialidad):


            if especialidad not in self.especialidades:
                self.especialidades.append(especialidad)
            else:
                raise ValueError(f"La especialidad '{especialidad.nombre}' ya se encuentra en el sistema.")


        else:
            raise TypeError(f"'{especialidad}' debe ser un objeto de la clase Especialidad.")



    def _validar_y_convertir_hora(self, hora_str):
        """La idea es que manejar los horarios como int, para que luego el uso de la clase
        turno sea de facil implementacion. El horairo de atencion debe tener un formato 09:00 - 21:00 (ejemplo)
        La funcion validar y convertir tomara un str y lo convierte a ese formato. Tambien realiza validaciones.
        """
        try:
            hora = hora_str.split(" - ")
            if len(hora) != 2:
                raise ValueError("El formato debe ser 'HH:MM - HH:MM'")
            else:
                hora_inicio, hora_fin = hora

            hora_inicio , minuto_inicio = map(int,hora_inicio.split(":"))
            #crea un tupla de int dividiendo hora inicio y minuto inicio, para luego validar las mismas.
            hora_fin, minuto_fin = map(int, hora_fin.split(":"))

            if not (0 <= hora_inicio < 24 and 0 <= hora_fin < 24 and 0 <= minuto_inicio < 60 and 0 <= minuto_fin < 60):
                raise ValueError("Horas o minutos fuera de rango (00:00 - 23:59)")

            total_min_inicio = hora_inicio * 60 + minuto_inicio
            total_min_fin = hora_fin * 60 + minuto_fin

            if total_min_inicio >= total_min_fin:
                raise ValueError("La hora de inicio debe ser anterior a la hora de fin.")

            # Devuelve una tupla de 4 enteros para usar en la clase Turnos
            return (hora_inicio, minuto_inicio, hora_fin, minuto_fin)
        except ValueError as e:
            # Lanza un error genérico con el detalle de la validación fallida
            raise ValueError(f"Error de formato o lógica en la hora: {e}")


    def configurar_dia_horario(self,dia,horario):

        if dia.lower() not in self.horarios:
            raise ValueError(f"El día '{dia}' no existe. Días válidos: {list(self.horarios.keys())}")

        horas_en_entero = self._validar_y_convertir_hora(horario)
        self.horarios[dia] = horas_en_entero

        return self.horarios
    def setTurno(self,turno):
        #el turno se genera en la clase turno, no tenia sentido validar si es una clase turno o no
        self.turno = turno

class Paciente:
    pass

from typing import Optional, Tuple
from datetime import datetime
class Turno:
    def __init__(self, id, paciente: Paciente, profesional: Profesional, activo: bool = True):
        self.id = id
        self.paciente = Paciente
        self.profesional = profesional
        self.dia_turno: Optional[str] = None
        self.hora_turno: Optional[Tuple[int, int]] = None
        self.activo = activo
        self.fecha_creacion = datetime.now()

    def __repr__(self):
        estado = f"{self.dia_turno} a las {self.hora_turno[0]:02d}:{self.hora_turno[1]:02d}" if self.dia_turno else "PENDIENTE DE ASIGNACIÓN"
        # chequear nombre del paciente
        return f"Turno(id={self.id},paciente = {self.paciente} profesional='{self.profesional.nombre}', estado='{estado}')"

    def getID(self):
        return self.id

    def getPaciente(self):
        return self.paciente

    def getProfecional(self):
        return self.profesional

    def getDiaTurno(self):
        return self.dia_turno

    def getHoraTurno(self):
        return self.hora_turno

    def setTurno(self,dia,horario: Tuple[int, int],especialidad:Especialidad):

        dia =dia.lower()
        horas, minutos = horario

        if especialidad not in self.profesional.especialidades:
            raise ValueError(f"El profecional no brinda esa especialidad")

        horario_profesional = self.profesional.horarios.get(dia)

        if not horario_profesional or horario_profesional is None:
            raise ValueError(f"El profesional no tiene horarios configurados para el día '{dia}'.")

        hora_inicio, minuto_inicio, hora_fin, minuto_fin = horario_profesional

        # 3. Validación de Rango Horario
        minutos_turno = horas * 60 + minutos
        minutos_inicio_disp = hora_inicio * 60 + minuto_inicio
        minutos_fin_disp = hora_fin * 60 + minuto_fin

        if not (minutos_inicio_disp <= minutos_turno and minutos_turno < minutos_fin_disp):
            hora_inicio_str = f"{hora_inicio:02d}:{minuto_inicio:02d}"
            hora_fin_str = f"{hora_fin:02d}:{minuto_fin:02d}"

            raise ValueError(
                f"Hora de turno ({dia} a las {horas:02d}:{minutos:02d}) fuera de la disponibilidad ({hora_inicio_str} - {hora_fin_str}).")


        self.dia_turno = dia
        self.hora_turno = horario

        self.profesional.turnos.append(self)
        return f"Turno asignado con éxito: {dia} a las {horas:02d}:{minutos:02d}."