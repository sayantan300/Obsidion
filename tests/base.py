import logging
import unittest
from contextlib import contextmanager
from typing import Dict

import discord
from discord.ext import commands

from tests import helpers


class CommandTestCase(unittest.IsolatedAsyncioTestCase):
    """TestCase with additional assertions that are useful for testing Discord commands."""

    async def assertHasPermissionsCheck(  # noqa: N802
        self, cmd: commands.Command, permissions: Dict[str, bool],
    ) -> None:
        """
        Test that `cmd` raises a `MissingPermissions` exception if author lacks `permissions`.
        Every permission in `permissions` is expected to be reported as missing. In other words, do
        not include permissions which should not raise an exception along with those which should.
        """
        # Invert permission values because it's more intuitive to pass to this assertion the same
        # permissions as those given to the check decorator.
        permissions = {k: not v for k, v in permissions.items()}

        ctx = helpers.MockContext()
        ctx.channel.permissions_for.return_value = discord.Permissions(**permissions)

        with self.assertRaises(commands.MissingPermissions) as cm:
            await cmd.can_run(ctx)
