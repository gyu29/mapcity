import discord
from discord.ext import commands
import random
import time
from discord import app_commands
import traceback
import json
import datetime
from keep_alive import keep_alive
from discord import app_commands
from discord_webhook import DiscordWebhook, DiscordEmbed

keep_alive()

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

webhook = DiscordWebhook(
    url=
    "https://discord.com/api/webhooks/1191756659740119122/6nqMpuEH9tKdS_CVpAOhenkHsszel7YG8jYMg69uOcUuGHYuZkGr8HlIm2tAVwPrWBWZ"
)


@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name="매입시티"))
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
  except Exception as e:
    print(e)


@bot.event
async def on_message_edit(before, after):
  log_channel_id = 1189092016009781268  # Replace with your desired log channel ID
  log_channel = bot.get_channel(log_channel_id)

  if log_channel:
    edit_time = after.edited_at if after.edited_at else before.created_at

    log_data = {
        "type": "edited",
        "user": str(after.author),
        "content_before": before.content,
        "content_after": after.content,
        "timestamp": str(edit_time)
    }

    with open("message_log.json", "a") as log_file:
      json.dump(log_data, log_file)
      log_file.write("\n")

    embed = discord.Embed(
        title="편집한 메시지",
        description=f"**Time of Edit:** {edit_time}",
        color=0x7289da  # Discord color (Blurple)
    )

    embed.add_field(name="전", value=before.content, inline=False)
    embed.add_field(name="후", value=after.content, inline=False)
    embed.add_field(name="유저", value=after.author, inline=False)
    embed.add_field(name="채널", value=after.channel.mention, inline=False)

    embed1 = DiscordEmbed(
        title="편집한 메시지",
        description=f"**Time of Edit:** {edit_time}",
        color=0x7289da  # Discord color (Blurple)
    )

    embed.add_field(name="전", value=before.content, inline=False)
    embed.add_field(name="후", value=after.content, inline=False)
    embed.add_field(name="유저", value=after.author, inline=False)
    embed.add_field(name="채널", value=after.channel.mention, inline=False)

    await log_channel.send(embed=embed)
    webhook.add_embed(embed1)
    response = webhook.execute()


@bot.event
async def on_message_delete(ctx):
  if ctx.author.bot:
    return
  target_channel_id = 1189092016009781268
  current_time = datetime.datetime.now()

  log_data = {
      "type": "deleted",
      "user": str(ctx.author),
      "content": ctx.content,
      "timestamp": str(current_time)
  }

  with open("message_log.json", "a") as log_file:
    json.dump(log_data, log_file)
    log_file.write("\n")

  embed = discord.Embed(title="Deleted Message Log",
                        color=discord.Color.red(),
                        timestamp=current_time)

  embed.add_field(name="삭제자:", value=ctx.author, inline=False)
  embed.add_field(name="삭제된 메세지", value=ctx.content, inline=False)
  embed.add_field(name='메세지 체널', value=ctx.channel, inline=False)

  embed1 = DiscordEmbed(title="Deleted Message Log",
                        color='0xFFFF0000',
                        timestamp=current_time)

  embed.add_field(name="삭제자:", value=ctx.author, inline=False)
  embed.add_field(name="삭제된 메세지", value=ctx.content, inline=False)
  embed.add_field(name='메세지 체널', value=ctx.channel, inline=False)

  target_channel = ctx.guild.get_channel(target_channel_id)
  await target_channel.send(embed=embed)
  webhook.add_embed(embed1)
  response = webhook.execute()


@bot.tree.command(name='메시지_챁기', description='삭제/편집된 메시지를 찾는다')
@app_commands.checks.has_permissions(administrator=True)
async def find_messages(interaction: discord.Interaction, user: discord.User):
  log_data = []
  with open("message_log.json", "r") as log_file:
    for line in log_file:
      log_entry = json.loads(line)
      if log_entry["user"] == str(user):
        log_data.append(log_entry)

  if log_data:
    embed = discord.Embed(title=f"{user}의 메시지", color=0x00ff00)

    for entry in log_data:
      if entry["type"] == "edited":
        embed.add_field(
            name="편집된 메시지",
            value=
            f"**전:** {entry['content_before']}\n**후:** {entry['content_after']}\n**타임스탬프:** {entry['timestamp']}",
            inline=False)
      elif entry["type"] == "deleted":
        embed.add_field(
            name="삭제된 메시지",
            value=
            f"**Content:** {entry['content']}\n**Timestamp:** {entry['timestamp']}",
            inline=False)

    await interaction.response.send_message(embed=embed)
  else:
    await interaction.response.send_message(f"{user.mention}과 과련된 메세지가 없읍니다")


@bot.event
async def on_member_remove(member):
  # Log the user who left and the timestamp
  log_channel_id = 1189092016009781268  # Replace with your log channel ID
  log_channel = bot.get_channel(log_channel_id)

  if log_channel:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{member.name}이 서버를 나갔습니다 \n시간: {timestamp}"

    await log_channel.send(log_message)
    webhook1 = DiscordWebhook(url=webhook, content=log_message)
    response = webhook.execute()


bot.run(
    'MTE4OTA4OTYxMjYxMDY4MjkxMg.GxKR9Y.mbFmqSouq05ue_0aX3B57oC2vis9mTEnDs_ql0')
