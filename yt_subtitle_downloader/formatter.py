from yt_subtitle_downloader.deepmultilingualpunctuation.punctuationmodel import PunctuationModel
from nltk import sent_tokenize, download
from truecase import get_true_case
import logging
import re

model = PunctuationModel(model='oliverguhr/fullstop-punctuation-multilang-large')
download('punkt')  # nltk


def preprocessing(text: str) -> str:
    text = re.sub(r"\[.*?\]", "", text)
    return text


def capitalize_sentence(text: str, lang: str = 'english') -> str:
    sentences = sent_tokenize(text, language=lang)
    sentences = [sentence.capitalize() for sentence in sentences]
    return ' '.join(sentences)


def format_text(text: str) -> str:
    text = preprocessing(text)
    logging.info('Finished preprocessing subtitles')
    text = model.restore_punctuation(text)
    logging.info('Finished restoring punctuation')
    text = capitalize_sentence(text, 'english')
    logging.info('Finished capitalizing sentence beginnings')
    text = get_true_case(text)
    logging.info('Finished restoring capitalization')
    return text.replace(' .', '.')  # there is probably a better solution

