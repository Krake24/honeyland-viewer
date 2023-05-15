import os
import disnake
import requests
from disnake.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned)

landUrl = "https://content.honey.land/assets/u1/lands/"
genesisBeeUrl = "https://content.honey.land/assets/bees/honeyland genesis/"
generationsBeeUrl = "https://content.honey.land/assets/bees/honeyland generations/"

defaultHeaders = {"User-Agent": "Honeyland Bot"}


@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))


@bot.slash_command()
async def show(inter):
  pass


@show.sub_command(description="Shows info for the given land ID")
async def land(inter, id: commands.Range[1, 2000]):
  url = landUrl + f"{id:05d}" + ".json"
  print("calling: " + url)
  result = requests.get(url, headers=defaultHeaders).json()

  embed = disnake.Embed(title=result['name'], colour=0xFFD324)
  embed.set_image(url=result['image'])
  for attribute in result['attributes']:
    embed.add_field(name=attribute['trait_type'],
                    value=attribute['value'],
                    inline=True)
  await inter.response.send_message(embed=embed)


@show.sub_command(description="Shows info for the given genesis bee ID",
                  name="genesis_bee")
async def genesis(inter, id: commands.Range[0, 5499]):
  url = genesisBeeUrl + f"{id:04d}" + ".json"
  print("calling: " + url)
  result = requests.get(url, headers=defaultHeaders).json()

  embed = disnake.Embed(title=result['name'], colour=0xFFD324)
  embed.set_image(url=result['image'].replace(" ", "%20"))
  for attribute in result['attributes']:
    embed.add_field(name=attribute['trait_type'],
                    value=attribute['value'],
                    inline=True)
  await inter.response.send_message(embed=embed)


@show.sub_command(description="Shows info for the given generations bee ID",
                  name="generations_bee")
async def generations(inter, id: commands.Range[0, 200000]):
  url = generationsBeeUrl + str(id) + ".json"
  print("calling: " + url)
  try:
      result = requests.get(url, headers=defaultHeaders).json()
  except:
      await inter.response.send_message("This bee doesn't seem to exist", ephemeral=True)
      return

  embed = disnake.Embed(title=result['name'], colour=0xFFD324)
  embed.set_image(url=result['image'].replace(" ", "%20"))
  for attribute in result['attributes']:
    embed.add_field(name=attribute['trait_type'],
                    value=attribute['value'],
                    inline=True)
  await inter.response.send_message(embed=embed)


bot.run(os.environ['botToken'])
