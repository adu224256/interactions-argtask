from interactions import Task as baseTask
from interactions import BaseTrigger
from datetime import datetime
from typing import Callable
import inspect
import asyncio


class Task(baseTask):
    def __init__(self, callback: Callable, trigger: BaseTrigger) -> None:
        super().__init__(callback, trigger)

    async def __call__(self, *args, **kwargs) -> None:
        try:
            if inspect.iscoroutinefunction(self.callback):
                val = await self.callback(*args, **kwargs)
            else:
                val = self.callback(*args, **kwargs)

            if isinstance(val, BaseTrigger):
                self.reschedule(val)
        except Exception as e:
            self.on_error(e)

    def _fire(self, fire_time: datetime, *args, **kwargs) -> None:
        """Called when the task is being fired."""
        self.trigger.set_last_call_time(fire_time)
        _ = asyncio.create_task(self(*args, **kwargs))
        self.iteration += 1

    async def _task_loop(self, *args, **kwargs) -> None:
        """The main task loop to fire the task at the specified time based on triggers configured."""
        while not self._stop.is_set():
            fire_time = self.trigger.next_fire()
            if fire_time is None:
                return self.stop()

            future = asyncio.create_task(self._stop.wait())
            timeout = (fire_time - datetime.now()).total_seconds()
            done, _ = await asyncio.wait([future], timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
            if future in done:
                return None

            self._fire(fire_time, *args, **kwargs)

    def start(self, *args, **kwargs) -> None:
        """Start this task."""
        try:
            self.trigger.reschedule()
            self._stop.clear()
            self.task = asyncio.create_task(self._task_loop(*args, **kwargs))
        except RuntimeError:
            get_logger().error(
                "Unable to start task without a running event loop! We recommend starting tasks within an `on_startup` event."
            )

    def stop(self) -> None:
        """End this task."""
        self._stop.set()
        if self.task:
            self.task.cancel()

    def restart(self, *args, **kwargs) -> None:
        """Restart this task."""
        self.stop()
        self.start(*args, **kwargs)

    def reschedule(self, trigger: BaseTrigger) -> None:
        """
        Change the trigger being used by this task.

        Args:
            trigger: The new Trigger to use

        """
        self.trigger = trigger
        self.restart(*args, **kwargs)
