u"""[위키북스] 파이썬 웹 프로그래밍 실습 예제."""
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, url_for


def print_setting(config):
    print "================================================"
    print "SETTINGS for PHOTOLOG APPLICATION"
    print "================================================"
    for key, value in config:
        print "%s=%s" % (key, value)
    print "================================================"


def not_found(error):
    return render_template("404.html"), 404


def server_error(error):
    err_msg = str(error)
    return render_template("500.html", err_msg=err_msg), 500


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def create_app(config_filepath="resource/config.cfg"):
    photolog_app = Flask(__name__)

    from photolog.photolog_config import PhotologConfig
    from photolog.photolog_logger import Log
    from photolog.database import DBManager
    from photolog.controller import *
    from photolog.cache_session import SimpleCacheSessionInterface
    from photolog.photolog_blueprint import photolog

    photolog_app.config.from_object(PhotologConfig)
    photolog_app.config.from_pyfile(config_filepath, silent=True)
    print_settings(photolog_app.config.iteritems())

    log_filepath = os.path.join(photolog_app.root_path,
                                photolog_app.config["LOG_FILE_PATH"])
    Log.init(log_filepath=log_filepath)

    db_filepath = os.path.join(photolog_app.root_path,
                               photolog_app.config['DB_FILE_PATH'])
    db_url = photolog_app.config['DB_URL'] + db_filepath
    DBManager.init(db_url, eval(photolog_app.config['DB_LOG_FLAG']))
    DBManager.init_db()

    photolog_app.register_blueprint(photolog)

    photolog_app.session_interface = SimpleCacheSessionInterface()

    photolog_app.error_handler_spec[None][404] = not_found
    photolog_app.error_handler_spec[None][500] = server_error

    photolog_app.jinja_env.globals["url_for_other_page"] = \
        url_for_other_page

    return photolog_app
