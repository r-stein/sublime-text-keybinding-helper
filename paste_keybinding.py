import sublime
import sublime_plugin
import re


_RE_COMMAND_PATTERN = re.compile(
     "command: "
     "(?P<command>\w*)"
     "(?: {(?P<args>[^\}]*)})?"
 )

_RE_PY_COMMAND_PATTERN = re.compile(
    "[A-Z]\w*Command"
)

keybinding_template = (
    "{\n"
    "\t\"keys\": [\"${1:ctrl+alt+shift+a}\"],\n"
    "\t\"command\": \"%s\""
    "%s,$2\n"
    "},$0"
)

mousebinding_template = (
    "{\n"
    "\t\"button\": \"${1:button1}\",\n"
    "\t\"modifiers\": [\"${2:alt}\"],\n"
    "\t\"press_command\": \"drag_selected\",\n"
    "\t\"command\": \"%s\""
    "%s,$3\n"
    "},$0"
)


def get_template(view):
    if len(view.sel()):
        point = view.sel()[0].b
        if view.score_selector(point, "source.sublimekeymap"):
            return keybinding_template
        elif view.score_selector(point, "source.sublimemousemap"):
            return mousebinding_template
    return keybinding_template


class PasteKeybindingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = sublime.get_clipboard()
        command_match = _RE_COMMAND_PATTERN.match(text)
        py_command_match = _RE_PY_COMMAND_PATTERN.match(text)

        if command_match:
            command = command_match.group("command")
            args = command_match.group("args")
            argstr = ""
            if args:
                argstr = ",\n\t\"args\": { %s }" % args
            template = get_template(self.view)
            keybinding = template % (command, argstr)
            self.view.run_command("insert_snippet", {"contents": keybinding})
        elif py_command_match:
            command = re.sub(r"Command$", "", text)
            command = re.sub(r"(?<=[a-z])([A-Z])", r"_\1", command)
            command = command.lower()
            template = get_template(self.view)
            keybinding = template % (command, "")
            self.view.run_command("insert_snippet", {"contents": keybinding})
        else:
            self.view.run_command("paste")
