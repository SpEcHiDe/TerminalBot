#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Friendly Telegram (telegram userbot)
# Copyright (C) 2018-2019 GitHub/penn5

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import asyncio


async def read_stream(func, stream, delay):
    text = ''
    pattern = re.compile(r'.+\r(?=\w)|\r')

    while not stream._eof:
        await stream._wait_for_data('read_stream')

        try:
            chunk = bytes(stream._buffer).decode()
        except UnicodeDecodeError:
            continue

        stream._buffer.clear()
        text = pattern.sub('', text + chunk)
        await func(text)

        if len(text) > 2048:
            text = text[-2048:]
        if stream._eof:
            break

        await asyncio.sleep(delay)

    if len(stream._buffer) > 0:
        chunk = bytes(stream._buffer).decode()
        stream._buffer.clear()
        text = pattern.sub('', text + chunk)
        await func(text)
