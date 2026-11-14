#!/usr/bin/env python3
"""Serve site/ locally the way Netlify and GitHub Pages do: /base-load serves
base-load.html. Used by the browser tests. Usage: serve.py PORT"""
import http.server
import os
import sys
from functools import partial

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and os.path.exists(p + '.html'):
            return p + '.html'
        return p

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    http.server.ThreadingHTTPServer(('127.0.0.1', port), partial(Handler, directory=ROOT)).serve_forever()
