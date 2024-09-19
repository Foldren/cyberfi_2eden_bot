import models
from models import User, Reward


async def get_referral_reward(lead: User, referral_code: str) -> None:
    """
    Функция для получения награды за зарегистрированного реферала.
    :param lead: объект модели User лида
    :param referral_code: код из реферальной ссылки
    """
    referrer = await User.filter(referral_code=referral_code).select_related("stats").first()
    if referrer:
        lead.referrer_id = referrer.id
        await lead.save()

        referrer.stats.invited_friends += 1
        await referrer.stats.save()

        match referrer.stats.invited_friends:
            case 1:
                await Reward.create(type_name=models.RewardType.INVITE_FRIENDS, user_id=referrer.id, amount=2000)
            case 5:
                await Reward.create(type_name=models.RewardType.INVITE_FRIENDS, user_id=referrer.id, amount=5000)
            case 100:
                await Reward.create(type_name=models.RewardType.INVITE_FRIENDS, user_id=referrer.id, amount=50000)
            case 1000:
                await Reward.create(type_name=models.RewardType.INVITE_FRIENDS, user_id=referrer.id, amount=250000)