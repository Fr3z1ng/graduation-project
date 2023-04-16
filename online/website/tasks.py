from .censor import CENSOR
from profanityfilter import ProfanityFilter
from celery import shared_task

from website.models import CommentWebsite
from dotenv import load_dotenv

load_dotenv()

pf = ProfanityFilter()


@shared_task()
def replace_text_with_censored(comment_id):
    pf_custom = ProfanityFilter(custom_censor_list=CENSOR)
    comment = CommentWebsite.objects.get(id=comment_id)
    censored_text = pf_custom.censor(comment.text)
    comment.text = censored_text
    comment.save()
