#!/usr/bin/python3.7

import os

from discord.ext import commands

from utilities import logger
from utilities import texts
from utilities import lists
from utilities.game_animator import GameAnimator
from utilities.config import Config

prefix = '!'

logger.init()

client = commands.AutoShardedBot(command_prefix=prefix)

logger.info('Starting Groovy ...')

config = Config().get_config()


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user} ...')
    await init()
    GameAnimator(client, client.loop).run()


@client.event
async def on_message(msg):
    if msg.author.bot:
        return

    if not msg.guild.get_member(client.user.id) in msg.mentions and not msg.content.startswith(prefix):
        return

    if len(msg.content.split(' ')) == 1 and msg.content.startswith(f'<@{client.user.id}>'):
        await msg.channel.send(texts.mention_text)

    async def run_command(command):
        if command not in lists.cogs:
            return

        logger.info(
            f'{msg.content} » {msg.author.name}#{msg.author.discriminator}'
            f' in #{msg.channel.name} on {msg.guild.name} ({msg.guild.id})'
        )
        await client.process_commands(msg)

    if msg.content.startswith(f'<@{client.user.id}>') and len(msg.content.split(' ')) > 1:
        invoke = msg.content.split(' ').pop(1)
        pre = msg.content.split(' ')
        for x in range(0, 2):
            del pre[0]

        content = ' '.join(pre)

        if invoke in lists.cogs:
            await run_command(invoke)

    if msg.content.startswith(prefix):
        invoke = msg.content[1:]

        if invoke in lists.cogs:
            await run_command(invoke)


async def init():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'cogs/')
    extensions = os.listdir(filename)

    logger.info('Started loading cogs ...')

    for file in extensions:
        if file.startswith('__'):
            logger.warn(f'There is a file or dir in /cogs/ which is no cog: {file}')
        else:
            cog = file.split('.')[0]
            client.load_extension(f'cogs.{cog}')
            logger.info(f'Successfully loaded cog {cog}!')


logger.info('Logging in ...')
client.run(config['test_bot']['token'])