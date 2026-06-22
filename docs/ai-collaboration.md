# AI Collaboration Notes

This project was built using Claude (Sonnet 4.6) as a coding assistant. 
Here's a breakdown of my work, along with AI task delegation and component builds.

## What I designed and directed

### v1.0 - v1.2
- The core product concept: a replacement for Windows' built-in emoji picker
- The 20-category taxonomy (see New-Categories.txt) — determined by me
- Unicode range selection for each category, including the decision to handle fully-qualified sequences only and to include base + light skin tone variants
- The decision to use embedded Python data (not .db or .sqlite) after evaluating storage tradeoff options presented by AI
- Bug reproduction: I provided exact error messages, terminal output, and attempted fixes before escalation to AI
- The decision to pause a mid-session build to clarify skin-tone requirements before proceeding — preventing a larger refactor later
- Monitor configuration specification (negative-coordinate secondary monitors)

### v1.3
- Created custom .json file to use with building the grid, combining 1,595 metadata files into a master .json file
- Idea to have a copy icon appear in the upper-right quadrant of the emoji grid box on hover, to copy to clipboard and not immediately send the emoji to the text input
- Worked across multiple apps to determine causes of issues and bugs

## What AI assisted with

### v1.0 - v1.2
- Parsing the emoji-test.txt source file (~620K characters) into category dicts
- Initial UI scaffolding in tkinter
- Iterative fixes to scrollbar styling, canvas rendering, and clipboard encoding
- Explaining why Python 3.14's Tk tightened tag_bind rules, and the fix

### v1.3
- Implemented real Fluent 3D emoji art loading from master_emojis.json + Assets/emoji-images/, with graceful fallback to plain text rendering
- Diagnosed the desktop-graphics-corruption bug from a Windows Event Viewer crash report (tcl86t.dll, exception 0x80000003) to its root cause:
  AttachThreadInput merging our thread's input-queue state with Explorer's, and a Tcl-internal panic during that merge corrupting Explorer's own
  desktop-rendering state. Replaced with plain SetForegroundWindow, which Windows permits without restriction here since the call only ever
  happens immediately after the user's own click
- Found and fixed the launch_emoji.ahk title mismatch (checked for "Custom Emoji Keyboard", actual window title is "Emoji Picker") and switched to
  exact title matching to prevent any future accidental window collisions
- Diagnosed why complex skin-tone+gender emoji sequences rendered as broken fragments (Pillow's basic text layout can't perform the OpenType ligature substitution needed to compose them) and disabled that fallback tier in favor of Tk's native text rendering
- Fixed a Pylance false-positive via local re-imports, verified against the actual Pyright engine rather than by inspection alone

## What I caught and corrected

- Scrollbar style name was invalid; Researched reasoning for error and conveyed updated instructions in subsequent builds on how to fix and avoid that error.
- Clipboard appeared to work (showed in history) but contained no data; I diagnosed using the Windows emoji picker as a verification tool
- Found bug that caused graphics crashes and distortions on desktop, as well as certain windows closing when they were not supposed to. I ran a few tests to narrow down the problem, and then combed through the Event Viewer items to find the error logs describing the issue, which I then handed over to Claude to make the fix.