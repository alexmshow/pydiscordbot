import random
import re
from typing import Iterable, Optional

from discord import Colour, Embed, Message, TextChannel, User
from discord.ext import commands
from discord.ext.commands import Cog, Context, group, has_role

class Clean(Cog):
    """
    A cog that allows messages to be deleted in bulk, while applying various filters.
    You can delete messages sent by a specific user, messages sent by bots, all messages, or messages that match a
    specific regular expression.
    The deleted messages are saved and uploaded to the database via an API endpoint, and a URL is returned which can be
    used to view the messages in the Discord dark theme style.
    """

    def __init__(self, bot):
        self.bot = bot
        self.cleaning = False


    async def _clean_messages(
        self,
        amount: int,
        ctx: Context,
        channels: Iterable[TextChannel],
        bots_only: bool = False,
        user: User = None,
        regex: Optional[str] = None,
        until_message: Optional[Message] = None,
    ) -> None:
        """A helper function that does the actual message cleaning."""
        def predicate_bots_only(message: Message) -> bool:
            """Return True if the message was sent by a bot."""
            return message.author.bot

        def predicate_specific_user(message: Message) -> bool:
            """Return True if the message was sent by the user provided in the _clean_messages call."""
            return message.author == user

        def predicate_regex(message: Message) -> bool:
            """Check if the regex provided in _clean_messages matches the message content or any embed attributes."""
            content = [message.content]

            # Add the content for all embed attributes
            for embed in message.embeds:
                content.append(embed.title)
                content.append(embed.description)
                content.append(embed.footer.text)
                content.append(embed.author.name)
                for field in embed.fields:
                    content.append(field.name)
                    content.append(field.value)

            # Get rid of empty attributes and turn it into a string
            content = [attr for attr in content if attr]
            content = "\n".join(content)

            # Now let's see if there's a regex match
            if not content:
                return False
            else:
                return bool(re.search(regex.lower(), content.lower()))

        # Is this an acceptable amount of messages to clean?
        if amount > CleanMessages.message_limit:
            embed = Embed(
                color=Colour(Colours.soft_red),
                title=random.choice(NEGATIVE_REPLIES),
                description=f"Вы не можете удалить больше чем {CleanMessages.message_limit} сообщений."
            )
            await ctx.send(embed=embed)
            return

        # Are we already performing a clean?
        if self.cleaning:
            embed = Embed(
                color=Colour(Colours.soft_red),
                title=random.choice(NEGATIVE_REPLIES),
                description="Подождите, пока завершится текущая операция очистки."
            )
            await ctx.send(embed=embed)
            return

        # Set up the correct predicate
        if bots_only:
            predicate = predicate_bots_only      # Delete messages from bots
        elif user:
            predicate = predicate_specific_user  # Delete messages from specific user
        elif regex:
            predicate = predicate_regex          # Delete messages that match regex
        else:
            predicate = None                     # Delete all messages

        # Default to using the invoking context's channel
        if not channels:
            channels = [ctx.channel]

        # Delete the invocation first
        await ctx.message.delete()

        messages = []
        message_ids = []
        self.cleaning = True

        # Find the IDs of the messages to delete. IDs are needed in order to ignore mod log events.
        for channel in channels:
            async for message in channel.history(limit=amount):

                # If at any point the cancel command is invoked, we should stop.
                if not self.cleaning:
                    return

                # If we are looking for specific message.
                if until_message:

                    # we could use ID's here however in case if the message we are looking for gets deleted,
                    # we won't have a way to figure that out thus checking for datetime should be more reliable
                    if message.created_at < until_message.created_at:
                        # means we have found the message until which we were supposed to be deleting.
                        break

                    # Since we will be using `delete_messages` method of a TextChannel and we need message objects to
                    # use it as well as to send logs we will start appending messages here instead adding them from
                    # purge.
                    messages.append(message)

                # If the message passes predicate, let's save it.
                if predicate is None or predicate(message):
                    message_ids.append(message.id)

        self.cleaning = False

        # Now let's delete the actual messages with purge.
        for channel in channels:
            if until_message:
                for i in range(0, len(messages), 100):
                    # while purge automatically handles the amount of messages
                    # delete_messages only allows for up to 100 messages at once
                    # thus we need to paginate the amount to always be <= 100
                    await channel.delete_messages(messages[i:i + 100])
            else:
                messages += await channel.purge(limit=amount, check=predicate)

        # Reverse the list to restore chronological order
        if messages:
            messages = reversed(messages)
        else:
            # Can't build an embed, nothing to clean!
            embed = Embed(
                color=Colour(Colours.soft_red),
                description="Подходящих сообщений не найдено."
            )
            await ctx.send(embed=embed, delete_after=10)
            return

        # Build the embed and send it
        target_channels = ", ".join(channel.mention for channel in channels)

        message = (
            f"**{len(message_ids)}** сообщений удалено в {target_channels} by "
            f"{ctx.author.mention}\n\n"
        )


    @group(invoke_without_command=True, name="clean", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clean_group(self, ctx: Context) -> None:
        """Commands for cleaning messages in channels."""
        await ctx.send_help(ctx.command)

    @clean_group.command(name="user", aliases=["users"])
    @commands.has_permissions(manage_messages=True)
    async def clean_user(
        self,
        ctx: Context,
        user: User,
        amount: Optional[int] = 10,
        channels: commands.Greedy[TextChannel] = None
    ) -> None:
        """Delete messages posted by the provided user, stop cleaning after traversing `amount` messages."""
        await self._clean_messages(amount, ctx, user=user, channels=channels)

    @clean_group.command(name="all", aliases=["everything"])
    @commands.has_permissions(manage_messages=True)
    async def clean_all(
        self,
        ctx: Context,
        amount: Optional[int] = 10,
        channels: commands.Greedy[TextChannel] = None
    ) -> None:
        """Delete all messages, regardless of poster, stop cleaning after traversing `amount` messages."""
        await self._clean_messages(amount, ctx, channels=channels)

    @clean_group.command(name="bots", aliases=["bot"])
    @commands.has_permissions(manage_messages=True)
    async def clean_bots(
        self,
        ctx: Context,
        amount: Optional[int] = 10,
        channels: commands.Greedy[TextChannel] = None
    ) -> None:
        """Delete all messages posted by a bot, stop cleaning after traversing `amount` messages."""
        await self._clean_messages(amount, ctx, bots_only=True, channels=channels)

    @clean_group.command(name="regex", aliases=["word", "expression"])
    @commands.has_permissions(manage_messages=True)
    async def clean_regex(
        self,
        ctx: Context,
        regex: str,
        amount: Optional[int] = 10,
        channels: commands.Greedy[TextChannel] = None
    ) -> None:
        """Delete all messages that match a certain regex, stop cleaning after traversing `amount` messages."""
        await self._clean_messages(amount, ctx, regex=regex, channels=channels)

    @clean_group.command(name="message", aliases=["messages"])
    @commands.has_permissions(manage_messages=True)
    async def clean_message(self, ctx: Context, message: Message) -> None:
        """Delete all messages until certain message, stop cleaning after hitting the `message`."""
        await self._clean_messages(
            CleanMessages.message_limit,
            ctx,
            channels=[message.channel],
            until_message=message
        )

    @clean_group.command(name="stop", aliases=["cancel", "abort"])
    @commands.has_permissions(manage_messages=True)
    async def clean_cancel(self, ctx: Context) -> None:
        """If there is an ongoing cleaning process, attempt to immediately cancel it."""
        self.cleaning = False

        embed = Embed(
            color=Colour.blurple(),
            description="Прервать удаление."
        )
        await ctx.send(embed=embed, delete_after=10)


def setup(bot) -> None:
    """Load the Clean cog."""
    bot.add_cog(Clean(bot))