from requests import JSONDecodeError, get

from discord import Embed, Color, ActionRow, Button, ButtonStyle

from utils import Command, Option

cache = {}

class CMD(Command):
  name = 'pokedex'
  slash_command = True
  prefix_command = True
  options = [Option(name='pokémon', type='String', required=True)]

  def run(self, msg, lang):
    pokemon = msg.options.get_string('pokémon') or msg.args[0]
    msg = msg.custom_reply(lang('global.loading'))

    res = cache.get(pokemon.lower())
    if not res:
      try:
        res = get(f'https://pokeapi.glitch.me/v1/pokemon/{pokemon}', timeout=10).json()
      except JSONDecodeError:
        return msg.custom_reply(lang('invalid_json'))

      if res:
        feet, inches = [float(e) for e in res.height.split("'")]
        res.height = (feet * 12 + inches) * 2.54
        res.height = f'{res.height}cm' if res.height < 100 else f'{float(res.height/100):.2f}m'

        if res.name: cache[res.name.lower()] = res

    name = res.name.lower()
    embed = Embed(color=Color.blurple()) \
        .set_thumbnail(url=f'https://play.pokemonshowdown.com/sprites/ani/{name}.gif') \
        .set_footer(text=res.description) \
        .set_author(name=f'PokéDex: {res.name}', icon_url=f'https://play.pokemonshowdown.com/sprites/ani/{name}.gif') \
        .set_fields([
            {'name': lang('types'), 'value': ', '.join(res.types), 'inline': False},
            {'name': lang('abilities'), 'value': f"{res.abilities.normal}{f' and {res.abilities.hidden}' if res.abilities.hidden else ''}.", 'inline': False},
            {'name': lang('genderRatio'), 'value': ', '.join(res.gender) if res.get('gender') else lang('noGender'), 'inline': False},
            {'name': lang('heightWeight'), 'value': f'{res.height}, {(float(res.weight) / 2.205):.2f}kg', 'inline': False},
            {
                'name': lang('evolutionLine'),
                'value': ', '.join(res.family.evolutionLine) + lang('currentStage', res.family.evolutionStage),
                'inline': False
            },
            {'name': lang('gen'), 'value': res.gen, 'inline': False}
        ])

    component = ActionRow([
        Button(label='Blubapedia', style=ButtonStyle.link, url=f'https://blubapedia.blubagarden.net/wiki/{res.name}'),
        Button(label='Serebii', style=ButtonStyle.link, url=f'https://serebii.net/pokedex-swsh/{name}'),
        Button(label='Smogon', style=ButtonStyle.link, url=f'https://smogon.com/dex/ss/pokemon/{name}')
    ])

    return msg.edit(content=None, embeds=[embed], components=[component])
