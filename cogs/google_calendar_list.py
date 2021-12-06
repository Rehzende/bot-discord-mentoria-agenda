from discord.ext import commands
import discord
from dateutil.parser import parse
from datetime import date
from utils import config as cfg
from utils.google_calendar import list_events
import logging


DIAS = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-Feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]


class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Retorna os agendamento de estudo do dia atual")
    async def agenda(self, ctx):
        """
        usage: >agenda

        """

        try:
            eventos = list_events.getEvents()
            if not eventos:
                embed = discord.Embed(
                    title="📚 Agenda de Estudos :loudspeaker: ")
                embed.add_field(
                    name="**:cold_sweat: Sem Agenda**",
                    value="Use ```>criar_agenda```  e agende um estudo, bora aprender!! ",
                    inline=False,
                )
                embed.set_footer(
                    text="Se você está afim de aprender algo, agende um momento de estudo, para que os demais possam saber do seu interesse."
                )
                await ctx.send(embed=embed)
                return
            data = date.today().strftime("%d %b %Y")
            indice_da_semana = date.today().weekday()
            dia_da_semana = DIAS[indice_da_semana]
            embed = discord.Embed(
                title="📚 Agenda de Estudos :loudspeaker:",
                description=f"Data: {data} - {dia_da_semana}",
            )
            for event in eventos:
                data = parse(event["start"]["dateTime"])
                embed.add_field(
                    name="\u200B",
                    value=cfg.EVENT_TEMPLATE.format(
                        event["summary"],
                        event["location"],
                        data.strftime("%d/%m/%Y - %H:%M"),
                    ),
                    inline=False,
                )
                embed.set_footer(text="")
            await ctx.send(embed=embed)
        except Exception as e:
            logging.error(e)
            embed = discord.Embed(
                title="Erro ao listar os eventos", color=0xFF0000)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Calendar(bot))
