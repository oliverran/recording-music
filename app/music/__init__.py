from flask import Blueprint

from .view import music

from .view import MusicHuman, RecordingStudio, NewsView, MusicHumanPage,RecordingStudioPage,NewsPage

music_human = MusicHuman.as_view('music_human')
music.add_url_rule('/music-human/', view_func=music_human)
music.add_url_rule('/music-human/<int:page>/', view_func=music_human)

music.add_url_rule('/music-human/page/<int:id>/', view_func=MusicHumanPage.as_view('music_human_page'))
music.add_url_rule('/recording-studio/page/<int:id>/', view_func=RecordingStudioPage.as_view('recording_studio_page'))
music.add_url_rule('/news/page/<int:id>/', view_func=NewsPage.as_view('news_page'))

recording_studio = RecordingStudio.as_view('recording_studio')
music.add_url_rule('/recording-studio/', view_func=recording_studio)
music.add_url_rule('/recording-studio/<int:page>/', view_func=recording_studio)

news = NewsView.as_view('news')
music.add_url_rule('/news/', view_func=news)
music.add_url_rule('/news/<int:page>/', view_func=news)
