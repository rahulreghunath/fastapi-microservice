"""_summary_

Returns:
    _type_: _description_
"""
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    """_summary_"""

    @classmethod
    def bcrypt(cls, password: str):
        """_summary_

        Args:
            password (str): _description_

        Returns:
            _type_: _description_
        """
        return pwd_cxt.hash(password)

    @classmethod
    def verify(cls, hashed_password: str, plane_password: str):
        """_summary_

        Args:
            hashed_password (str): _description_
            plane_password (str): _description_

        Returns:
            _type_: _description_
        """
        return pwd_cxt.verify(plane_password, hashed_password)
