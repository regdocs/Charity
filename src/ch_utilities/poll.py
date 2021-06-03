import discord
from discord.ext import commands
from ch_boot.startup import *

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def poll(ctx):
    poll = {}
    def check(m):
        return m.channel == ctx.channel and ctx.author == m.author

    continue_loop = True
    wizard = await ctx.channel.send("Poll wizard invoked. Type `.cancel` to end the wizard. This will lead to loss of unsaved information. Choose your type of poll:\n`1. Anonymous`\n`2. Non-anonymous`")
    while continue_loop:
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        elif reply.content == "1":
            poll["type"] = "anonymous"
            poll["epoch_t"] = time.time()
            continue_loop = False
            await reply.add_reaction('☑️')
        elif reply.content == "2":
            poll["type"] = "non-anonymous"
            poll["epoch_t"] = time.time()
            continue_loop = False
            await reply.add_reaction('☑️')
        else:
            await ctx.channel.send("Invalid input. Try again.", delete_after = 3)
        await reply.delete(delay = 3)

    continue_loop = True
    await wizard.edit(content = "Enter the poll title [question] below.")
    while continue_loop:
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        else:
            poll["title"] = reply.content
            continue_loop = False
            await reply.add_reaction('☑️')
        await reply.delete(delay = 3)

    continue_loop = True
    await wizard.edit(content = "Enter the number of choices. Upto 15 choices supported.")
    while continue_loop:
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        try:
            integer = int(reply.content)
        except TypeError:
            await ctx.channel.send("Invalid input. Try again.", delete_after = 3)
            continue
        if integer > 15:
            await ctx.channel.send("Invalid input. Try again.", delete_after = 3)
        else:
            poll["no_of_choices"] = integer
            continue_loop = False
            await reply.add_reaction('☑️')
        await reply.delete(delay = 3)

    choice_counter = 1
    choice_list = []
    while choice_counter != poll["no_of_choices"] + 1:
        await wizard.edit(content = f"Enter choice #{choice_counter} text.")
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        elif len(reply.content) > 350:
            await ctx.channel.send("The length of the option's string cannot exceed 350 characters. Try again.", delete_after = 3)
        else:
            choice_list.append(reply.content)
            await reply.add_reaction('☑️')
            choice_counter += 1
        await reply.delete(delay = 3)

    continue_loop = True
    choice_counter = 1
    choices_dict = {}
    choice_emotes_def = [
        "🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴"
    ]
    await wizard.edit(content = "Type `.default` to let me assign the default reacts against the requested options, or type `.custom` to continue to the next step of assigning custom reacts.")
    while continue_loop:
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        elif reply.content == ".default":
            for i in range(poll["no_of_choices"]):
                choices_dict[choice_emotes_def[i]] = choice_list[i]
                await reply.add_reaction('☑️')
                continue_loop = False
        elif reply.content == ".custom":
            pass # to be continued
        else:
            await ctx.channel.send("Invalid input. Try again.", delete_after = 3)
        await reply.delete(delay = 3)

    poll["choices"] = choices_dict
    print (poll)
    """ continue_loop = False
    while continue_loop:
        await wizard.edit(content = f"React the emote ") """
