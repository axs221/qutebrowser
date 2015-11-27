# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

import pytest

import pytest_bdd as bdd

# pylint: disable=unused-import
from test_yankpaste import skip_with_broken_clipboard


# https://github.com/The-Compiler/qutebrowser/issues/1124#issuecomment-158073581
pytestmark = pytest.mark.qt_log_ignore(
    '^QXcbClipboard: SelectionRequest too old', extend=True)


bdd.scenarios('caret.feature')


@bdd.when("I yank the selected text")
def yank_selected_text(qtbot, qapp, quteproc):
    """Run :yank-selected and wait until the clipboard content changes."""
    with qtbot.wait_signal(qapp.clipboard().changed):
        quteproc.send_cmd(':yank-selected')


@bdd.then(bdd.parsers.parse('the clipboard should contain:\n{content}'))
def clipboard_contains_multiline(qapp, content):
    data = qapp.clipboard().text()
    expected = '\n'.join(line.strip() for line in content.splitlines())
    assert data == expected
