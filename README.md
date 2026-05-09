# Minimessagefied-Rich

A Python library that brings Minecraft's MiniMessage format to the Rich library.

## Features
- Parse MiniMessage tags like `<red>`, `<bold>`, `<click:open_url:'...'>`.
- Custom MiniMessageConsole for automatic string parsing.
- Support for hex colors and nested styles.
- Support for the universal closing tag </>.

## Usage
### python
from minimessage_rich import MiniMessageConsole

```
console = MiniMessageConsole()
console.print('<red>Hello <bold>MiniMessage</bold></red>!')
```
