from yt_subtitle_downloader.formatter import format_text
from youtube_transcript_api import YouTubeTranscriptApi
import unicodedata
import logging


def extract_subtitles(identifier: str, language: str) -> str:
    default_languages = ['en', 'de']

    transcript_info = YouTubeTranscriptApi.list_transcripts(identifier)
    available_languages = [lang.language_code for lang in transcript_info]
    default_languages.extend(available_languages)

    if language in available_languages:
        caption = YouTubeTranscriptApi.get_transcript(identifier, [language])
    else:
        transcript = transcript_info.find_transcript(default_languages)
        translated_script = transcript.translate(language)
        caption = translated_script.fetch()

    return normalize_subtitles(caption)


def extract_formatted_subtitles(identifier: str, language: str) -> str:
    subtitles = extract_subtitles(identifier, language)
    logging.info('Finished extracting subtitles from yt-video')

    return format_text(subtitles)


def normalize_subtitles(transcript: [str]) -> str:
    subtitle = ''
    for line in transcript:
        subtitle += line['text'] + ' '

    return unicodedata.normalize('NFKD', subtitle)
