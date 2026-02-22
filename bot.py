"""
Operators Bot - A simple Discord bot with tarot, philosophy, journaling, and mental models.
Uses discord.py. Keep your bot token in a .env file or set BOT_TOKEN in environment.
"""

import asyncio
import os
import random
import discord
from discord import app_commands, Intents, Message
from discord.ext import commands, tasks

# Load .env file if present (optional; BOT_TOKEN can also be set in environment)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Configuration: put your token in .env as BOT_TOKEN=your_token_here ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
# Channel ID for the background philosophy announcements (set to your channel's ID, or None to disable)
ANNOUNCEMENT_CHANNEL_ID = 1364423221314846802  # e.g. 123456789012345678

# --- Tarot cards: name + short meaning (beginner-friendly list) ---
TAROT_CARDS = [
    ("The Fool", "New beginnings, leap of faith, innocence"),
    ("The Magician", "Manifestation, skill, resourcefulness"),
    ("The High Priestess", "Intuition, mystery, inner wisdom"),
    ("The Empress", "Abundance, nurturing, creativity"),
    ("The Emperor", "Structure, authority, stability"),
    ("The Hierophant", "Tradition, teaching, spiritual guidance"),
    ("The Lovers", "Choice, partnership, alignment of values"),
    ("The Chariot", "Willpower, victory, determination"),
    ("Strength", "Courage, patience, inner strength"),
    ("The Hermit", "Soul-searching, wisdom, solitude"),
    ("Wheel of Fortune", "Change, cycles, destiny"),
    ("Justice", "Fairness, truth, cause and effect"),
    ("The Hanged Man", "Letting go, new perspective, sacrifice"),
    ("Death", "Transformation, endings, rebirth"),
    ("Temperance", "Balance, moderation, patience"),
    ("The Devil", "Shadow self, attachment, illusion"),
    ("The Tower", "Sudden change, revelation, upheaval"),
    ("The Star", "Hope, inspiration, renewal"),
    ("The Moon", "Unconscious, dreams, illusion"),
    ("The Sun", "Joy, success, vitality"),
    ("Judgement", "Awakening, reflection, absolution"),
    ("The World", "Completion, wholeness, accomplishment"),
]

# --- Operator philosophy quotes (reply when someone @mentions the bot) ---
PHILOSOPHY_REPLIES = [
    "The map is not the territory.",
    "The best time to plant a tree was 20 years ago; the second best time is now.",
    "You don't rise to the level of your goals; you fall to the level of your systems.",
    "What gets measured gets managed.",
    "Invert, always invert.",
    "First principles: break down the problem to what you know is true, then reason up.",
    "The obstacle is the way.",
    "Focus on the process, not the outcome.",
    "You are the average of the five people you spend the most time with.",
    "Skin in the game: only take advice from those who share the downside.",
    "I would tell you the answer, but then you'd stop growing. So: figure it out.",
    "The stars have spoken. They said 'touch grass.'",
    "Have you considered that you might just be the problem?",
    "Correct. And also wrong. Simultaneously. Welcome to reality.",
    "This too shall pass. Unless it doesn't. Both outcomes are instructive.",
    "The universe has a plan for you. It did not ask for your input.",
    "Ah yes. A classic mistake. I've seen it a thousand times. Good luck.",
    "Your enemies are also doing their best. Horrifying, isn't it?",
    "The answer is obvious in hindsight. That's the joke.",
    "You already know what to do. You just don't like the answer.",
    "Bold strategy. Let's see if it works.",
    "The oracle has consulted itself. The oracle is also confused.",
    "Everything is a system. Including your excuses.",
    "Somewhere, someone is doing the thing you're procrastinating on. Just saying.",
    "Fate is just probability with a flair for drama.",
]

# --- Journaling prompts for /reflect ---
JOURNALING_PROMPTS = [
    "What's one thing that went well today and why?",
    "What would you do differently if you could redo today?",
    "What are you avoiding that you know you should face?",
    "What's a belief you hold that you've never really questioned?",
    "What would you tell your past self from one year ago?",
    "What are you grateful for right now?",
    "What's one small step you could take tomorrow toward something that matters to you?",
    "When did you last feel fully present? What were you doing?",
    "What feedback have you been ignoring?",
    "What would you do if you weren't afraid of failing?",
]

