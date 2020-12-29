"""
Module contains the regex rules that will be used during processing text
in the preparator.py module.
"""
import re
from razdel.segmenters.tokenize import PUNCTS

PUNCTUATIONS = re.compile(f"[%s]" % re.escape(PUNCTS))

DOMAINS = "(com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel" \
          "|xxx|рф|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs" \
          "|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee" \
          "|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm" \
          "|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk" \
          "|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl" \
          "|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si" \
          "|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug" \
          "|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)"
URLS = re.compile(r"r(https?://[^\s]+)|(www\.[^\s]+)|([\wа-яА-Я]+\.{}[^\s]+)".format(DOMAINS), re.IGNORECASE)

SWORDS = ['и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так',
          'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'ее', 'мне',
          'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'ли', 'если', 'уже', 'или', 'ни',
          'него', 'до', 'вас', 'нибудь', 'уж', 'вам',
          'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'они', 'тут', 'где', 'надо', 'ней',
          'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'без', 'раз', 'тоже', 'себе',
          'под', 'ж', 'кто', 'этот', 'того', 'какой', 'совсем', 'ним',
          'здесь', 'этом', 'один', 'мой', 'тем', 'нее', 'куда', 'зачем',
          'всех', 'никогда', 'можно', 'при', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше',
          'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя',
          'свою', 'этой', 'это', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой',
          'им', 'всю']
STOPWORDS = re.compile(rf"\b({'|'.join(SWORDS)})\b")
