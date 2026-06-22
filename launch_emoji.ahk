; ╔══════════════════════════════════════════════════════════════╗
; ║  Custom Emoji Keyboard Launcher  —  AutoHotkey v2            ║
; ║  Bind any hotkey to open custom-emoji-keyboard.py near the cursor.   ║
; ╚══════════════════════════════════════════════════════════════╝
;
; SETUP
;   1. Install AutoHotkey v2  (https://www.autohotkey.com)
;   2. Put this file in the same folder as custom-emoji-keyboard.py
;   3. Double-click launch_emoji.ahk  (or add it to startup)
;   4. Press the hotkey to open the picker
;
; CHANGE YOUR HOTKEY
;   Edit the line that says  YOUR_HOTKEY::  below.
;   Examples:
;     ^!e::        →  Ctrl + Alt + E
;     #.::         →  Win  + .   (same as Windows built-in — override it)
;     ^!Space::    →  Ctrl + Alt + Space
;     F9::         →  F9
;
; HOW IT WORKS
;   • Opens custom-emoji-keyboard.py via pythonw (no console window)
;   • The picker appears near your mouse cursor
;   • Click an emoji → inserts it at your cursor (also copies it)
;   • Hover an emoji's top-right corner → click to copy only
;   • Pressing the hotkey again while the picker is open closes it

#Requires AutoHotkey v2.0
#SingleInstance Force

; Exact title matching only — the Python window is always titled exactly
; "Emoji Picker" (see r.title(...) in the script), never anything else.
; This used to default to "title contains this text anywhere", which
; previously matched an unrelated, currently-open Explorer window whose
; title happened to contain a near-identical string — closing THAT window
; instead of the picker, and skipping the Run(...) line below entirely.
SetTitleMatchMode(3)

; ── Path to custom-emoji-keyboard.py ──────────────────────────────────────
; By default, looks in the same folder as this .ahk file.
; Change this if you keep the files in different locations.
PICKER_SCRIPT := A_ScriptDir . "\custom-emoji-keyboard.py"

; ── Hotkey ───────────────────────────────────────────────────────
; Change  ^!e  to whatever shortcut you prefer (see examples above)
^!e:: {
    global PICKER_SCRIPT

    ; Toggle: if already open, close it
    if WinExist("Emoji Picker") {
        WinClose("Emoji Picker")
        return
    }

    ; Launch without a console window (pythonw instead of python)
    Run('pythonw "' . PICKER_SCRIPT . '"',, "Hide")
}
