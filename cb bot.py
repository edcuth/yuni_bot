#todo
from botkey import bot_key
import discord
from discord.ext import commands
#prefix for the boss commands, can be changed to anything
bot = commands.Bot(command_prefix='!', case_insensitive=True)

class Table:
    def __init__(self):
        """ table constructor, uses a 2D array for the reservations (self.bosses), self.boss_name is for potential memes """
        self.bosses = [[],[],[],[],[],[]]
        self.boss_names = [""]*5

    def __str__(self):
        """ Returns a string with a dropdown list for each boss with all their respective reservations. Uses `` at the start and at the end so discord keeps the formating a bit better """
        s = "`"
        for i in range(1, 6):
            s += "Boss {0}({1}): \n".format(i, self.boss_names[i-1])
            for user in self.bosses[i - 1]:
                s += "  {0}\n".format(str(user.display_name))
        s += "Carryover:\n"
        for user in self.bosses[5]:
            s += "  {0}\n".format(str(user.display_name))
        s += "`"
        return s
        
""" initializes the table """
table = Table()

@bot.event
async def on_ready():
    """ sets up a custom status (as playing a game since discord actually doesn't support custom status for bots. """
    await bot.change_presence(activity=discord.Game(name="!h for help."))
    print('Im Ready')

    
@bot.command()
async def rsv(ctx, arg=""):
    """ Command to make reservations, can reserve any number of bosses """
    x = 0
    try:
        for i in arg:
            if i not in "123456":
                continue
            if ctx.author not in table.bosses[int(i) - 1]:
                table.bosses[int(i) - 1].append(ctx.author)
                x += 1
    except TypeError as te:
        await ctx.send("Please only use numbers for reserves.")
        print(te)
    except IndexError as ie:
        await ctx.send("Please only use numbers from 1 to 6.")
        print(ie)
    await ctx.send(str(x) + " bosses reserved>" + str(ctx.author.display_name))
            
@bot.command()
async def good(ctx):
    """ good bot :relieved"""
    await ctx.send("https://media.discordapp.net/attachments/430877608389902346/767146032017702912/yunigif.gif")

@bot.command()
async def reserv(ctx):
    await ctx.send(table)

@bot.command()
async def ment(ctx, arg):
    """ mentions all the users queue'd for the boss in the argument, only uses the first character of the argument"""
    try:
        if arg[0] not in "123456":
            raise IndexError
        s = "Boss {0}:\n".format(arg[0])
        for user in table.bosses[int(arg[0]) - 1]:
            s += "<@{0}>\n".format(user.id)
        await ctx.send(s)
    except IndexError as IE:
        await ctx.send("Please only use numbers from 1~6.")
        

@bot.command()
async def fin(ctx, arg=""):
    """ removes reservations from any number of bosses"""
    x = 0
    try:
        for i in arg:
            if i not in "123456":
                continue
            table.bosses[int(i) - 1].remove(ctx.author)
            x += 1
    except TypeError as TE:
        await ctx.send("please only use numbers to remove reserves.")
    except ValueError as VE:
        await ctx.send("No reservation found for the specified bosses")
    except IndexError as ie:
        await ctx.send("Please only use numbers from 1 to 6")
    await ctx.send(str(x) + " reservations removed>" + str(ctx.author.display_name))

@bot.command()
async def name_boss(ctx, boss_id="", boss_name=""):
    """ Changes the name of the boss, takes 2 arguements, the boss ID and the name to set """
    try:
        if boss_id not in "12345":
            raise IndexError
        table.boss_names[int(boss_id[0]) - 1] = boss_name
        await ctx.send("Boss {0} name set to {1}".format(boss_id[0], boss_name))
    except IndexError as IE:
        await ctx.send("Please use numbers from 1 to 5 to select the boss, the a name for the boss.")

@bot.command()
async def clean(ctx):
    """ Removes all reservations from table.bosses """
    if 425791550371397653 not in [role.id for role in ctx.author.roles]:
        return await ctx.send("Only mods can use this command.")
    table.bosses = [[]*6]
    return await ctx.send("ALL RESERVATIONS REMOVED")

@bot.command()
async def h(ctx):
    await ctx.send("**rsv**: adds a reservation, from 1 to 6 (6 is carryover).\
\n**fin**: removes any nunmber of reservations, from 1 to 6.\
\n**ment**: mentions all the users with reservations for a boss, from 1 to 6.\
\n**reserv**: posts a list with each boss and their respective reservations.\
\n**name_boss**: changes a boss name: `!name_boss (boss_id) (boss_name)`.\
\n**clean**: removes all the reservations, only mods can use this command.\
\n**good**: <:yuni:640688445936631843>")

bot.run(bot_key())
