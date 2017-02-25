import sublime
import sublime_plugin
import re


_RE_COMMAND_PATTERN = re.compile(
    r"command: "
    r"(?P<command>\w*)"
    r"(?: {(?P<args>.*)})?"
)

_RE_PY_COMMAND_PATTERN = re.compile(
    r"[A-Z]\w*Command"
)

keybinding_template = (
    "{\n"
    "\t\"keys\": [\"${1:ctrl+alt+shift+a}\"],\n"
    "\t\"command\": \"<<command>>\""
    "<<args>>,$2\n"
    "},$0"
)

mousebinding_template = (
    "{\n"
    "\t\"button\": \"${1:button1}\",\n"
    "\t\"modifiers\": [\"${2:alt}\"],\n"
    "\t\"press_command\": \"drag_selected\",\n"
    "\t\"command\": \"<<command>>\""
    "<<args>>,$3\n"
    "},$0"
)

surigate_profile_template = (
    '''"${1:<<command>>}":
{
\t"keys": [${2:"<c>+o", "<c>+t"}],
\t"caption": "${3:${1/(?:^|(_))(\\w)/\\U(?1: :)\\2/g}...}",$0
\t"call": "sublime.<<command>>"<<args>>
},
'''
)


def get_template(view):
    if len(view.sel()):
        point = view.sel()[0].b
        if view.score_selector(
                point, "source.json.sublimekeymap, source.sublimekeymap"):
            return keybinding_template
        elif view.score_selector(
                point, "source.json.sublimemousemap, source.sublimemousemap"):
            return mousebinding_template
        elif view.score_selector(point, "source.suricate-profile"):
            return surigate_profile_template
    return keybinding_template


def _to_snake_case_command(text):
    if text.endswith("Command"):
        text = text[:-len("Command")]
    command = re.sub(r"(?<=[a-z])([A-Z])", r"_\1", text)
    command = command.lower()
    return command


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
            keybinding = (
                template
                .replace("<<command>>", command)
                .replace("<<args>>", argstr))
            self.view.run_command("insert_snippet", {"contents": keybinding})
        elif py_command_match:
            command = _to_snake_case_command(text)
            template = get_template(self.view)
            keybinding = (
                template
                .replace("<<command>>", command)
                .replace("<<args>>", ""))
            self.view.run_command("insert_snippet", {"contents": keybinding})
        else:
            self.view.run_command("paste")


class PasteCommandCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = sublime.get_clipboard()
        py_command_match = _RE_PY_COMMAND_PATTERN.match(text)

        if py_command_match:
            command = _to_snake_case_command(text)
            self.view.run_command("insert", {"characters": command})
        else:
            self.view.run_command("paste")
