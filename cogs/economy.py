import io
import json
import os

import discord
from discord.ext import commands, flags, tasks

from bot import DumbBot
from utils.economy_manager import *


class Economy(commands.Cog):
    def __init__(self, bot: DumbBot):
        self.bot = bot

    @commands.command(aliases=["bal", "BAL", "Bal"])
    async def balance(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await open_account(member)
        user = member
        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        eme = discord.Embed(title=f"{user.name}'s balance", color=ctx.author.color)
        eme.add_field(name="Wallet", value=wallet_amt, inline=False)
        eme.add_field(name="Bank", value=bank_amt, inline=False)
        eme.add_field(name="Net Worth", value=f"{bank_amt + wallet_amt}", inline=False)
        await ctx.send(embed=eme)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(501)

        await ctx.send(f"Someone Gave you {earnings} coins!")

        users[str(user.id)]["wallet"] += earnings

        with open("storage_data/bank.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def daily(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(1000, 10000)

        await ctx.send(f"Someone Gave you {earnings} coins!")

        users[str(user.id)]["wallet"] += earnings

        with open("storage_data/bank.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Ok, you wanna tell me how much you want to withdraw now?")
            return

        bal = await update_bank(ctx.author)
        amount = int(amount)
        if amount == "all":
            amount = bal[0]

        if amount > bal[1]:
            await ctx.send("You don't have that much money")
            return

        if amount < 0:
            await ctx.send("amount must be postitive")
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")

        await ctx.send(f"You withdrew {amount} of coins!")

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount=None):
        try:
            await open_account(ctx.author)
            if amount == None:
                await ctx.send(
                    "Ok, you wanna tell me how much you want to deposit now?"
                )
                return

            bal = await update_bank(ctx.author)
            amount = int(amount)
            if amount == "all":
                amount = bal[0]
            if amount > bal[0]:
                await ctx.send("You don't have that much money")
                return

            if amount < 0:
                await ctx.send("amount must be postitive")
                return

            await update_bank(ctx.author, -1 * amount)
            await update_bank(ctx.author, amount, "bank")

            await ctx.send(f"You deposited {amount} of coins!")
        except ValueError:
            await ctx.send("You didn't enter a number")

    @commands.command(aliases=["give", "moneygive", "givemoney", "send"])
    async def sendmoney(self, ctx, member: discord.Member, amount=None):
        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("Ok, you wanna tell me how much you want to withdraw now?")
            return

        bal = await update_bank(ctx.author)
        amount = int(amount)
        if amount == "all":
            amount = bal[0]

        if amount > bal[1]:
            await ctx.send("You don't have that much money")
            return

        if amount < 0:
            await ctx.send("amount must be postitive")
            return

        await update_bank(ctx.author, -1 * amount, "bank")
        await update_bank(member, amount, "bank")

        await ctx.send(f"You Gave {amount} of coins to {member}")



def setup(bot: DumbBot):
    bot.add_cog(Economy(bot))
