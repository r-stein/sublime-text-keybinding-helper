# Keybinding Helper

A plugin with the purpose to show keybindings and simplify the creation of new keybindings.


## Show used keybindings

Use ``ctrl+alt+` `` to show they used commands (keybindings) and ``ctrl+alt+shift+` `` to show the keys (key events). This will just open the console and call `sublime.log_commands` or `sublime.log_input`.


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

This does also work if you write a `TextCommand` plugin and copy the name, e.g. `PasteKeybindingCommand`.

