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

## Demonstration

__Show user keybindings__

This demonstrates the feature to show the used keybindings. Just press ``ctrl+alt+` `` or `ctrl+shift+p` and write `KeybindingHelper: Toggle show commands` to show all commands in the Sublime Text Console. Copy a line from the console (*Hint: Click on the line above*) and paste it into a keymap to create a keybinding.

![kbh_example_show_key](https://cloud.githubusercontent.com/assets/12573621/13863434/0f483dfc-ec9a-11e5-996b-c8bda789ea80.gif)

__Paste command definitions__

This demonstrates an other mode of the paste keybinding command for Sublime Text package developers. Just select and copy the class name and paste it a keymap. If it ends with `Command` it will automatically converted into a keybinding.

![kbh_paste_command](https://cloud.githubusercontent.com/assets/12573621/13863430/023aa104-ec9a-11e5-99b0-f7effdb9b017.gif)