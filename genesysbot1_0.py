import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix = '!')

info_txt = 'Hello!\n This is where I explain how to the commands. All commands are preceeded by a "!"\n\nroll is the command used for skill checks, and should be entered as followed:\n roll*(space)*Characteristic Score*(space)*Ranks*(space)*# of Purple*(space)*# of Red*(space)*# of Blue*(space)*# of Black*[optional](space)*Name of Skill\n\ninit is the command for initiative rolls, and should be entered as followed:\n init*(space)*Characteristic Score*(space)*Ranks\n\nforce is the command for rolling force dice. The 1 die is rolled by default, but if you need more, enter:\n force*(space)*number'

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game('Genesys'))
    print('Logged in as '+client.user.name+' (ID:'+str(client.user.id)+')')
    print('Genesys Bot is ready')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')

#Clear messages
@client.command(brief = 'Clear previous messages, default previous 4 messages.')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#Defining the rolls
def blue(blue_number = 1):
    boost_outcomes = ['Blank', 'Blank', '1S', '1S, 1A', '2A', '1A']
    i = 0
    blue_outcome = []
    while i < int(blue_number):
        blue_outcome.append(random.choice(boost_outcomes))
        i+=1
    return blue_outcome
def green(g_number = 1):
    ability_outcomes = ['Blank', '1S', '1S', '2S', '1A', '1A', '1S, 1A', '2A']
    i=0
    g_outcomes = []
    while i < int(g_number):
        g_outcomes.append(random.choice(ability_outcomes))
        i+=1
    return g_outcomes
def yellow(y_number = 1):
    prof_outcomes = ['Blank', '1S', '1S', '2S', '2S', '1A', '1S, 1A', '1S, 1A', '1S, 1A', '2A', '2A', 'GH']
    i=0
    y_outcomes = []
    while i < int(y_number):
        y_outcomes.append(random.choice(prof_outcomes))
        i+=1
    return y_outcomes
def black(bl_number = 1):
    setback_outcomes = ['Blank', 'Blank', '1F', '1F', '1D', '1D']
    i=0
    bl_outcome
    while i < int(bl_number):
        bl_outcome.append(random.choice(setback_outcomes))
        i+=1
    return bl_outcome
def purple(p_number = 1):
    diff_outcomes = ['Blank', '1F', '1D', '2F', '1D', '1D', '1F, 1D', '2D']
    i=0
    p_outcome = []
    while i < int(p_number):
        p_outcome.append(random.choice(diff_outcomes))
        i+=1
    return p_outcome
def red(r_number = 1):
    challenge_outcomes = ['Blank', '1F', '1F', '2F', '2F', '1D', '1D', '1F, 1D', '1F, 1D', '2D', '2D', 'BH']
    i=0
    r_outcome = []
    while i < int(r_number):
        r_outcome.append(random.choice(challenge_outcomes))
        i+=1
    return r_outcome
def f_dice(f_number = 1):
    force_outcomes = ['1 Dark', '1 Dark', '1 Dark', '1 Dark', '1 Dark', '1 Dark', '2 Dark', '1 Light', '1 Light', '2 Light', '2 Light', '2 Light']
    i=0
    f_outcome = []
    while i < int(f_number):
        f_outcome.append(random.choice(force_outcomes))
        i+=1
    return f_outcome

#Figure out the results
def clean_list(list1):
    list2 = [x for x in list1 if x != 'Blank']
    list3 = [x for x in list2 if not ", " in x]
    list3a = [x for x in list2 if ", " in x]
    list3b = [x.split(', ') for x in list3a]
    list4 = [x for y in list3b for x in y]
    list_final = list3 + list4
    return list_final
def comp_results(good, bad):
    good_v = [x for x in good if "A" in x]
    good_v2 = [int(x[0]) for x in good_v]
    good_n = [x for x in good if "S" in x]
    good_n2 = [int(x[0]) for x in good_n]
    good_h = [x for x in good if "GH" in x]
    good_h2 = [1 for x in good_h]

    bad_v = [x for x in bad if "D" in x]
    bad_v2 = [int(x[0]) for x in bad_v]
    bad_n = [x for x in bad if "F" in x]
    bad_n2 = [int(x[0]) for x in bad_n]
    bad_h = [x for x in bad if "BH" in x]
    bad_h2 = [1 for x in bad_h]

    vant = sum(good_v2) - sum(bad_v2)
    norm = sum(good_n2) - sum(bad_n2)
    hype = sum(good_h2) - sum(bad_h2)

    print(vant, norm, hype)
    return vant, norm, hype
def init_results(init_list):
    good_v = [x for x in init_list if "A" in x]
    good_v2 = [int(x[0]) for x in good_v]
    good_n = [x for x in init_list if "S" in x]
    good_n2 = [int(x[0]) for x in good_n]
    good_h = [x for x in init_list if "GH" in x]
    good_h2 = [1 for x in good_h]
    vant = sum(good_v2)
    norm = sum(good_n2)
    hype = sum(good_h2)
    print(vant, norm, hype)
    return vant, norm, hype
