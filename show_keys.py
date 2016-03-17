import sublime
import sublime_plugin


def toggle_show_input(name):
    """Returns and toggles the current show state"""
    state = toggle_show_input.states.get(name, True)
    toggle_show_input.states[name] = not state
    return state

toggle_show_input.states = {}


class ToggleShowCommandsCommand(sublime_plugin.WindowCommand):
    def run(self):
        show_commands = toggle_show_input("show_commands")
        sublime.log_commands(show_commands)
        print("Show commands: {0}".format(show_commands))
        if show_commands:
            self.window.run_command("show_panel", {"panel": "console"})


class ToggleShowInputsCommand(sublime_plugin.WindowCommand):
    def run(self):
        show_input = toggle_show_input("show_input")
        sublime.log_input(show_input)
        print("Show input: {0}".format(show_input))
        if show_input:
            self.window.run_command("show_panel", {"panel": "console"})
