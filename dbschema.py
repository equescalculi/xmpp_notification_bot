"""Define the database schema for addressees and their groups"""
# Licensed under the MIT License, see LICENSE for details

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint


Base = declarative_base()


class Addressee(Base):
    """
    Table of addressee JIDs

    Columns
    -------
    id : Integer
       row id
    jid : String(256)
       JID of the addressee
    """

    __tablename__ = 'addressees'
    id = Column(Integer, primary_key=True)
    jid = Column(String(256), unique=True, nullable=False)


class Group(Base):
    """
    Table of names of addressee groups

    Columns
    -------
    id : Integer
        row id
    name : String(256)
        name of the group
    """

    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False)


class Membership(Base):
    """
    Table of group membership of addressees

    Columns
    -------
    id : Integer
        row id
    addressee_id : Integer, ForeignKey
        foreign key referencing addressees.id
    group_id : Integer, ForeignKey
        foreign key referencing groups.id
    """

    __tablename__ = 'memberships'
    id = Column(Integer, primary_key=True)
    addressee_id = Column(Integer, ForeignKey('addressees.id'))
    addressee = relationship(Addressee)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(Group)
    UniqueConstraint(addressee_id, group_id)
