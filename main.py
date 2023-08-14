# CSharpener is a discord bot that you can send your c script to be compiled.
import discord, os, subprocess

help_msg = """
```
############################################################
#                       CSharpener                         #
#                  ~ Made by JohnTheReaver                 #
############################################################
#                       Description:                       #
# This program is used to compile C scripts using discord. #
############################################################
# !compile Attach C script, it responds with compiled file #    
# !version See the version of this program.                #
# !help Get this help menu.                                #
############################################################
```
"""
intents = discord.Intents.default()
client = discord.Client(intents=intents)

print("Bot has started running...")

@client.event
async def on_message(message):
    if message.content.startswith('!compile'):
        if len(message.attachments) == 0:
            await message.channel.send("Please attach your .c script.")
            return

        for attachment in message.attachments:
            filename = attachment.filename
            if os.path.exists(filename):
                os.remove(filename)
            await attachment.save(filename)
            if ".c" in filename:
                outputfile = filename.replace(".c", '')
                subprocess.call(f"gcc -o {outputfile} {filename}", shell=True)
                with open(f"{outputfile}", "rb") as f:
                    compiled_file = discord.File(f, filename=f"{outputfile}")
                    await message.channel.send(file=compiled_file)
                os.remove(filename)
                os.remove(outputfile)
            else:
                await message.channel.send("Sorry, filename must end with .c")

    elif message.content.startswith('!help'):
        await message.channel.send(help_msg)

    elif message.content.startswith('!version'):
        await message.channel.send("Version: 1.0")

client.run('YOUR_DISCORD_TOKEN')
