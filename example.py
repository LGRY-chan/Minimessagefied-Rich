from minimessage_rich import MiniMessageConsole

console = MiniMessageConsole()

console.print("--- MiniMessage Test Cases ---")
console.print("1. Bold & Nested: <red>Hello <bold>MiniMessage</bold></red>!")
console.print("2. Hex: <#00ff00>This is hex green</#00ff00>")
console.print("3. Gradient: <gradient:red:blue:green>This is a smooth gradient from red to blue!</gradient>")
console.print("4. Click: <click:open_url:'https://github.com/Textualize/rich'><gradient:#ff0000:#0000ff>[<u>Click here</u> for Rich!]</gradient></click>")
console.print("5. Universal Closer: <green>Green text</> back to normal")
console.print("6. Multi-tag: <b:u:i>Bold Underlined Italic</>")
console.print("7. Rainbow-ish: <rainbow>Rainbow Gradient</rainbow>")

# Integration with other rich objects
from rich.table import Table
from minimessage_rich import parse
table = Table(title="MiniMessage in Tables")
table.add_column("Tag", style="cyan")
table.add_column("Result")
table.add_row("<red>Red</red>", parse("<red>Red</red>"))
table.add_row("<gradient:yellow:red>Fire</>", parse("<gradient:yellow:red>Fire</>"))
console.print(table)
