# -*- coding: utf-8 -*-

"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT License.
"""

import base64

from datetime import timedelta
from typing import Any, Dict, Union


class ActorReminderData:
    """The class that holds actor reminder data.

    Attrtibutes:
        name: the name of Actor reminder.
        state: the state data data passed to receive_reminder callback.
        due_time: the amount of time to delay before invoking the reminder
            for the first time.
        period: the time interval between reminder invocations after
            the first invocation.
    """

    def __init__(
            self, name: str, state: Union[bytes, str],
            due_time: timedelta, period: timedelta):
        """Creates new :class:`ActorReminderData` instance.

        Args:
            name (str): the name of Actor reminder.
            state (bytes, str): the state data passed to
                receive_reminder callback.
            due_time (datetime.timedelta): the amount of time to delay before
                invoking the reminder for the first time.
            period (datetime.timedelta): the time interval between reminder
                invocations after the first invocation.
        """
        self._name = name
        self._due_time = due_time
        self._period = period

        if not isinstance(state, (str, bytes)):
            raise ValueError(f'only str and bytes are allowed for state: {type(state)}')

        if isinstance(state, str):
            self._state = state.encode('utf-8')
        else:
            self._state = state

    @property
    def name(self) -> str:
        """Gets the name of Actor Reminder."""
        return self._name

    @property
    def state(self) -> bytes:
        """Gets the state data of Actor Reminder."""
        return self._state

    @property
    def due_time(self) -> timedelta:
        """Gets due_time of Actor Reminder."""
        return self._due_time

    @property
    def period(self) -> timedelta:
        """Gets period of Actor Reminder."""
        return self._period

    def as_dict(self) -> Dict[str, Any]:
        """Gets :class:`ActorReminderData` as a dict object."""
        encoded_state = None
        if self._state is not None:
            encoded_state = base64.b64encode(self._state)
        return {
            'name': self._name,
            'dueTime': self._due_time,
            'period': self._due_time,
            'data': encoded_state.decode("utf-8"),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> 'ActorReminderData':
        """Creates :class:`ActorReminderData` object from dict object."""
        b64encoded_state = obj.get('data')
        state_bytes = None
        if b64encoded_state is not None and len(b64encoded_state) > 0:
            state_bytes = base64.b64decode(b64encoded_state)
        return ActorReminderData(obj['name'], state_bytes, obj['dueTime'], obj['period'])