# --- Mental models for /leverage ---
MENTAL_MODELS = [
    ("Second-order thinking", "Consider not just the immediate effect of a decision, but the effects of those effects."),
    ("Inversion", "Instead of 'how do I succeed?', ask 'how would I fail?' and avoid those paths."),
    ("Occam's Razor", "Among competing hypotheses, prefer the one with the fewest assumptions."),
    ("Hanlon's Razor", "Never attribute to malice what can be explained by stupidity or neglect."),
    ("Pareto Principle (80/20)", "Roughly 80% of effects come from 20% of causes. Find the vital few."),
    ("Circle of competence", "Know the boundaries of what you truly understand; stay inside them when it matters."),
    ("Opportunity cost", "Doing one thing means not doing another. What are you giving up?"),
    ("Margin of safety", "Build in buffer so that when things go wrong, you still have room to act."),
    ("Regression to the mean", "Extreme outcomes are often followed by more average ones; don't over-attribute cause."),
    ("Incentives", "Understand what motivates people; incentives drive behavior more than intentions."),
]

# --- Bot setup ---
intents = Intents.default()
intents.message_content = True  # needed to read message content (e.g. for @mentions)
bot = commands.Bot(command_prefix="!", intents=intents)


# --- Background task: send a random philosophy quote to the announcement channel every 4–8 hours ---
@tasks.loop()
async def philosophy_announcement():
    await bot.wait_until_ready()
    await asyncio.sleep(random.uniform(4 * 3600, 8 * 3600))  # 4–8 hours in seconds
    if ANNOUNCEMENT_CHANNEL_ID:
        channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)
        if channel:
            await channel.send(random.choice(PHILOSOPHY_REPLIES))


@bot.event
async def on_ready():
    """Runs when the bot connects to Discord. Syncs slash commands and starts background tasks."""
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    if ANNOUNCEMENT_CHANNEL_ID:
        philosophy_announcement.start()
        print(f"Philosophy announcement task started (channel ID: {ANNOUNCEMENT_CHANNEL_ID}).")


# --- Tarot reading: pick 1–3 cards and show name + meaning ---
@bot.tree.command(name="tarot", description="Get a tarot reading (1–3 cards).")
@app_commands.describe(cards="Number of cards to draw (1, 2, or 3)")
async def tarot(interaction: discord.Interaction, cards: int = 1):
    await interaction.response.defer()
    if interaction.channel:
        async with interaction.channel.typing():
            await asyncio.sleep(random.uniform(1, 3))
    else:
        await asyncio.sleep(random.uniform(1, 3))
    if cards < 1 or cards > 3:
        await interaction.followup.send("Please choose 1, 2, or 3 cards.", ephemeral=True)
        return
    drawn = random.sample(TAROT_CARDS, cards)
    lines = []
    for name, meaning in drawn:
        lines.append(f"**{name}** — {meaning}")
    await interaction.followup.send("🔮 Your reading:\n\n" + "\n\n".join(lines))


# --- /reflect: random journaling prompt ---
@bot.tree.command(name="reflect", description="Get a random journaling prompt.")
async def reflect(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.channel:
        async with interaction.channel.typing():
            await asyncio.sleep(random.uniform(1, 3))
    else:
        await asyncio.sleep(random.uniform(1, 3))
    prompt = random.choice(JOURNALING_PROMPTS)
    await interaction.followup.send(f"📔 **Reflect:**\n{prompt}")


# --- /leverage: random mental model ---
@bot.tree.command(name="leverage", description="Get a random mental model.")
async def leverage(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.channel:
        async with interaction.channel.typing():
            await asyncio.sleep(random.uniform(1, 3))
    else:
        await asyncio.sleep(random.uniform(1, 3))
    name, description = random.choice(MENTAL_MODELS)
    await interaction.followup.send(f"🧠 **{name}**\n{description}")


# --- When someone @mentions the bot, reply with random operator philosophy ---
@bot.event
async def on_message(message: Message):
    # Don't respond to ourselves
    if message.author.bot:
        return
    # Check if this bot was mentioned in the message
    if bot.user and bot.user.mentioned_in(message):
        async with message.channel.typing():
            await asyncio.sleep(random.uniform(1, 3))
        reply = random.choice(PHILOSOPHY_REPLIES)
        await message.channel.send(reply)
    # Let other commands (e.g. prefix) still run
    await bot.process_commands(message)


def main():
    if not BOT_TOKEN:
        print("No BOT_TOKEN found. Set BOT_TOKEN in your environment or in a .env file.")
        return
    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
