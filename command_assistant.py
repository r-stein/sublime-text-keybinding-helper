import json
import sublime
import sublime_plugin

# the current capturing state
capturing = False


# button texts must be a single word surrounded with braces
_COPY_TEXT = "[COPY]"
_CLOSE_TEXT = "[CLOSE]"
_BUTTON_TEXTS = [_COPY_TEXT, _CLOSE_TEXT]


def _reset_sel(view):
    view.sel().clear()
    view.sel().add(sublime.Region(0, 0))


def _write_clipboard(command_name, args):
    # write it in the format, that the paste will work automatically
    template = "command: {0} {1}"
    argstr = json.dumps(args) if args else ""
    keybinding = template.format(command_name, argstr)
    sublime.set_clipboard(keybinding)
    print("Write clipboard: '{0}'".format(keybinding))


class ShowCommandAssistantCommand(sublime_plugin.WindowCommand):
    def run(self):
        global capturing
        capturing = True

        view = self.window.create_output_panel("keybinding")
        self.window.run_command("show_panel", {"panel": "output.keybinding"})

        vsettings = view.settings()
        vsettings.set("draw_white_space", "none")


class KhReplaceCaptureCommand(sublime_plugin.TextCommand):
    def run(self, edit, command_name, args=None):
        view = self.view
        width, _ = view.viewport_extent()
        em_width = view.em_width()
        columns = width / em_width

        button_text = " ".join(_BUTTON_TEXTS)
        button_text = " " * (int(columns) - len(button_text) - 3) + button_text
        text = "command: " + command_name
        if args:
            text += "\n   args: " + json.dumps(args)
        text += "\n" + button_text
        text += "\n"
        view.replace(edit, sublime.Region(0, view.size()), text)
        _reset_sel(view)

        # store the information in the view
        vsettings = view.settings()
        vsettings.set("kh_content_length", view.size())
        vsettings.set("kh_command_name", command_name)
        vsettings.set("kh_args", args)


class KhAppendInfoCommand(sublime_plugin.TextCommand):
    def run(self, edit, info):
        view = self.view
        content_length = view.settings().get("kh_content_length", view.size())
        content_region = sublime.Region(content_length, view.size())
        view.replace(edit, content_region, info)


class CommandAssistantListener(sublime_plugin.EventListener):

    # ------------------------------------------
    # Handle "button" clicks in the output panel
    # ------------------------------------------

    def __init__(self):
        # add the handler for each button
        self._button_handler = {
            _COPY_TEXT: self._button_copy,
            _CLOSE_TEXT: self._button_close
        }

    def _button_copy(self, view):
        command_name = view.settings().get("kh_command_name", "")
        if not command_name:
            return
        args = view.settings().get("kh_args", None)
        _write_clipboard(command_name, args)
        view.run_command("kh_append_info", {"info": "Copied keybinding"})
        _reset_sel(view)

    def _button_close(self, view):
        global capturing
        # set the capture state to false
        capturing = False
        # destroy the output panel and delete the view
        del self.output_view
        sublime.active_window().destroy_output_panel("keybinding")

    def on_selection_modified_async(self, view):
        if not capturing:
            return
        if not hasattr(self, "output_view"):
            return
        if view != self.output_view:
            return
        if (len(view.sel()) != 1 or
                not view.sel()[0].empty() or
                view.sel()[0].a == 0):
            return
        point = view.sel()[0].b
        word = view.word(point)
        command = view.substr(sublime.Region(word.a - 1, word.b + 1))
        if command in self._button_handler:
            self._button_handler[command](view)

    # -------------------------------------
    # show the commands in the output panel
    # -------------------------------------

    def _show_command_callback(self, command_name, args):
        window = sublime.active_window()
        # if not set, set the output_view to the correct panel
        if not hasattr(self, "output_view"):
            self.output_view = window.get_output_panel("keybinding")
        # if the output view is not longer active, call the close event
        # to cleanup and not waste cpu time to write into an invisible view
        if window.active_panel() != "output.keybinding":
            self._button_close(self.output_view)
            return
        run_args = {"command_name": command_name, "args": args}
        self.output_view.run_command("kh_replace_capture", run_args)

    def _show_command(self, command_name, args):
        # set a timeout to not block sublime
        sublime.set_timeout(
            lambda: self._show_command_callback(command_name, args), 1)

    def on_text_command(self, view, command_name, args):
        if not capturing:
            return
        # we don't want to handle every single mouse click
        if command_name == "drag_select":
            return
        self._show_command(command_name, args)

    def on_window_command(self, window, command_name, args):
        if not capturing:
            return
        self._show_command(command_name, args)
