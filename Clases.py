from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass




"""
el id en todas las clases deberia ser como opcional aqui en la creacion, luego con la bd se generara un idea al caso,
se deben inicializar como none.

"""

class Usuario:
    def __init__(self,  email: str, password: str, id=None):
        self.id = id
        self._email = self._validar_email(email)
        self._password=self._validar_password(password)

    def __repr__(self):
        return f"Usuario(id={self.id}, email='{self._email}')"

    # funciones para validar mail y password, se deberian mejorar

    def _validar_email(self, email: str) -> str:
        if not isinstance(email, str):
            raise ValueError("El email debe ser una cadena")
        email = email.strip()
        if not email:
            raise ValueError("El email no puede estar vacío.")
        # Aquí se podría añadir una validación de formato más robusta (regex)
        return email


    def _validar_password(self, password: str) -> str:
        """Valida que el password no esté vacío y tenga una longitud mínima. Se me ocurrio 6 caracteres
        minimo, pero a reveer
        """

        if not password or len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        return password

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, nuevo_email: str):

        self._email = self._validar_email(nuevo_email)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, nueva_password: str):

        self._password = self._validar_password(nueva_password)

# esta clase se creo probando @dataclass
@dataclass
class Especialidad:
    id: int
    _nombre: str = ""
    descripcion: str = ""

    @property
    def nombre(self:str)-> str:
        return self._nombre



#Clase Profesional
# hereda de usuario password y email.
class Profesional(Usuario):
    def __init__(self, email: str, password : str, nombre: str, matricula: int, id=None):
        super().__init__(email, password, id)
        #hereda id de usuario

        self._nombre= self._validador_nombre(nombre)
        self._matricula = self._validador_matricula(matricula)

        #las especialidades se crean desde la clase
        self.especialidades = []
        #los turnos vienen por otro lado
        self._turnos = []

        self._horarios: Dict[str, Optional[Tuple[int, int, int, int]]] = {
            "lunes": None,
            "martes": None,
            "miercoles": None,
            "jueves": None,
            "viernes": None,
            "sabado": None,
        }



    def __repr__(self):
        return (f"Medico(id={self.id}, nombre='{self._nombre}', matricula='{self._matricula}, horarios disponibles"
                f"={self.horarios}', especialidades = {self.especialidades})")


    @property
    def matricula(self):
        return self._matricula

    @property
    def espacialidades(self):
        return  self.especialidades

    @property
    def turnos(self):
        return self._turnos
    @property
    def nombre(self):
        return  self._nombre

    @property
    def horarios(self):
        return  self._horarios


    @nombre.setter
    def nombre(self,nombre: str):
        self._nombre  = self._validador_nombre(nombre)

    @matricula.setter
    def matricula(self, matricula: int):
        self._matricula = self._validador_matricula(matricula)




    # Validador nombre y matricula

    def _validador_nombre(self,nombre: str) -> str:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del profesional no puede estar vacío.")
        return nombre

    def _validador_matricula(self,matricula: int) -> int:

       if not isinstance(matricula,int):
           raise ValueError("La matricula debe ser un numero entero mayor a 0")



       if matricula <= 0:
            raise ValueError("La matricula debe ser un numero mayor a  0.")
       return matricula


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
    """
    No creo que el paciente deba heredar de la clase usuario.
    No deberia tener password.

    """
    def __init__(self,id,nombre,apellido,celular,email,obra_social,):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.email = email
        self.obra_social = obra_social
        self.turno = []

    # getter

    def getId(self):
        return self.id
    def getNombre(self):
        return self.nombre
    def getApellido(self):
        return self.apellido
    def getCelular(self):
        return self.celular
    def getemail(self):
        return self.celular
    def getEmail(self):
        return self.celular
    def getObra_social(self):
        return self.obra_social
    def getTurno(self):
        return self.turno

    def __repr__(self):
        return (f"Nombre y apellido del paciente: {self.nombre}-{self.apellido}, "
                f"celular: {self.celular}, email: {self.celular}, email: {self.email},"
                f"obra social: {self.obra_social}, turnos asignado {self.turno} ")

    def setTurno(self,turno):
        self.turno.append(turno)

    """
    la idea seria crear una funcion que cree un objeto turno, lo asigne al listados de turnos del medico
    e ingrese al listado de turnos del paciente.
    La clase turno esta creada y tiene funciones y validaciones que ayudan en este punto.
    """

    def solicitar_turno(self,id, profesional: Profesional, dia_str: str, hora_int_tupla: tuple[int, int],
                        especialidad_requerida: Especialidad):
        """
        Crea, valida y registra un nuevo turno, asegurando que el paciente
        no tenga ya un turno asignado para la misma fecha y hora.
        """



        dia_a_chequear = dia_str.lower()

        # Recorrer el historial para ver si ya hay un turno para ese día y hora. La clave estara
        # ( y sera importante que el profesional lo haga ) en si el turno esta True o False.
        for turno_existente in self.getTurno():


            if (turno_existente.dia_turno == dia_a_chequear and
                    turno_existente.hora_turno == hora_int_tupla and
                    turno_existente.activo is True):

                raise ValueError(
                    f"Ya tienes un turno asignado el {dia_str} a las {hora_int_tupla[0]:02d}:{hora_int_tupla[1]:02d}.")


        nuevo_turno = Turno(id=None, paciente=self, profesional=profesional)


        mensaje = nuevo_turno.setTurno(dia_str, hora_int_tupla, especialidad_requerida)

        self.setTurno(nuevo_turno)

        return nuevo_turno, mensaje

    def cancelarTurbo(self, id):

        for i in self.getTurno():
            print(i)


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
        errores = []
        dia =dia.lower()
        horas, minutos = horario

        # Aca se evalua la especialidad
        if especialidad not in self.profesional.especialidades:
            errores.append(f"El profesional no brinda la especialidad '{especialidad.nombre}'.")

        horario_profesional = self.profesional.horarios.get(dia)

        # Aca evaluo si el dia tiene el horario asignado
        if not horario_profesional or horario_profesional is None:
            errores.append(f"El profesional no tiene horarios configurados para el día '{dia}'.")
        else:


            # Aca chequeamos la hora
            hora_inicio, minuto_inicio, hora_fin, minuto_fin = horario_profesional

            # 3. Validación de Rango Horario

            minutos_turno = horas * 60 + minutos
            minutos_inicio_disp = hora_inicio * 60 + minuto_inicio
            minutos_fin_disp = hora_fin * 60 + minuto_fin

            if not (minutos_inicio_disp <= minutos_turno and minutos_turno < minutos_fin_disp):
                hora_inicio_str = f"{hora_inicio:02d}:{minuto_inicio:02d}"
                hora_fin_str = f"{hora_fin:02d}:{minuto_fin:02d}"

                errores.append(
                    f"Hora de turno ({dia} a las {horas:02d}:{minutos:02d}) fuera de la disponibilidad ({hora_inicio_str} - {hora_fin_str}).")


            self.dia_turno = dia
            self.hora_turno = horario

            self.profesional.turnos.append(self)
            return f"Turno asignado con éxito: {dia} a las {horas:02d}:{minutos:02d}."

        if errores:
           # Si tenemos errores aca la lista creada los presenta.
            raise ValueError("\n".join(errores))









