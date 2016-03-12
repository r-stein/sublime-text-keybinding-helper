import sublime
import sublime_plugin


class ToggleShowCommandsCommand(sublime_plugin.WindowCommand):
    def run(self):
        show_commands = not self.window.settings().get("kh_do_show_commands")
        self.window.settings().set("kh_do_show_commands", show_commands)
        sublime.log_commands(show_commands)
        print("Show commands: {0}".format(show_commands))
        if show_commands:
            self.window.run_command("show_panel", {"panel": "console"})


class ToggleShowInputsCommand(sublime_plugin.WindowCommand):
    def run(self):
        show_input = not self.window.settings().get("kh_do_show_input")
        self.window.settings().set("kh_do_show_input", show_input)
        sublime.log_input(show_input)
        print("Show input: {0}".format(show_input))
        if show_input:
            self.window.run_command("show_panel", {"panel": "console"})
