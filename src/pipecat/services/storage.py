#
# Copyright (c) 2024, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import asyncio
import time

# from dataclasses import dataclass
from abc import abstractmethod

from typing import Awaitable, Callable, List

from pipecat.processors.aggregators.openai_llm_context import (
    OpenAILLMContextFrame
)

from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.frames.frames import Frame


class SesameClient:
    # @abstractmethod
    async def save_message(self, message: str, role: str, filename: str):
        # print(f"_____--_____--_____storage.py * SesameClient save_message! {role}: {message}")
        await self.local_save_message(message, role, filename)
        # pass

    async def local_save_message(self, message: str, role: str, filename: str):
        with open(filename, 'a') as file:
            if type(message) is list:
                file.write(f"{role}: ")
                for line in message:
                    file.write(f"{line['text']} ")
            else:
                file.write(f"{role}: {message}")
            file.write('\n')

class SesameDBClient(SesameClient):
    def __init__(self, db_credentials):
        pass

    async def save_message(self, message: str, role: str):
        # Save to DB
        pass

class SesameStorage(FrameProcessor):
    def __init__(self, client: SesameClient):
        super().__init__()
        self._client = client
        self._save_filename = "SesameStorage-" + str(int(time.time())) + ".txt"

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        if isinstance(frame, OpenAILLMContextFrame):
            messages = frame.context.messages
            user_message = messages[-2]
            assistant_message = messages[-1]
            await self._client.save_message(user_message["content"], user_message["role"], self._save_filename)
            await self._client.save_message(assistant_message["content"], assistant_message["role"], self._save_filename)
