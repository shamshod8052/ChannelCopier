import asyncio

from Admin.models import User


async def user_manager(user: User):
    """Checks whether channel messages for a given user have been copied."""
    ...

started = True

async def copy_manager():
    """Creates a task that copies messages for each user"""
    tasks = [
        user_manager(user) for user in User.objects.filter(status=True).all()
    ]

    await asyncio.gather(*tasks)

    global started
    started = False
