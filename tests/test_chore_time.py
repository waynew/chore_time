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
    database.create_family('Fnords', 'fnord email')
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind=engine)()

    family = session.query(database.Family).first()

    assert family == database.Family('Fnords', 'fnord email')


