#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from base64 import urlsafe_b64encode
from hashlib import blake2b

import pygments.lexers
import redis
from flask import Flask, abort, request, send_from_directory
from pygments import highlight
from pygments.formatters import HtmlFormatter

DOMAIN = os.getenv("PASTA_DOMAIN", "paste.steeve.io")
TLS = os.getenv("PASTA_TLS", False)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

SCHEME = "https" if TLS else "http"
URL = f"{SCHEME}://{DOMAIN}"

redis = redis.Redis(host=REDIS_HOST, port=6379, db=0)

HTML = '<!DOCTYPE html> <html> <head> <meta charset="UTF-8" /> <meta name="viewport" content="width=device-width" /> <title>Pasta</title> <style> body {{ background-color: #272822; color: #f8f8f2 }} </style> </head> <body> {} </body> </html>'  # noqa

HOME = f"""<pre>
pasta(1)                             PASTA                             pasta(1)

NAME
    pasta: command line pastebin.

SYNOPSIS
    < command > | curl -F 'paste=<-' {URL}

DESCRIPTION
    add ?<lang> to resulting url for line numbers and syntax highlighting
    use this form to paste from a browser

EXAMPLES
    $ cat bin/ching | curl -F 'paste=<-' {URL}
       {URL}/aXZI
    $ firefox {URL}/aXZI?py
    $ curl {URL}/aXZI?raw

SEE ALSO
    http://github.com/WnP/pasta
</pre>"""


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def main():
        if request.method == "POST" and "paste" in request.form:
            paste = request.form["paste"]
            h = (
                urlsafe_b64encode(
                    blake2b(paste.encode(), digest_size=3).digest()
                )
                .decode("ascii")
                .replace("=", "")
            )
            redis.set(h, paste)
            return f"""{URL}/{h}
    """
        return HTML.format(HOME)

    @app.route("/<h>", methods=["GET"])
    def get(h):
        paste = redis.get(h)
        if paste is None:
            abort(404)

        args = [k for k in request.args.keys()]
        syntax = args and args[0] or None
        if syntax == "raw":
            return paste.decode()
        try:
            lexer = pygments.lexers.get_lexer_by_name(syntax)
        except Exception:
            lexer = pygments.lexers.TextLexer()
        paste = highlight(
            paste,
            lexer,
            HtmlFormatter(
                full=True,
                style="monokai",
                lineanchors="n",
                linenos="inline" if syntax is not None else False,
                # weird, but this works and utf-8 does not.
                encoding="latin-1",
            ),
        )
        return paste.decode("latin-1").replace(
            # Fix linenos background color
            "background-color: #f0f0f0; ",
            "",
            2,
        )

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            app.root_path, "favicon.ico", mimetype="image/vnd.microsoft.icon"
        )

    return app
