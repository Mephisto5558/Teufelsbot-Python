from json import load
from itertools import chain

from utils import Command, i18n_provider, cooldowns, permission_translator, error_handler, message_component_handler, get_owner_only_folders, autocomplete_generator, Colors, better_partial

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

owner_only_folders = get_owner_only_folders()
error_embed = EmbedBuilder(color=Colors.Red)

def run(client, interaction):
  if interaction.user.id in client.settings.blacklist: return None

  locale = interaction.guild.db['config.lang'] or interaction.guild.local_code
  if interaction.type == InteractionType.MessageComponent:
    return message_component_handler(interaction, better_partial(i18n_provider.__, locale=locale))

  command = client.slash_commands.get(interaction.command_name)

  if command and interaction.type == InteractionType.ApplicationCommandAutocomplete:
    return interaction.respond(autocomplete_generator(interaction, command, locale))

  lang = better_partial(
      i18n_provider.__, locale=locale,
      backup_path=f'commands.{command.category.lower()}.{command.alias_of or command.name}' if command else None
  )

  # DO NOT REMOVE THIS STATEMENT!
  if not isinstance(command, Command) or (command.category.lower() in owner_only_folders and interaction.user.id != client.application.owner.id):
    return None

  if client.bot_type == 'dev' and not command.beta:
    if config.get('replyOnNonBetaCommand') is False: return None
    return interaction.reply(embeds=[error_embed.set_description(lang('events.command_non_beta'))], ephemeral=True)

  if command.disabled:
    if config.get('replyOnDisabledCommand') is False: return None
    return interaction.reply(embeds=[error_embed.set_description(lang('events.command_disabled'))])

  disabled_list = interaction.guild.db[f'command_settings.{command.alias_of or command.name}.disabled'] or \
      {'members': [], 'channels': [], 'roles': []}

  if interaction.user.id in disabled_list['members']:
    return interaction.reply(embeds=[error_embed.set_description(lang('events.not_allowed.member'))], ephemeral=True)
  if interaction.user.id in disabled_list['channels']:
    return interaction.reply(embeds=[error_embed.set_description(lang('events.not_allowed.channel'))], ephemeral=True)
  if disabled_list['roles'] and any(e.id in disabled_list['roles'] for e in interaction.member.roles.cache):
    return interaction.reply(embeds=[error_embed.set_description(lang('events.not_allowed.role'))], ephemeral=True)

  if command.category.lower() == 'nsfw' and not interaction.channel.nsfw:
    return interaction.reply(embeds=[error_embed.set_description(lang('events.nsfw_command'))], ephemeral=True)

  for option in list(chain.from_iterable(command.options)):
    if option.autocomplete_options and option.strict_autocomplete and interaction.options.get(option.name) and not any(
        interaction.options.get(option.name).value.lower() in (e.lower() if isinstance(e, str) else e['value'].lower())
        for e in autocomplete_generator(interaction, command, locale) or []
    ):
      return interaction.reply(embeds=[error_embed.set_description(lang('events.strict_autocomplete_no_match'))], ephemeral=True)

  if client.bot_type != 'dev':
    cooldown = cooldowns(interaction, command.name, command.cooldowns)
    if cooldown: return interaction.reply(embeds=[error_embed.set_description(lang('events.cooldown', cooldown))], ephemeral=True)

  if interaction.type == InteractionType.ApplicationCommand:
    user_perms_missing = interaction.member.permissionsIn(interaction.channel).missing(command.permissions.user)
    client_perms_missing = interaction.guild.members.me.permissionsIn(interaction.channel).missing(command.permissions.client)

    if user_perms_missing or client_perms_missing:
      error_embed.data.title = lang('events.permission_denied.embed_title')
      error_embed.data.description = lang(
          f"events.permission_denied.embed_description_{'user' if user_perms_missing else 'bot'}",
          permissions='`, `'.join(permission_translator(user_perms_missing or client_perms_missing))
      )

      return interaction.reply(embeds=[error_embed], ephemeral=True)

    if not command.no_defer and not interaction.replied: interaction.defer_reply(ephemeral=command.ephemeral_defer or False)

    try:
      command.run(interaction, lang)
      if client.bot_type != 'dev':
        client.db.set('BOTSETTINGS', f'stats.{command.name}', (client.settings[f'stats.{command.name}'] or 1) + 1)
    except Exception as err:  # pylint:disable=broad-exception-caught
      return error_handler(client, err, interaction, lang)
