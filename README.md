<p align="center"><img src="https://cdn.discordapp.com/attachments/871821842694959104/929501481927848056/Screenshot_from_2022-01-09_03-37-02.png" /></p>

<h1 align="center" size="25">
  <pre><code>Charity#2894</code></pre>
</h1>

<h6><code>INFO</code> This repository uses the deprecated and unmaintained <a href="https://github.com/Rapptz/discord.py">discord.py Python3 API wrapper</a> (Charity uses the PyPi v1.7.2) and will stop working soon. Discord expects all bots to migrate over to a special Slash Commands implementation by April 2022. <a href="https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1">Read more here.</a> Following the archival, I stopped regular maintenance of this project but will continue if I can spare time redeveloping the source using the Javascript Discord API library building a few additional scientific and computing modules onto the current codebase.</h6>

## About
Versatile moderation bot utilising modern Pythonic Discord API (PyPi v1.7.2) with many utilities, and a few fun modules for an invite-only global community language server that I administer. Charity uses a self-hosted MongoDB database on the backend for a few flexible user-data modules and is entirely written in Python.

## Development
This project is in its beta phase and it might be a while before it sees the light of dawn with an alpha release. There are several exploitable security vulnerabilities in the code and the server configurator is failing my UX expectations and will not have a public release until a few more subversions. Until then, some moderator and auto-moderator features will be disabled.

## Features
The following is an exhaustive list of all the features I've been able to succesfully implement from scratch so far (may not be updated w.r.t. the latest commits):
**MODERATION:**
- Auto-moderator
  - Anti-massmention
  - Anti-spam
- Moderator
  - Modmail
  - Annoucer / Replier
  - Message purge
  - Scheduled message
  - Warn
  - Kick
  - Mute / Unmute
  - Ban / Unban
  - Temporary ban
  - Moderation log

**UTILITIES:**
- Guild join message
- AFK notifier
- English - English Dictionary
- `DEPRECATED` Server poll
- Song lyrics
- Bing image search
- Google translate
- Google web search
- YouTube video search
- `DEPRECATED` YouTube audio play
- `PRIVATE` Confession

**FUN:**
- Starboard
- Hello World
- `PRIVATE` Custom react

## Contribution
Issues and pull requests are appreciated and most welcome! If you wish to collaborate and revive this project with your support, find me on Discord at `Anathema#3633` or reach me out via [mail](mailto:jay.dnb@outlook.in).

## Invite link
*I'd not recommend using Charity in a full-fledged active community*. [Tap to invite Charity#2894 to your guild.](https://discord.com/api/oauth2/authorize?client_id=838831095730143283&permissions=8&scope=bot)

## License
[`LICENSE`](https://github.com/jay-io/Charity/blob/dev/LICENSE) This project is licensed under the GNU General Public License v3.0.
