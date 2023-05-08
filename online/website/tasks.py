from celery import shared_task
from profanityfilter import ProfanityFilter
from website.models import CommentWebsite

from .censor import CENSOR

pf = ProfanityFilter()


@shared_task()
def replace_text_with_censored(comment_id):
    """
    Делает фильтрацию матных слов в отзывах

    Args:
        comment_id (int): идентификационный номер отзыва

    """
    pf_custom = ProfanityFilter(custom_censor_list=CENSOR)
    comment = CommentWebsite.objects.get(id=comment_id)
    censored_text = pf_custom.censor(comment.text)
    comment.text = censored_text
    comment.save()
