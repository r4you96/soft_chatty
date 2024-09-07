import asyncio
import sys


async def read_input():
    loop = asyncio.get_event_loop()
    input_line = await loop.run_in_executor(None, sys.stdin.readline)
    return input_line.strip()
