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
;   • Click an emoji → it copies to clipboard; paste with Ctrl+V
;   • Pressing the hotkey again while the picker is open closes it

#Requires AutoHotkey v2.0
#SingleInstance Force

; ── Path to custom-emoji-keyboard.py ──────────────────────────────────────
; By default, looks in the same folder as this .ahk file.
; Change this if you keep the files in different locations.
PICKER_SCRIPT := A_ScriptDir . "\custom-emoji-keyboard.py"

; ── Hotkey ───────────────────────────────────────────────────────
; Change  ^!e  to whatever shortcut you prefer (see examples above)
^!e:: {
    global PICKER_SCRIPT

    ; Toggle: if already open, close it
    if WinExist("Custom Emoji Keyboard") {
        WinClose("Custom Emoji Keyboard")
        return
    }

    ; Launch without a console window (pythonw instead of python)
    Run('pythonw "' . PICKER_SCRIPT . '"',, "Hide")
}
