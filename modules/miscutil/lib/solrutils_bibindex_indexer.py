# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Solr utilities.
"""


from invenio.config import CFG_SOLR_URL
from invenio.textutils import remove_control_characters
from invenio.solrutils_config import CFG_SOLR_INVALID_CHAR_REPLACEMENTS


if CFG_SOLR_URL:
    import solr
    SOLR_CONNECTION = solr.SolrConnection(CFG_SOLR_URL) # pylint: disable=E1101


def remove_invalid_solr_characters(utext):
    for char in CFG_SOLR_INVALID_CHAR_REPLACEMENTS:
        try:
            utext = utext.replace(char, CFG_SOLR_INVALID_CHAR_REPLACEMENTS[char])
        except:
            pass
    return utext


def solr_add_fulltext(recid, text):
    """
    Helper function that dispatches TEXT to Solr for given record ID.
    Returns True/False upon success/failure.
    """
    if recid:
        try:
            text = remove_control_characters(text)
            utext = unicode(text, 'utf-8')
            utext = remove_invalid_solr_characters(utext)
            SOLR_CONNECTION.add(id=recid, abstract="", author="", fulltext=utext, keyword="", title="")
            return True
        except (UnicodeDecodeError, UnicodeEncodeError):
            # forget about bad UTF-8 files
            pass
    return False


def solr_commit():
    SOLR_CONNECTION.commit()
