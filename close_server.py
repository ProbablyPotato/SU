# Function to apply the role to all members with the specified role
async def apply_role():
    guild = client.get_guild(guild_id)
    apply_role = guild.get_role(CLOSED_ROLE_ID)
    usual_role = guild.get_role(STANDARD_ROLE_ID)

    for member in guild.members:
        if usual_role in member.roles and apply_role not in member.roles:
            await member.add_role(apply_role)

    print(f"Applied role {apply_role.name} to all members with role {usual_role.name}")

# Function to remove the role from all members
async def remove_role():
    guild = client.get_guild(guild_id)
    apply_role = guild.get_role(CLOSED_ROLE_ID)
    usual_role = guild.get_role(STANDARD_ROLE_ID)

    for member in guild.members:
        if usual_role in member.roles and apply_role in member.roles:
            await member.remove_role(apply_role)

    print(f"Removed role {apply_role.name} from all members")



async def start_schedule():
    print(f'Bot scheduler has been triggered!')
    # Set up the scheduler to run the functions at the specified times
    scheduler.add_job(apply_role, 'cron', hour=APPLY_TIME.split(':')[0], minute=APPLY_TIME.split(':')[1])
    scheduler.add_job(remove_role, 'cron', hour=REMOVE_TIME.split(':')[0], minute=REMOVE_TIME.split(':')[1])
    scheduler.start()

