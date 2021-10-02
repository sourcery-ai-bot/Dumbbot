import json
import os

import discord
from discord import Forbidden, Member
from discord.ext import commands

from bot import DumbBot


class Moderaion(commands.Cog):
    def __init__(self, bot: DumbBot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason: str = "None"):
        if member.top_role.position > ctx.author.top_role.position:
            await ctx.send(
                "You can't ban this member cause he has a higher role than you."
            )
        if member.top_role.position == ctx.author.top_role.position:
            await ctx.send(
                "You can't ban this member cause they have the same role position as you."
            )
        else:
            try:
                await member.ban(reason=reason)
                await ctx.send("I have banned {} ".format(member))
                await member.send(
                    "You have been banned from {} for {}".format(ctx.guild, reason)
                )
            except Forbidden:
                pass

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason: str = "None"):
        if member.top_role.position > ctx.author.top_role.position:
            await ctx.send(
                "You can't kick this member cause he has a higher role than you."
            )
        if member.top_role.position == ctx.author.top_role.position:
            await ctx.send(
                "You can't kick this member cause they have the same role position as you."
            )
        else:
            try:
                await member.kick(reason=reason)
                await ctx.send("I have kicked {} ".format(member))
                await member.send(
                    "You have been kickned from {} for {}".format(ctx.guild, reason)
                )
            except Forbidden:
                pass

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason Provided"):
        with open("storage_data/warns.json", "r") as f:
            warns = json.load(f)
        if str(ctx.guild.id) not in warns:
            warns[str(ctx.guild.id)] = {}
        if str(member.id) not in warns[str(ctx.guild.id)]:
            warns[str(ctx.guild.id)][str(member.id)] = {'warns': 1}
            warns[str(ctx.guild.id)][str(member.id)]["warnings"] = [reason]
        else:
            warns[str(ctx.guild.id)][str(member.id)]["warnings"].append(reason)
        with open("storage_data/warns.json", "w") as f:
            json.dump(warns, f)
            await ctx.send(f"{member.mention} was warned for: {reason}")

            embed = discord.Embed(
                title="You have been warned in {}".format(member.guild),
                description=f"You received a warning from {member}",
            )
            embed.add_field(name="Reason:", value=f"{reason}")
            await member.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warns(self, ctx, member: discord.Member):
        with open("storage_data/warns.json", "r") as f:
            warns = json.load(f)

        warnings = discord.Embed(title=f"{member}'s warns")
        for num, warn in enumerate(warns[str(ctx.guild.id)][str(member.id)]["warnings"], start=1):
            warnings.add_field(name=f"Warn {num}", value=warn, inline=False)
        await ctx.send(embed=warnings)


def setup(bot: DumbBot):
    bot.add_cog(Moderaion(bot))