def force_sort(f_list):
    light = [x for x in f_list if "Light" in x]
    light2 = [int(x[0]) for x in light]
    dark = [x for x in f_list if "Dark" in x]
    dark2 = [int(x[0]) for x in dark]

    tot_dark = sum(dark2)
    tot_light = sum(light2)

    print(tot_dark, tot_light)
    return tot_dark, tot_light

#Skill checks
@client.command(brief = 'Skill Checks')
async def roll(ctx, score = 0, rank = 0, pur = 0, chal = 0, plus = 0, minus = 0, *, ability = None):
    good_results = []
    bad_results = []

    good_dice = [score, rank, plus]
    print(good_dice)
    if (good_dice[0] > good_dice[1]) or (good_dice[0] < good_dice[1]):
        y1 = min(good_dice[0], good_dice[1])
        g1 = max(good_dice[0], good_dice[1]) - y1
        good_results.append(yellow(y1))
        good_results.append(green(g1))
    elif good_dice[0] == good_dice[1]:
        y2 = good_dice[0]
        good_results.append(yellow(y2))
    if good_dice[2] != 0:
        good_results.append(blue(good_dice[2]))

    bad_dice = [pur, chal, minus]
    print(bad_dice)
    if (bad_dice[0] != 0) and (bad_dice[1] != 0) and (bad_dice[2] != 0):
        bad_results.append(purple(bad_dice[0]))
        bad_results.append(red(bad_dice[1]))
        bad_results.append(black(bad_dice[2]))
    elif (bad_dice[0] != 0) and (bad_dice[1] != 0) and (bad_dice[2] == 0):
        bad_results.append(purple(bad_dice[0]))
        bad_results.append(red(bad_dice[1]))
    elif (bad_dice[0] != 0) and (bad_dice[1] == 0) and (bad_dice[2] != 0):
        bad_results.append(purple(bad_dice[0]))
        bad_results.append(black(bad_dice[2]))
    elif (bad_dice[0] == 0) and (bad_dice[1] != 0) and (bad_dice[2] != 0):
        bad_results.append(red(bad_dice[1]))
        bad_results.append(black(bad_dice[2]))
    elif (bad_dice[0] != 0) and (bad_dice[1] == 0) and (bad_dice[2] == 0):
        bad_results.append(purple(bad_dice[0]))
    elif (bad_dice[0] == 0) and (bad_dice[1] != 0) and (bad_dice[2] == 0):
        bad_results.append(red(bad_dice[1]))

    print(good_results)
    print(bad_results)

    flat_good = [x for y in good_results for x in y]
    print(flat_good)
    flat_bad = [x for y in bad_results for x in y]
    print(flat_bad)
    clean_good = clean_list(flat_good)
    clean_bad = clean_list(flat_bad)
    print(clean_good)
    print(clean_bad)

    vant, norm, hype = comp_results(clean_good, clean_bad)

    if ability != None:
        await ctx.send(f'Skill being checked: {ability}')
    else:
        pass

    if (vant == 0) and (norm == 0) and (hype == 0):
        await ctx.send('Net Zero Result')
    else:
        if vant < 0:
            await ctx.send(f'{abs(vant)} disadvantage!')
        elif vant > 0:
            await ctx.send(f'{abs(vant)} advantage!')

        if norm < 0:
            await ctx.send(f'{abs(norm)} failure!')
        elif norm > 0:
            await ctx.send(f'{abs(norm)} success!')

        if hype < 0:
            await ctx.send(f'{abs(hype)} DISPAIR!')
        elif hype > 0:
            await ctx.send(f'{abs(hype)} TRIUMPH!')

@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Looks like you're a number short. Make sure you've put in values for all 6 dice types!")

#Initiative roll
@client.command(brief = 'Initiative Rolls')
async def init(ctx, score = 1, rank = 1):

    init_result = []

    if (score > rank) or (score < rank):
        y1 = min(score, rank)
        g1 = max(score, rank) - y1
        init_result.append(yellow(y1))
        init_result.append(green(g1))
    elif score == rank:
        y2 = score
        init_result.append(yellow(y2))

    print(init_result)

    flat_init = [x for y in init_result for x in y]
    print(flat_init)
    vant, norm, hype = init_results(flat_init)

    if vant != 0:
        await ctx.send(f'{abs(vant)} advantage!')
    else:
        pass
    if norm != 0:
        await ctx.send(f'{abs(norm)} success!')
    else:
        pass
    if hype != 0:
        await ctx.send(f'{abs(hype)} TRIUMPH!')
    else:
        pass

#Force dice
@client.command(brief = 'Force Rolls')
async def force(ctx, num = 1):
    outcome = f_dice(num)
    dark, light = force_sort(outcome)

    if dark != 0:
        await ctx.send(f'{dark} Dark Side')
    else:
        pass
    if light != 0:
        await ctx.send(f'{light} Light Side')

#Dice explaination
@client.command()
async def info(ctx):
    await ctx.send(info_txt)


client.run('NzMzNTQzMjQzNDIxMTg4MTY3.XxEreA.PW4YRXgPl405FZKwMdAhzdltbog')
