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

import asyncio


async def read_stream(func, stream, delay):
    last_task = None
    data = b""
    while True:
        dat = (await stream.read(1))
        if not dat:
            # EOF
            if last_task:
                # Send all pending data
                last_task.cancel()
                await func(data.decode("UTF-8"))
                # If there is no last task there is inherently no data, so theres no point sending a blank string
            break
        data += dat
        if last_task:
            last_task.cancel()
        last_task = asyncio.ensure_future(sleep_for_task(func, data, delay))


async def sleep_for_task(func, data, delay):
    await asyncio.sleep(delay)
    await func(data.decode("utf-8"))
