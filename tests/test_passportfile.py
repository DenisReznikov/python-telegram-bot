#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2021
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

import pytest

from telegram import PassportFile, PassportElementError, Bot, File
from tests.conftest import check_shortcut_signature, check_shortcut_call, check_defaults_handling


@pytest.fixture(scope='class')
def passport_file(bot):
    return PassportFile(
        file_id=TestPassportFile.file_id,
        file_unique_id=TestPassportFile.file_unique_id,
        file_size=TestPassportFile.file_size,
        file_date=TestPassportFile.file_date,
        bot=bot,
    )


class TestPassportFile:
    file_id = 'data'
    file_unique_id = 'adc3145fd2e84d95b64d68eaa22aa33e'
    file_size = 50
    file_date = 1532879128

    def test_expected_values(self, passport_file):
        assert passport_file.file_id == self.file_id
        assert passport_file.file_unique_id == self.file_unique_id
        assert passport_file.file_size == self.file_size
        assert passport_file.file_date == self.file_date

    def test_to_dict(self, passport_file):
        passport_file_dict = passport_file.to_dict()

        assert isinstance(passport_file_dict, dict)
        assert passport_file_dict['file_id'] == passport_file.file_id
        assert passport_file_dict['file_unique_id'] == passport_file.file_unique_id
        assert passport_file_dict['file_size'] == passport_file.file_size
        assert passport_file_dict['file_date'] == passport_file.file_date

    def test_get_file_instance_method(self, monkeypatch, passport_file):
        def make_assertion(*_, **kwargs):
            result = kwargs['file_id'] == passport_file.file_id
            # we need to be a bit hacky here, b/c PF.get_file needs Bot.get_file to return a File
            return File(file_id=result, file_unique_id=result)

        assert check_shortcut_signature(PassportFile.get_file, Bot.get_file, ['file_id'], [])
        assert check_shortcut_call(passport_file.get_file, passport_file.bot, 'get_file')
        assert check_defaults_handling(passport_file.get_file, passport_file.bot)

        monkeypatch.setattr(passport_file.bot, 'get_file', make_assertion)
        assert passport_file.get_file().file_id == 'True'

    def test_equality(self):
        a = PassportFile(self.file_id, self.file_unique_id, self.file_size, self.file_date)
        b = PassportFile('', self.file_unique_id, self.file_size, self.file_date)
        c = PassportFile(self.file_id, self.file_unique_id, '', '')
        d = PassportFile('', '', self.file_size, self.file_date)
        e = PassportElementError('source', 'type', 'message')

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)