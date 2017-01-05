# Keybinding Helper

A plugin with the purpose to show keybindings and simplify the creation of new keybindings.

New in version 2.1.0:

- support of the [Suricate package](https://packagecontrol.io/packages/Suricate)
- support of pasting into python `run_command` calls

## Command Assistant *(ST3 only)*

The command assistant shows the executed commands in an output panel and adds a `[COPY]`-*button* to copy the command. Afterwards it can be pasted into a keymap via [Paste keybindings](#paste-keybindings) to create a keybinding. Press `` alt+` `` or `ctrl+shift+p` and write `KeybindingHelper: Show Command Assistant` to show the *Command Assistant*. If you click on `[COPY]` it will copy the command in your clipboard. Afterwards you can paste it via `ctrl+v` into a keymap to create a keybinding. Use the `[CLOSE]`-*button* or press `escape` to close the panel.

![kh_command_assistant](https://cloud.githubusercontent.com/assets/12573621/14055462/856e63fa-f2e2-11e5-82b1-cc969d1739fd.gif)


## Show used keybindings

Use ``ctrl+alt+` `` (*KeybindingHelper: Toggle show commands*) to show the used commands (keybindings) and ``ctrl+alt+shift+` `` (*KeybindingHelper: Toggle show inputs*) to show the keys (key events). This will just open the console and call `sublime.log_commands` or `sublime.log_input`.
Copy a line from the console (*Hint: Click on the line above*) and paste it into a keymap to create a keybinding.

![kbh_example_show_key](https://cloud.githubusercontent.com/assets/12573621/13863434/0f483dfc-ec9a-11e5-996b-c8bda789ea80.gif)


## Paste keybindings

Because the keybinding is bound to a scope, it requires the [PackageDev](https://packagecontrol.io/packages/PackageDev) package to be installed.

Select and copy a command from the console and paste it into a keymap.
E.g. you could select `command: paste_keybinding` and paste it into a keymap. This will create a snippet, which transforms it into a valid keybinding and will insert the following:

``` js
{
    "keys": ["ctrl+alt+shift+a"],
    "command": "paste_keybinding",|
},
```

This does also work if you write a `TextCommand` plugin and copy the name, e.g. `PasteKeybindingCommand`. If it ends with `Command` it will automatically converted into a keybinding.

![kbh_paste_command](https://cloud.githubusercontent.com/assets/12573621/13863430/023aa104-ec9a-11e5-99b0-f7effdb9b017.gif)

This does also work in profile files of the [Suricate package](https://packagecontrol.io/packages/Suricate) or paste inside a python `run_command` call.