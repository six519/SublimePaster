# -*- coding: utf-8 -*-


from api import PastebinImplementation
from vendor import lodgeitlib


class Lodgeit(PastebinImplementation):

    # _name = 'lodgeit'

    SYNTAXES = {
       #'syntax'     : 'lodgeit language code'
        'python'     : 'python',
        'sql'        : 'sql',
        'javascript' : 'js',
        'json'       : 'js',
        'css'        : 'css',
        'xml'        : 'xml',
        'diff'       : 'diff',
        'rb'         : 'ruby',
        'rhtml'      : 'rhtml',
        'hs'         : 'literate-haskell',
        'sh'         : 'bash', 
        'ini'        : 'ini', 
        'tst'        : 'text',
        'plaintext'  : 'text',
        'yaml'       : 'yaml', 
        'html'       : 'html'
    }

    def __init__(self, view):
        super(Lodgeit, self).__init__(view)
        self.pastebin = lodgeitlib.Lodgeit(
            self.config.get('url'), 
            username=self.config.get('username'), 
            password=self.config.get('password')
        )

    def prepare(self, content):
        return content

    def upload(self, content):
        lang = self.language()
        content = self.prepare(content)
        paste_id = self.pastebin.new_paste(
            content, lang, parent=None, 
            filename='', mimetype='', private=False)
        new_paste = self.pastebin.get_paste_by_id(paste_id)
        return new_paste.url
