#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_chore_time
----------------------------------

Tests for `chore_time` module.
"""

import pytest
import tempfile
import os

from chore_time import chore_time, database
from sqlalchemy.orm import sessionmaker


def test_when_init_db_is_called_it_should_create_file_at_given_path():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        filename = f.name
        f.close()
        database.init_db('sqlite:///'+filename)
        assert os.path.isfile(filename)
        os.unlink(filename)


def test_when_init_db_is_called_with_memory_db_it_should_not_error():
    database.init_db('sqlite:///:memory:')


def test_when_init_db_is_called_it_should_return_engine():
    from sqlalchemy.engine import Engine

    assert isinstance(database.init_db('sqlite:///:memory:'), Engine)


def test_create_family_should_be_readable_from_init_db_engine():
    engine = database.init_db('sqlite:///:memory:')
    database.create_family('Fnords')
    session = sessionmaker(bind=engine)()

    family = session.query(database.Family).first()
    expected_familiy = database.Family('Fnords') 
    expected_familiy.id = 1


    assert family == expected_familiy


def test_creating_Family_should_use_provided_name():
    expected_name = 'Fnord'
    family = database.Family(expected_name)

    assert family.name == expected_name


def test_create_family_should_return_created_family():
    family = database.create_family('Fnords')
    
    assert isinstance(family, database.Family)


def test_create_family_member_should_ValueError_if_no_family_has_provided_id():
    with pytest.raises(ValueError):
        database.create_family_member(42, 'My Name', 'fnord@fnord.com')


def test_create_family_member_with_valid_id_should_not_ValueError():
    family = database.create_family('Fnords')

    database.create_family_member(family.id, 'My Name', 'fnord@fnord.com')


def test_create_family_member_should_be_readable_from_init_db_engine():
    engine = database.init_db('sqlite:///:memory:')
    family = database.create_family('Fnords')

    session = sessionmaker(bind=engine)()
    expected_family_member = database.FamilyMember(1, 'My Name', 'fnord@fnord.com') 
    expected_family_member.id = 1

    database.create_family_member(family.id, 'My Name', 'fnord@fnord.com')

    family_member = session.query(database.FamilyMember).first()
    assert family_member == expected_family_member
