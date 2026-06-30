from sqlalchemy import Column, ForeignKey, Integer, String

from base import Base


class Department(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    name = Column(String(200))