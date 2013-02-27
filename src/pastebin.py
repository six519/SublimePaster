# -*- coding: utf-8 -*-

import api
import os.path
from vendor import pastebin_python
from vendor.pastebin_python.pastebin_formats import *
from vendor.pastebin_python.pastebin_constants import PASTEBIN_URL, PASTE_PRIVATE, PASTE_PUBLIC
from vendor.pastebin_python.pastebin_exceptions import PastebinBadRequestException, PastebinHTTPErrorException

class PasteBinPython(api.PastebinImplementation):

    _name = 'pastebin'

    SYNTAXES = {
       #'syntax'                :   'http://pastebin.com language code'
        "actionscript"          :   FORMAT_ACTIONSCRIPT,
        "applescript"           :   FORMAT_APPLESCRIPT,
        "asp"                   :   FORMAT_ASP,
        "batchfile"             :   FORMAT_WINBATCH,
        "c#"                    :   FORMAT_C_SHARP,
        "c"                     :   FORMAT_C,
        "c++"                   :   FORMAT_CPP,
        "clojure"               :   FORMAT_CLOJURE,
        "css"                   :   FORMAT_CSS,
        "d"                     :   FORMAT_D,
        "diff"                  :   FORMAT_DIFF,
        "erlang"                :   FORMAT_ERLANG,
        "go"                    :   FORMAT_GO,
        "dot"                   :   FORMAT_DOT,
        "groovy"                :   FORMAT_GROOVY,
        "haskell"               :   FORMAT_HASKELL,
        "html"                  :   FORMAT_HTML,
        "java"                  :   FORMAT_JAVA,
        "javascript"            :   FORMAT_JAVASCRIPT,
        "latex"                 :   FORMAT_LATEX,
        "lisp"                  :   FORMAT_LISP,
        "lua"                   :   FORMAT_LUA,
        "makefile"              :   FORMAT_MAKE,
        "matlab"                :   FORMAT_MATLAB,
        "objective-c"           :   FORMAT_OBJECTIVE_C,
        "ocaml"                 :   FORMAT_OCAML,
        "perl"                  :   FORMAT_PERL,
        "php"                   :   FORMAT_PHP,
        "python"                :   FORMAT_PYTHON,
        "r"                     :   FORMAT_R,
        "rubyonrails"           :   FORMAT_RAILS,
        "regexp"                :   FORMAT_REG,
        "ruby"                  :   FORMAT_RUBY,
        "scala"                 :   FORMAT_SCALA,
        "shell-unix-generic"    :   FORMAT_BASH,
        "sql"                   :   FORMAT_SQL,
        "tcl"                   :   FORMAT_TCL,
        "plaintext"             :   FORMAT_NONE,
        "xml"                   :   FORMAT_XML,
        "yaml"                  :   FORMAT_YAML
    }

    def url(self):
        return self.config.get('url') or PASTEBIN_URL

    def upload(self, content):
        pl = FORMAT_NONE
        pbin = pastebin_python.PastebinPython(api_dev_key='f4dfe115d610ebddc278115d9f80752d')

        if self.syntax() in self.SYNTAXES:
            pl = self.SYNTAXES[self.syntax()]

        username = self.config.get('username', '')
        password = self.config.get('password', '')
        isPrivate = PASTE_PRIVATE if self.config.get('private', False) else PASTE_PUBLIC
        filename = os.path.basename(self.view.file_name() if self.view.file_name() else 'Untitled')

        if username and password:
            try:
                pbin.createAPIUserKey(username, password)
            except PastebinBadRequestException as e:
                raise api.TransportError("Invalid username or password")

        try:
            pbinURL = pbin.createPaste(content, filename, pl, isPrivate)
            return pbinURL
        except PastebinBadRequestException as e:
            raise api.TransportError("An error occurred: %s" % str(e))

    def fetch(self, paste_id):
        pbin = pastebin_python.PastebinPython(api_dev_key='f4dfe115d610ebddc278115d9f80752d')

        try:
            rawOutput = pbin.getPasteRawOutput(paste_id)
            return (rawOutput, None, "%s%s" % (self.url(), paste_id))
        except PastebinHTTPErrorException as e:
            raise api.TransportError("Unknown paste id '%s'" % paste_id)