class Usuario():
    def __init__(self, row):
        # Asumimos que el SELECT * trae:
        # (id, email, password_hash, negocio_id)
        self._id = row[0]
        self._email = row[1]
        self._password_hash = row[2]
        self._negocio_id = row[3]
    
    def to_json(self):
        # ¡Importante! NUNCA devolvemos el hash en un JSON
        return {
            "id": self._id,
            "email": self._email,
            "negocio_id": self._negocio_id
        }