import asyncio

from app.utils.miscs import is_sync_function


class BackgroundTasksManager:
    def __init__(self, limit: int = 5):
        self.limit = limit
        self.tasks = set()
        self.semaphore = asyncio.Semaphore(limit)
        self.loop = asyncio.get_event_loop()

    async def _run_with_semaphore(self, coro):
        async with self.semaphore:
            task = asyncio.create_task(coro)
            self.tasks.add(task)
            try:
                await task
            except asyncio.CancelledError:
                pass
            finally:
                self.tasks.remove(task)

    def create(self, func_or_coroutinefunc, *sync_function_args, **sync_function_kwargs):
        if is_sync_function(func_or_coroutinefunc):
            fut = self.loop.run_in_executor(None, func_or_coroutinefunc, *sync_function_args, **sync_function_kwargs)
            return fut
        future = self.loop.create_task(self._run_with_semaphore(func_or_coroutinefunc))
        return future

    async def wait_for_all(self):
        if self.tasks:
            await asyncio.wait(self.tasks)
