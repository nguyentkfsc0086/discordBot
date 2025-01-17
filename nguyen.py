import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Track join times and cumulative time
join_times = {}
cumulative_times = {}

# Define roles and thresholds
role_categories = {
    "Cố lên bạn ey!!": 1,   # 0-1 hour
    "Còn nhiều thứ để học lắm": 14,  # 1-2 hours
    "Sắp được rồi bạn eiii": 30, # 2-3 hours
    "Đủ chỉ tiêu": 40,  # 3-4 hours
    "Bạn thiêt là đáng ngưỡng mộ": 60,
    "Nào giàu nhớ bọn mình nhé": 70# 4+ hours
}

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        # User joins the voice channel
        join_times[member.id] = datetime.now()
    elif before.channel is not None and after.channel is None:
        # User leaves the voice channel
        join_time = join_times.pop(member.id, None)
        if join_time:
            time_spent = datetime.now() - join_time
            cumulative_times[member.id] = cumulative_times.get(member.id, timedelta()) + time_spent
            await assign_role_based_on_time(member)

async def assign_role_based_on_time(member):
    hours_spent = cumulative_times[member.id].total_seconds() / 3600
    for role_name, threshold in role_categories.items():
        if hours_spent <= threshold:
            role = discord.utils.get(member.guild.roles, name=role_name)
            if role:
                await member.add_roles(role)
                await member.send(f"Congrats {member.name}, you've earned the '{role_name}' role by studying for {hours_spent:.2f} hours!")
            break
@tasks.loop(hours=168)  # 168 hours = 1 week
async def reset_cumulative_times():
    cumulative_times.clear()
bot.run('YOUR_BOT_TOKEN')
