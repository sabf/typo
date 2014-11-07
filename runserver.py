#!/usr/bin/env python
from __future__ import absolute_import

import os
from werkzeug.serving import run_simple
from typo import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    run_simple('localhost', port, app, use_reloader=True)
