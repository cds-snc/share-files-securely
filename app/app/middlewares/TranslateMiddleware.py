from masonite.middleware import Middleware

import glob
import json
import os


class TranslateMiddleware(Middleware):
    """Middleware that adds translated string to the view."""

    def before(self, request, response):
        language = "en"
        if request.session.has("lang"):
            language = request.session.get("lang")
        languages = self.load_languages()
        if language not in languages:
            language = "en"

        request.app.make("view").share(
            {
                "t": lambda s: languages[language].get(s, f"MISSING_STRING: {s}"),
            }
        )

        return request

    def after(self, request, response):
        return request

    def load_languages(self):
        languages = {}
        language_list = glob.glob("i18n/*.json")
        for lang in language_list:
            filename = lang.split(os.path.sep)
            lang_code = filename[1].split(".")[0]

            with open(lang, "r", encoding="utf8") as file:
                languages[lang_code] = json.load(file)
        return languages
