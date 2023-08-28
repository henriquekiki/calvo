import discord
from discord.ext import commands, tasks
import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

timers = {
    "minato": {"fixed_time": datetime.timedelta(minutes=120), "custom_time": None, "reset": False},
    "mini minato": {"fixed_time": datetime.timedelta(minutes=60), "custom_time": None, "reset": False},
    "d reaper": {"fixed_time": datetime.timedelta(minutes=60), "custom_time": None, "reset": False},
}

def format_time(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}H{minutes:02}M"

@bot.command()
async def minato(ctx, custom_minutes: int = None):
    if custom_minutes is not None:
        timers['minato']['custom_time'] = datetime.timedelta(minutes=custom_minutes)
        await ctx.send(f"Run de Minato iniciará em {custom_minutes} minutos e depois seguirá o tempo fixo.")
    else:
        await ctx.send(f"Tempo aproximado para Run de Minato: {format_time(timers['minato']['custom_time'] or timers['minato']['fixed_time'])} CH 0")

@bot.command()
async def miniminato(ctx, custom_minutes: int = None):
    if custom_minutes is not None:
        timers['mini minato']['custom_time'] = datetime.timedelta(minutes=custom_minutes)
        await ctx.send(f"Mini run Minato iniciará em {custom_minutes} minutos e depois seguirá o tempo fixo.")
    else:
        await ctx.send(f"Tempo aproximado para Mini run Minato: {format_time(timers['mini minato']['custom_time'] or timers['mini minato']['fixed_time'])} CH 0")

@bot.command()
async def dreaper(ctx, custom_minutes: int = None):
    if custom_minutes is not None:
        timers['d reaper']['custom_time'] = datetime.timedelta(minutes=custom_minutes)
        await ctx.send(f"D-Reaper iniciará em {custom_minutes} minutos e depois seguirá o tempo fixo.")
    else:
        await ctx.send(f"Tempo aproximado para D-Reaper: {format_time(timers['d reaper']['custom_time'] or timers['d reaper']['fixed_time'])} CH 0")

@tasks.loop(seconds=1)
async def update_timers():
    for timer_name, timer in timers.items():
        if timer['custom_time'] and timer['custom_time'].total_seconds() > 0:
            timer['custom_time'] -= datetime.timedelta(seconds=1)
        elif timer['fixed_time'].total_seconds() > 0:
            timer['fixed_time'] -= datetime.timedelta(seconds=1)
        else:
            timer['fixed_time'] = timers[timer_name]['original_fixed_time']

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    for timer in timers.values():
        timer['original_custom_time'] = timer['custom_time']
        timer['original_fixed_time'] = timer['fixed_time']
    update_timers.start()

discord_token = 'MTE0NTc5ODIzMTY1NDE0MTk3Mg.Gjk0Yo.G_OQb8_XMASZjsAH280zt9tZRHK8_0ZwCJds1E'
bot.run(discord_token)