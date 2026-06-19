# AI Collaboration Notes

This project was built using Claude (Sonnet 4.6) as a coding assistant. 
Here's a breakdown of my work, along with AI task delegation and component builds.

## What I designed and directed

- The core product concept: a replacement for Windows' built-in emoji picker
- The 20-category taxonomy (see New-Categories.txt) — written entirely by me
- Unicode range selection for each category, including the decision to handle
  fully-qualified sequences only and to include base + light skin tone variants
- The decision to use embedded Python data (not .db or .sqlite) after evaluating
  storage tradeoff options presented by AI
- Bug reproduction: I provided exact error messages, terminal output, and
  attempted fixes before escalation to AI
- The decision to pause a mid-session build to clarify skin-tone requirements
  before proceeding — preventing a larger refactor later
- Monitor configuration specification (negative-coordinate secondary monitors)

## What AI assisted with

- Parsing the emoji-test.txt source file (~620K characters) into category dicts
- Initial UI scaffolding in tkinter
- Iterative fixes to scrollbar styling, canvas rendering, and clipboard encoding
- Explaining why Python 3.14's Tk tightened tag_bind rules, and the fix

## What I caught and corrected

- Scrollbar style name was invalid; Researched reasoning for error and conveyed updated instructions in subsequent builds on how to fix and avoid that error.
- Clipboard appeared to work (showed in history) but contained no data;
  I diagnosed using the Windows emoji picker as a verification tool