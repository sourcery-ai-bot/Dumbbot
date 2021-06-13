from tortoise import Model, fields

class GuildModel(Model):
    id = fields.BigIntField(pk=True, description="Discord ID of the guild")
    prefix = fields.CharField(
        max_length=5, default=".", description="Custom prefix of the guild", 
        pk=False
    )

    class Meta:
        table = "guilds"
