#!/usr/bin/env python3
"""
Emoji Picker  v1.1
────────────────────────────────────────────────────────────────────
Lightweight Windows emoji keyboard — 20 custom categories.

SETUP
  pip install pillow          ← required for full-color emoji rendering

USAGE
  python emoji_picker.py      ← run directly
  See launch_emoji.ahk        ← bind to any hotkey via AutoHotkey v2

CONTROLS
  Click emoji   → copied to clipboard; paste with Ctrl+V anywhere
  Search bar    → search emoji by name across all categories
  Escape / click outside → close
────────────────────────────────────────────────────────────────────
"""
import tkinter as tk
from tkinter import ttk
import ctypes, ctypes.wintypes, platform, os

# ── Optional: Pillow for full-color emoji rendering ──────────────
try:
    from PIL import Image, ImageDraw, ImageFont, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ════════════════════════════════════════════════════════════════════
#  EMBEDDED EMOJI DATA  (auto-generated)
#  • Base (yellow/default) + light-skin-tone variants included
#  • Medium-light / medium / medium-dark / dark tones excluded
#  • Fully-qualified Unicode sequences only
# ════════════════════════════════════════════════════════════════════
EMOJI_DATA = {
    "Smileys": [("😀", "grinning face"), ("😃", "grinning face with big eyes"), ("😄", "grinning face with smiling eyes"), ("😁", "beaming face with smiling eyes"), ("😆", "grinning squinting face"), ("😅", "grinning face with sweat"), ("🤣", "rolling on the floor laughing"), ("😂", "face with tears of joy"), ("🙂", "slightly smiling face"), ("🙃", "upside-down face"), ("🫠", "melting face"), ("😉", "winking face"), ("😊", "smiling face with smiling eyes"), ("😇", "smiling face with halo"), ("🥰", "smiling face with hearts"), ("😍", "smiling face with heart-eyes"), ("🤩", "star-struck"), ("😘", "face blowing a kiss"), ("😗", "kissing face"), ("☺️", "smiling face"), ("😚", "kissing face with closed eyes"), ("😙", "kissing face with smiling eyes"), ("🥲", "smiling face with tear"), ("😋", "face savoring food"), ("😛", "face with tongue"), ("😜", "winking face with tongue"), ("🤪", "zany face"), ("😝", "squinting face with tongue"), ("🤑", "money-mouth face"), ("🤗", "smiling face with open hands"), ("🤭", "face with hand over mouth"), ("🫢", "face with open eyes and hand over mouth"), ("🫣", "face with peeking eye"), ("🤫", "shushing face"), ("🤔", "thinking face"), ("🫡", "saluting face"), ("🤐", "zipper-mouth face"), ("🤨", "face with raised eyebrow"), ("😐", "neutral face"), ("😑", "expressionless face"), ("😶", "face without mouth"), ("🫥", "dotted line face"), ("😶‍🌫️", "face in clouds"), ("😏", "smirking face"), ("😒", "unamused face"), ("🙄", "face with rolling eyes"), ("😬", "grimacing face"), ("😮‍💨", "face exhaling"), ("🤥", "lying face"), ("🫨", "shaking face"), ("🙂‍↔️", "head shaking horizontally"), ("🙂‍↕️", "head shaking vertically"), ("😌", "relieved face"), ("😔", "pensive face"), ("😪", "sleepy face"), ("🤤", "drooling face"), ("😴", "sleeping face"), ("🫩", "face with bags under eyes"), ("😷", "face with medical mask"), ("🤒", "face with thermometer"), ("🤕", "face with head-bandage"), ("🤢", "nauseated face"), ("🤮", "face vomiting"), ("🤧", "sneezing face"), ("🥵", "hot face"), ("🥶", "cold face"), ("🥴", "woozy face"), ("😵", "face with crossed-out eyes"), ("😵‍💫", "face with spiral eyes"), ("🤯", "exploding head"), ("🤠", "cowboy hat face"), ("🥳", "partying face"), ("🥸", "disguised face"), ("😎", "smiling face with sunglasses"), ("🤓", "nerd face"), ("🧐", "face with monocle"), ("😕", "confused face"), ("🫤", "face with diagonal mouth"), ("😟", "worried face"), ("🙁", "slightly frowning face"), ("☹️", "frowning face"), ("😮", "face with open mouth"), ("😯", "hushed face"), ("😲", "astonished face"), ("😳", "flushed face"), ("🫪", "distorted face"), ("🥺", "pleading face"), ("🥹", "face holding back tears"), ("😦", "frowning face with open mouth"), ("😧", "anguished face"), ("😨", "fearful face"), ("😰", "anxious face with sweat"), ("😥", "sad but relieved face"), ("😢", "crying face"), ("😭", "loudly crying face"), ("😱", "face screaming in fear"), ("😖", "confounded face"), ("😣", "persevering face"), ("😞", "disappointed face"), ("😓", "downcast face with sweat"), ("😩", "weary face"), ("😫", "tired face"), ("🥱", "yawning face"), ("😤", "face with steam from nose"), ("😡", "enraged face"), ("😠", "angry face"), ("🤬", "face with symbols on mouth"), ("😈", "smiling face with horns"), ("👿", "angry face with horns"), ("💀", "skull"), ("☠️", "skull and crossbones"), ("💩", "pile of poo"), ("🤡", "clown face"), ("👹", "ogre"), ("👺", "goblin"), ("👻", "ghost"), ("👽", "alien"), ("👾", "alien monster"), ("🤖", "robot"), ("😺", "grinning cat"), ("😸", "grinning cat with smiling eyes"), ("😹", "cat with tears of joy"), ("😻", "smiling cat with heart-eyes"), ("😼", "cat with wry smile"), ("😽", "kissing cat"), ("🙀", "weary cat"), ("😿", "crying cat"), ("😾", "pouting cat"), ("🙈", "see-no-evil monkey"), ("🙉", "hear-no-evil monkey"), ("🙊", "speak-no-evil monkey")],
    "Hearts": [("💌", "love letter"), ("💘", "heart with arrow"), ("💝", "heart with ribbon"), ("💖", "sparkling heart"), ("💗", "growing heart"), ("💓", "beating heart"), ("💞", "revolving hearts"), ("💕", "two hearts"), ("💟", "heart decoration"), ("❣️", "heart exclamation"), ("💔", "broken heart"), ("❤️‍🔥", "heart on fire"), ("❤️‍🩹", "mending heart"), ("❤️", "red heart"), ("🩷", "pink heart"), ("🧡", "orange heart"), ("💛", "yellow heart"), ("💚", "green heart"), ("💙", "blue heart"), ("🩵", "light blue heart"), ("💜", "purple heart"), ("🤎", "brown heart"), ("🖤", "black heart"), ("🩶", "grey heart"), ("🤍", "white heart"), ("💋", "kiss mark")],
    "Emotions": [("💯", "hundred points"), ("💢", "anger symbol"), ("🫯", "fight cloud"), ("💥", "collision"), ("💫", "dizzy"), ("💦", "sweat droplets"), ("💨", "dashing away"), ("🕳️", "hole"), ("💬", "speech balloon"), ("👁️‍🗨️", "eye in speech bubble"), ("🗨️", "left speech bubble"), ("🗯️", "right anger bubble"), ("💭", "thought balloon"), ("💤", "ZZZ")],
    "Hands": [("👈", "backhand index pointing left"), ("👈🏻", "backhand index pointing left: light skin tone"), ("👉", "backhand index pointing right"), ("👉🏻", "backhand index pointing right: light skin tone"), ("👆", "backhand index pointing up"), ("👆🏻", "backhand index pointing up: light skin tone"), ("🖕", "middle finger"), ("🖕🏻", "middle finger: light skin tone"), ("👇", "backhand index pointing down"), ("👇🏻", "backhand index pointing down: light skin tone"), ("☝️", "index pointing up"), ("☝🏻", "index pointing up: light skin tone"), ("🫵", "index pointing at the viewer"), ("🫵🏻", "index pointing at the viewer: light skin tone"), ("👍", "thumbs up"), ("👍🏻", "thumbs up: light skin tone"), ("👎", "thumbs down"), ("👎🏻", "thumbs down: light skin tone"), ("✊", "raised fist"), ("✊🏻", "raised fist: light skin tone"), ("👊", "oncoming fist"), ("👊🏻", "oncoming fist: light skin tone"), ("🤛", "left-facing fist"), ("🤛🏻", "left-facing fist: light skin tone"), ("🤜", "right-facing fist"), ("🤜🏻", "right-facing fist: light skin tone"), ("👏", "clapping hands"), ("👏🏻", "clapping hands: light skin tone"), ("🙌", "raising hands"), ("🙌🏻", "raising hands: light skin tone"), ("🫶", "heart hands"), ("🫶🏻", "heart hands: light skin tone"), ("👐", "open hands"), ("👐🏻", "open hands: light skin tone"), ("🤲", "palms up together"), ("🤲🏻", "palms up together: light skin tone"), ("🤝", "handshake"), ("🤝🏻", "handshake: light skin tone"), ("🙏", "folded hands"), ("🙏🏻", "folded hands: light skin tone"), ("✍️", "writing hand"), ("✍🏻", "writing hand: light skin tone"), ("💅", "nail polish"), ("💅🏻", "nail polish: light skin tone"), ("🤳", "selfie"), ("🤳🏻", "selfie: light skin tone")],
    "Body": [("💪", "flexed biceps"), ("💪🏻", "flexed biceps: light skin tone"), ("🦾", "mechanical arm"), ("🦿", "mechanical leg"), ("🦵", "leg"), ("🦵🏻", "leg: light skin tone"), ("🦶", "foot"), ("🦶🏻", "foot: light skin tone"), ("👂", "ear"), ("👂🏻", "ear: light skin tone"), ("🦻", "ear with hearing aid"), ("🦻🏻", "ear with hearing aid: light skin tone"), ("👃", "nose"), ("👃🏻", "nose: light skin tone"), ("🧠", "brain"), ("🫀", "anatomical heart"), ("🫁", "lungs"), ("🦷", "tooth"), ("🦴", "bone"), ("👀", "eyes"), ("👁️", "eye"), ("👅", "tongue"), ("👄", "mouth"), ("🫦", "biting lip")],
    "People Actions": [("👶", "baby"), ("👶🏻", "baby: light skin tone"), ("🧒", "child"), ("🧒🏻", "child: light skin tone"), ("👦", "boy"), ("👦🏻", "boy: light skin tone"), ("👧", "girl"), ("👧🏻", "girl: light skin tone"), ("🧑", "person"), ("🧑🏻", "person: light skin tone"), ("👱", "person: blond hair"), ("👱🏻", "person: light skin tone, blond hair"), ("👨", "man"), ("👨🏻", "man: light skin tone"), ("🧔", "person: beard"), ("🧔🏻", "person: light skin tone, beard"), ("🧔‍♂️", "man: beard"), ("🧔🏻‍♂️", "man: light skin tone, beard"), ("🧔‍♀️", "woman: beard"), ("🧔🏻‍♀️", "woman: light skin tone, beard"), ("👨‍🦰", "man: red hair"), ("👨🏻‍🦰", "man: light skin tone, red hair"), ("👨‍🦱", "man: curly hair"), ("👨🏻‍🦱", "man: light skin tone, curly hair"), ("👨‍🦳", "man: white hair"), ("👨🏻‍🦳", "man: light skin tone, white hair"), ("👨‍🦲", "man: bald"), ("👨🏻‍🦲", "man: light skin tone, bald"), ("👩", "woman"), ("👩🏻", "woman: light skin tone"), ("👩‍🦰", "woman: red hair"), ("👩🏻‍🦰", "woman: light skin tone, red hair"), ("🧑‍🦰", "person: red hair"), ("🧑🏻‍🦰", "person: light skin tone, red hair"), ("👩‍🦱", "woman: curly hair"), ("👩🏻‍🦱", "woman: light skin tone, curly hair"), ("🧑‍🦱", "person: curly hair"), ("🧑🏻‍🦱", "person: light skin tone, curly hair"), ("👩‍🦳", "woman: white hair"), ("👩🏻‍🦳", "woman: light skin tone, white hair"), ("🧑‍🦳", "person: white hair"), ("🧑🏻‍🦳", "person: light skin tone, white hair"), ("👩‍🦲", "woman: bald"), ("👩🏻‍🦲", "woman: light skin tone, bald"), ("🧑‍🦲", "person: bald"), ("🧑🏻‍🦲", "person: light skin tone, bald"), ("👱‍♀️", "woman: blond hair"), ("👱🏻‍♀️", "woman: light skin tone, blond hair"), ("👱‍♂️", "man: blond hair"), ("👱🏻‍♂️", "man: light skin tone, blond hair"), ("🧓", "older person"), ("🧓🏻", "older person: light skin tone"), ("👴", "old man"), ("👴🏻", "old man: light skin tone"), ("👵", "old woman"), ("👵🏻", "old woman: light skin tone"), ("🙍", "person frowning"), ("🙍🏻", "person frowning: light skin tone"), ("🙍‍♂️", "man frowning"), ("🙍🏻‍♂️", "man frowning: light skin tone"), ("🙍‍♀️", "woman frowning"), ("🙍🏻‍♀️", "woman frowning: light skin tone"), ("🙎", "person pouting"), ("🙎🏻", "person pouting: light skin tone"), ("🙎‍♂️", "man pouting"), ("🙎🏻‍♂️", "man pouting: light skin tone"), ("🙎‍♀️", "woman pouting"), ("🙎🏻‍♀️", "woman pouting: light skin tone"), ("🙅", "person gesturing NO"), ("🙅🏻", "person gesturing NO: light skin tone"), ("🙅‍♂️", "man gesturing NO"), ("🙅🏻‍♂️", "man gesturing NO: light skin tone"), ("🙅‍♀️", "woman gesturing NO"), ("🙅🏻‍♀️", "woman gesturing NO: light skin tone"), ("🙆", "person gesturing OK"), ("🙆🏻", "person gesturing OK: light skin tone"), ("🙆‍♂️", "man gesturing OK"), ("🙆🏻‍♂️", "man gesturing OK: light skin tone"), ("🙆‍♀️", "woman gesturing OK"), ("🙆🏻‍♀️", "woman gesturing OK: light skin tone"), ("💁", "person tipping hand"), ("💁🏻", "person tipping hand: light skin tone"), ("💁‍♂️", "man tipping hand"), ("💁🏻‍♂️", "man tipping hand: light skin tone"), ("💁‍♀️", "woman tipping hand"), ("💁🏻‍♀️", "woman tipping hand: light skin tone"), ("🙋", "person raising hand"), ("🙋🏻", "person raising hand: light skin tone"), ("🙋‍♂️", "man raising hand"), ("🙋🏻‍♂️", "man raising hand: light skin tone"), ("🙋‍♀️", "woman raising hand"), ("🙋🏻‍♀️", "woman raising hand: light skin tone"), ("🧏", "deaf person"), ("🧏🏻", "deaf person: light skin tone"), ("🧏‍♂️", "deaf man"), ("🧏🏻‍♂️", "deaf man: light skin tone"), ("🧏‍♀️", "deaf woman"), ("🧏🏻‍♀️", "deaf woman: light skin tone"), ("🙇", "person bowing"), ("🙇🏻", "person bowing: light skin tone"), ("🙇‍♂️", "man bowing"), ("🙇🏻‍♂️", "man bowing: light skin tone"), ("🙇‍♀️", "woman bowing"), ("🙇🏻‍♀️", "woman bowing: light skin tone"), ("🤦", "person facepalming"), ("🤦🏻", "person facepalming: light skin tone"), ("🤦‍♂️", "man facepalming"), ("🤦🏻‍♂️", "man facepalming: light skin tone"), ("🤦‍♀️", "woman facepalming"), ("🤦🏻‍♀️", "woman facepalming: light skin tone"), ("🤷", "person shrugging"), ("🤷🏻", "person shrugging: light skin tone"), ("🤷‍♂️", "man shrugging"), ("🤷🏻‍♂️", "man shrugging: light skin tone"), ("🤷‍♀️", "woman shrugging"), ("🤷🏻‍♀️", "woman shrugging: light skin tone")],
    "People Roles": [("🧑‍⚕️", "health worker"), ("🧑🏻‍⚕️", "health worker: light skin tone"), ("👨‍⚕️", "man health worker"), ("👨🏻‍⚕️", "man health worker: light skin tone"), ("👩‍⚕️", "woman health worker"), ("👩🏻‍⚕️", "woman health worker: light skin tone"), ("🧑‍🎓", "student"), ("🧑🏻‍🎓", "student: light skin tone"), ("👨‍🎓", "man student"), ("👨🏻‍🎓", "man student: light skin tone"), ("👩‍🎓", "woman student"), ("👩🏻‍🎓", "woman student: light skin tone"), ("🧑‍🏫", "teacher"), ("🧑🏻‍🏫", "teacher: light skin tone"), ("👨‍🏫", "man teacher"), ("👨🏻‍🏫", "man teacher: light skin tone"), ("👩‍🏫", "woman teacher"), ("👩🏻‍🏫", "woman teacher: light skin tone"), ("🧑‍⚖️", "judge"), ("🧑🏻‍⚖️", "judge: light skin tone"), ("👨‍⚖️", "man judge"), ("👨🏻‍⚖️", "man judge: light skin tone"), ("👩‍⚖️", "woman judge"), ("👩🏻‍⚖️", "woman judge: light skin tone"), ("🧑‍🌾", "farmer"), ("🧑🏻‍🌾", "farmer: light skin tone"), ("👨‍🌾", "man farmer"), ("👨🏻‍🌾", "man farmer: light skin tone"), ("👩‍🌾", "woman farmer"), ("👩🏻‍🌾", "woman farmer: light skin tone"), ("🧑‍🍳", "cook"), ("🧑🏻‍🍳", "cook: light skin tone"), ("👨‍🍳", "man cook"), ("👨🏻‍🍳", "man cook: light skin tone"), ("👩‍🍳", "woman cook"), ("👩🏻‍🍳", "woman cook: light skin tone"), ("🧑‍🔧", "mechanic"), ("🧑🏻‍🔧", "mechanic: light skin tone"), ("👨‍🔧", "man mechanic"), ("👨🏻‍🔧", "man mechanic: light skin tone"), ("👩‍🔧", "woman mechanic"), ("👩🏻‍🔧", "woman mechanic: light skin tone"), ("🧑‍🏭", "factory worker"), ("🧑🏻‍🏭", "factory worker: light skin tone"), ("👨‍🏭", "man factory worker"), ("👨🏻‍🏭", "man factory worker: light skin tone"), ("👩‍🏭", "woman factory worker"), ("👩🏻‍🏭", "woman factory worker: light skin tone"), ("🧑‍💼", "office worker"), ("🧑🏻‍💼", "office worker: light skin tone"), ("👨‍💼", "man office worker"), ("👨🏻‍💼", "man office worker: light skin tone"), ("👩‍💼", "woman office worker"), ("👩🏻‍💼", "woman office worker: light skin tone"), ("🧑‍🔬", "scientist"), ("🧑🏻‍🔬", "scientist: light skin tone"), ("👨‍🔬", "man scientist"), ("👨🏻‍🔬", "man scientist: light skin tone"), ("👩‍🔬", "woman scientist"), ("👩🏻‍🔬", "woman scientist: light skin tone"), ("🧑‍💻", "technologist"), ("🧑🏻‍💻", "technologist: light skin tone"), ("👨‍💻", "man technologist"), ("👨🏻‍💻", "man technologist: light skin tone"), ("👩‍💻", "woman technologist"), ("👩🏻‍💻", "woman technologist: light skin tone"), ("🧑‍🎤", "singer"), ("🧑🏻‍🎤", "singer: light skin tone"), ("👨‍🎤", "man singer"), ("👨🏻‍🎤", "man singer: light skin tone"), ("👩‍🎤", "woman singer"), ("👩🏻‍🎤", "woman singer: light skin tone"), ("🧑‍🎨", "artist"), ("🧑🏻‍🎨", "artist: light skin tone"), ("👨‍🎨", "man artist"), ("👨🏻‍🎨", "man artist: light skin tone"), ("👩‍🎨", "woman artist"), ("👩🏻‍🎨", "woman artist: light skin tone"), ("🧑‍✈️", "pilot"), ("🧑🏻‍✈️", "pilot: light skin tone"), ("👨‍✈️", "man pilot"), ("👨🏻‍✈️", "man pilot: light skin tone"), ("👩‍✈️", "woman pilot"), ("👩🏻‍✈️", "woman pilot: light skin tone"), ("🧑‍🚀", "astronaut"), ("🧑🏻‍🚀", "astronaut: light skin tone"), ("👨‍🚀", "man astronaut"), ("👨🏻‍🚀", "man astronaut: light skin tone"), ("👩‍🚀", "woman astronaut"), ("👩🏻‍🚀", "woman astronaut: light skin tone"), ("🧑‍🚒", "firefighter"), ("🧑🏻‍🚒", "firefighter: light skin tone"), ("👨‍🚒", "man firefighter"), ("👨🏻‍🚒", "man firefighter: light skin tone"), ("👩‍🚒", "woman firefighter"), ("👩🏻‍🚒", "woman firefighter: light skin tone"), ("👮", "police officer"), ("👮🏻", "police officer: light skin tone"), ("👮‍♂️", "man police officer"), ("👮🏻‍♂️", "man police officer: light skin tone"), ("👮‍♀️", "woman police officer"), ("👮🏻‍♀️", "woman police officer: light skin tone"), ("🕵️", "detective"), ("🕵🏻", "detective: light skin tone"), ("🕵️‍♂️", "man detective"), ("🕵🏻‍♂️", "man detective: light skin tone"), ("🕵️‍♀️", "woman detective"), ("🕵🏻‍♀️", "woman detective: light skin tone"), ("💂", "guard"), ("💂🏻", "guard: light skin tone"), ("💂‍♂️", "man guard"), ("💂🏻‍♂️", "man guard: light skin tone"), ("💂‍♀️", "woman guard"), ("💂🏻‍♀️", "woman guard: light skin tone"), ("🥷", "ninja"), ("🥷🏻", "ninja: light skin tone"), ("👷", "construction worker"), ("👷🏻", "construction worker: light skin tone"), ("👷‍♂️", "man construction worker"), ("👷🏻‍♂️", "man construction worker: light skin tone"), ("👷‍♀️", "woman construction worker"), ("👷🏻‍♀️", "woman construction worker: light skin tone"), ("🫅", "person with crown"), ("🫅🏻", "person with crown: light skin tone"), ("🤴", "prince"), ("🤴🏻", "prince: light skin tone"), ("👸", "princess"), ("👸🏻", "princess: light skin tone"), ("👳", "person wearing turban"), ("👳🏻", "person wearing turban: light skin tone"), ("👳‍♂️", "man wearing turban"), ("👳🏻‍♂️", "man wearing turban: light skin tone"), ("👳‍♀️", "woman wearing turban"), ("👳🏻‍♀️", "woman wearing turban: light skin tone"), ("👲", "person with skullcap"), ("👲🏻", "person with skullcap: light skin tone"), ("🧕", "woman with headscarf"), ("🧕🏻", "woman with headscarf: light skin tone"), ("🤵", "person in tuxedo"), ("🤵🏻", "person in tuxedo: light skin tone"), ("🤵‍♂️", "man in tuxedo"), ("🤵🏻‍♂️", "man in tuxedo: light skin tone"), ("🤵‍♀️", "woman in tuxedo"), ("🤵🏻‍♀️", "woman in tuxedo: light skin tone"), ("👰", "person with veil"), ("👰🏻", "person with veil: light skin tone"), ("👰‍♂️", "man with veil"), ("👰🏻‍♂️", "man with veil: light skin tone"), ("👰‍♀️", "woman with veil"), ("👰🏻‍♀️", "woman with veil: light skin tone"), ("🤰", "pregnant woman"), ("🤰🏻", "pregnant woman: light skin tone"), ("🫃", "pregnant man"), ("🫃🏻", "pregnant man: light skin tone"), ("🫄", "pregnant person"), ("🫄🏻", "pregnant person: light skin tone"), ("🤱", "breast-feeding"), ("🤱🏻", "breast-feeding: light skin tone"), ("👩‍🍼", "woman feeding baby"), ("👩🏻‍🍼", "woman feeding baby: light skin tone"), ("👨‍🍼", "man feeding baby"), ("👨🏻‍🍼", "man feeding baby: light skin tone"), ("🧑‍🍼", "person feeding baby"), ("🧑🏻‍🍼", "person feeding baby: light skin tone"), ("👼", "baby angel"), ("👼🏻", "baby angel: light skin tone"), ("🎅", "Santa Claus"), ("🎅🏻", "Santa Claus: light skin tone"), ("🤶", "Mrs. Claus"), ("🤶🏻", "Mrs. Claus: light skin tone"), ("🧑‍🎄", "Mx Claus"), ("🧑🏻‍🎄", "Mx Claus: light skin tone"), ("🦸", "superhero"), ("🦸🏻", "superhero: light skin tone"), ("🦸‍♂️", "man superhero"), ("🦸🏻‍♂️", "man superhero: light skin tone"), ("🦸‍♀️", "woman superhero"), ("🦸🏻‍♀️", "woman superhero: light skin tone"), ("🦹", "supervillain"), ("🦹🏻", "supervillain: light skin tone"), ("🦹‍♂️", "man supervillain"), ("🦹🏻‍♂️", "man supervillain: light skin tone"), ("🦹‍♀️", "woman supervillain"), ("🦹🏻‍♀️", "woman supervillain: light skin tone"), ("🧙", "mage"), ("🧙🏻", "mage: light skin tone"), ("🧙‍♂️", "man mage"), ("🧙🏻‍♂️", "man mage: light skin tone"), ("🧙‍♀️", "woman mage"), ("🧙🏻‍♀️", "woman mage: light skin tone"), ("🧚", "fairy"), ("🧚🏻", "fairy: light skin tone"), ("🧚‍♂️", "man fairy"), ("🧚🏻‍♂️", "man fairy: light skin tone"), ("🧚‍♀️", "woman fairy"), ("🧚🏻‍♀️", "woman fairy: light skin tone"), ("🧛", "vampire"), ("🧛🏻", "vampire: light skin tone"), ("🧛‍♂️", "man vampire"), ("🧛🏻‍♂️", "man vampire: light skin tone"), ("🧛‍♀️", "woman vampire"), ("🧛🏻‍♀️", "woman vampire: light skin tone"), ("🧜", "merperson"), ("🧜🏻", "merperson: light skin tone"), ("🧜‍♂️", "merman"), ("🧜🏻‍♂️", "merman: light skin tone"), ("🧜‍♀️", "mermaid"), ("🧜🏻‍♀️", "mermaid: light skin tone"), ("🧝", "elf"), ("🧝🏻", "elf: light skin tone"), ("🧝‍♂️", "man elf"), ("🧝🏻‍♂️", "man elf: light skin tone"), ("🧝‍♀️", "woman elf"), ("🧝🏻‍♀️", "woman elf: light skin tone"), ("🧞", "genie"), ("🧞‍♂️", "man genie"), ("🧞‍♀️", "woman genie"), ("🧟", "zombie"), ("🧟‍♂️", "man zombie"), ("🧟‍♀️", "woman zombie"), ("🧌", "troll"), ("🫈", "hairy creature"), ("💆", "person getting massage"), ("💆🏻", "person getting massage: light skin tone"), ("💆‍♂️", "man getting massage"), ("💆🏻‍♂️", "man getting massage: light skin tone"), ("💆‍♀️", "woman getting massage"), ("💆🏻‍♀️", "woman getting massage: light skin tone"), ("💇", "person getting haircut"), ("💇🏻", "person getting haircut: light skin tone"), ("💇‍♂️", "man getting haircut"), ("💇🏻‍♂️", "man getting haircut: light skin tone"), ("💇‍♀️", "woman getting haircut"), ("💇🏻‍♀️", "woman getting haircut: light skin tone"), ("🚶", "person walking"), ("🚶🏻", "person walking: light skin tone"), ("🚶‍♂️", "man walking"), ("🚶🏻‍♂️", "man walking: light skin tone"), ("🚶‍♀️", "woman walking"), ("🚶🏻‍♀️", "woman walking: light skin tone"), ("🚶‍➡️", "person walking facing right"), ("🚶🏻‍➡️", "person walking facing right: light skin tone"), ("🚶‍♀️‍➡️", "woman walking facing right"), ("🚶🏻‍♀️‍➡️", "woman walking facing right: light skin tone"), ("🚶‍♂️‍➡️", "man walking facing right"), ("🚶🏻‍♂️‍➡️", "man walking facing right: light skin tone"), ("🧍", "person standing"), ("🧍🏻", "person standing: light skin tone"), ("🧍‍♂️", "man standing"), ("🧍🏻‍♂️", "man standing: light skin tone"), ("🧍‍♀️", "woman standing"), ("🧍🏻‍♀️", "woman standing: light skin tone"), ("🧎", "person kneeling"), ("🧎🏻", "person kneeling: light skin tone"), ("🧎‍♂️", "man kneeling"), ("🧎🏻‍♂️", "man kneeling: light skin tone"), ("🧎‍♀️", "woman kneeling"), ("🧎🏻‍♀️", "woman kneeling: light skin tone"), ("🧎‍➡️", "person kneeling facing right"), ("🧎🏻‍➡️", "person kneeling facing right: light skin tone"), ("🧎‍♀️‍➡️", "woman kneeling facing right"), ("🧎🏻‍♀️‍➡️", "woman kneeling facing right: light skin tone"), ("🧎‍♂️‍➡️", "man kneeling facing right"), ("🧎🏻‍♂️‍➡️", "man kneeling facing right: light skin tone"), ("🧑‍🦯", "person with white cane"), ("🧑🏻‍🦯", "person with white cane: light skin tone"), ("🧑‍🦯‍➡️", "person with white cane facing right"), ("🧑🏻‍🦯‍➡️", "person with white cane facing right: light skin tone"), ("👨‍🦯", "man with white cane"), ("👨🏻‍🦯", "man with white cane: light skin tone"), ("👨‍🦯‍➡️", "man with white cane facing right"), ("👨🏻‍🦯‍➡️", "man with white cane facing right: light skin tone"), ("👩‍🦯", "woman with white cane"), ("👩🏻‍🦯", "woman with white cane: light skin tone"), ("👩‍🦯‍➡️", "woman with white cane facing right"), ("👩🏻‍🦯‍➡️", "woman with white cane facing right: light skin tone"), ("🧑‍🦼", "person in motorized wheelchair"), ("🧑🏻‍🦼", "person in motorized wheelchair: light skin tone"), ("🧑‍🦼‍➡️", "person in motorized wheelchair facing right"), ("🧑🏻‍🦼‍➡️", "person in motorized wheelchair facing right: light skin tone"), ("👨‍🦼", "man in motorized wheelchair"), ("👨🏻‍🦼", "man in motorized wheelchair: light skin tone"), ("👨‍🦼‍➡️", "man in motorized wheelchair facing right"), ("👨🏻‍🦼‍➡️", "man in motorized wheelchair facing right: light skin tone"), ("👩‍🦼", "woman in motorized wheelchair"), ("👩🏻‍🦼", "woman in motorized wheelchair: light skin tone"), ("👩‍🦼‍➡️", "woman in motorized wheelchair facing right"), ("👩🏻‍🦼‍➡️", "woman in motorized wheelchair facing right: light skin tone"), ("🧑‍🦽", "person in manual wheelchair"), ("🧑🏻‍🦽", "person in manual wheelchair: light skin tone"), ("🧑‍🦽‍➡️", "person in manual wheelchair facing right"), ("🧑🏻‍🦽‍➡️", "person in manual wheelchair facing right: light skin tone"), ("👨‍🦽", "man in manual wheelchair"), ("👨🏻‍🦽", "man in manual wheelchair: light skin tone"), ("👨‍🦽‍➡️", "man in manual wheelchair facing right"), ("👨🏻‍🦽‍➡️", "man in manual wheelchair facing right: light skin tone"), ("👩‍🦽", "woman in manual wheelchair"), ("👩🏻‍🦽", "woman in manual wheelchair: light skin tone"), ("👩‍🦽‍➡️", "woman in manual wheelchair facing right"), ("👩🏻‍🦽‍➡️", "woman in manual wheelchair facing right: light skin tone")],
    "People Activities": [("🏃", "person running"), ("🏃🏻", "person running: light skin tone"), ("🏃‍♂️", "man running"), ("🏃🏻‍♂️", "man running: light skin tone"), ("🏃‍♀️", "woman running"), ("🏃🏻‍♀️", "woman running: light skin tone"), ("🏃‍➡️", "person running facing right"), ("🏃🏻‍➡️", "person running facing right: light skin tone"), ("🏃‍♀️‍➡️", "woman running facing right"), ("🏃🏻‍♀️‍➡️", "woman running facing right: light skin tone"), ("🏃‍♂️‍➡️", "man running facing right"), ("🏃🏻‍♂️‍➡️", "man running facing right: light skin tone"), ("🧑‍🩰", "ballet dancer"), ("🧑🏻‍🩰", "ballet dancer: light skin tone"), ("💃", "woman dancing"), ("💃🏻", "woman dancing: light skin tone"), ("🕺", "man dancing"), ("🕺🏻", "man dancing: light skin tone"), ("🕴️", "person in suit levitating"), ("🕴🏻", "person in suit levitating: light skin tone"), ("👯", "people with bunny ears"), ("👯🏻", "people with bunny ears: light skin tone"), ("👯‍♂️", "men with bunny ears"), ("👯🏻‍♂️", "men with bunny ears: light skin tone"), ("👯‍♀️", "women with bunny ears"), ("👯🏻‍♀️", "women with bunny ears: light skin tone"), ("🧖", "person in steamy room"), ("🧖🏻", "person in steamy room: light skin tone"), ("🧖‍♂️", "man in steamy room"), ("🧖🏻‍♂️", "man in steamy room: light skin tone"), ("🧖‍♀️", "woman in steamy room"), ("🧖🏻‍♀️", "woman in steamy room: light skin tone"), ("🧗", "person climbing"), ("🧗🏻", "person climbing: light skin tone"), ("🧗‍♂️", "man climbing"), ("🧗🏻‍♂️", "man climbing: light skin tone"), ("🧗‍♀️", "woman climbing"), ("🧗🏻‍♀️", "woman climbing: light skin tone"), ("🤺", "person fencing"), ("🏇", "horse racing"), ("🏇🏻", "horse racing: light skin tone"), ("⛷️", "skier"), ("🏂", "snowboarder"), ("🏂🏻", "snowboarder: light skin tone"), ("🏌️", "person golfing"), ("🏌🏻", "person golfing: light skin tone"), ("🏌️‍♂️", "man golfing"), ("🏌🏻‍♂️", "man golfing: light skin tone"), ("🏌️‍♀️", "woman golfing"), ("🏌🏻‍♀️", "woman golfing: light skin tone"), ("🏄", "person surfing"), ("🏄🏻", "person surfing: light skin tone"), ("🏄‍♂️", "man surfing"), ("🏄🏻‍♂️", "man surfing: light skin tone"), ("🏄‍♀️", "woman surfing"), ("🏄🏻‍♀️", "woman surfing: light skin tone"), ("🚣", "person rowing boat"), ("🚣🏻", "person rowing boat: light skin tone"), ("🚣‍♂️", "man rowing boat"), ("🚣🏻‍♂️", "man rowing boat: light skin tone"), ("🚣‍♀️", "woman rowing boat"), ("🚣🏻‍♀️", "woman rowing boat: light skin tone"), ("🏊", "person swimming"), ("🏊🏻", "person swimming: light skin tone"), ("🏊‍♂️", "man swimming"), ("🏊🏻‍♂️", "man swimming: light skin tone"), ("🏊‍♀️", "woman swimming"), ("🏊🏻‍♀️", "woman swimming: light skin tone"), ("⛹️", "person bouncing ball"), ("⛹🏻", "person bouncing ball: light skin tone"), ("⛹️‍♂️", "man bouncing ball"), ("⛹🏻‍♂️", "man bouncing ball: light skin tone"), ("⛹️‍♀️", "woman bouncing ball"), ("⛹🏻‍♀️", "woman bouncing ball: light skin tone"), ("🏋️", "person lifting weights"), ("🏋🏻", "person lifting weights: light skin tone"), ("🏋️‍♂️", "man lifting weights"), ("🏋🏻‍♂️", "man lifting weights: light skin tone"), ("🏋️‍♀️", "woman lifting weights"), ("🏋🏻‍♀️", "woman lifting weights: light skin tone"), ("🚴", "person biking"), ("🚴🏻", "person biking: light skin tone"), ("🚴‍♂️", "man biking"), ("🚴🏻‍♂️", "man biking: light skin tone"), ("🚴‍♀️", "woman biking"), ("🚴🏻‍♀️", "woman biking: light skin tone"), ("🚵", "person mountain biking"), ("🚵🏻", "person mountain biking: light skin tone"), ("🚵‍♂️", "man mountain biking"), ("🚵🏻‍♂️", "man mountain biking: light skin tone"), ("🚵‍♀️", "woman mountain biking"), ("🚵🏻‍♀️", "woman mountain biking: light skin tone"), ("🤸", "person cartwheeling"), ("🤸🏻", "person cartwheeling: light skin tone"), ("🤸‍♂️", "man cartwheeling"), ("🤸🏻‍♂️", "man cartwheeling: light skin tone"), ("🤸‍♀️", "woman cartwheeling"), ("🤸🏻‍♀️", "woman cartwheeling: light skin tone"), ("🤼", "people wrestling"), ("🤼🏻", "people wrestling: light skin tone"), ("🤼‍♂️", "men wrestling"), ("🤼🏻‍♂️", "men wrestling: light skin tone"), ("🤼‍♀️", "women wrestling"), ("🤼🏻‍♀️", "women wrestling: light skin tone"), ("🤽", "person playing water polo"), ("🤽🏻", "person playing water polo: light skin tone"), ("🤽‍♂️", "man playing water polo"), ("🤽🏻‍♂️", "man playing water polo: light skin tone"), ("🤽‍♀️", "woman playing water polo"), ("🤽🏻‍♀️", "woman playing water polo: light skin tone"), ("🤾", "person playing handball"), ("🤾🏻", "person playing handball: light skin tone"), ("🤾‍♂️", "man playing handball"), ("🤾🏻‍♂️", "man playing handball: light skin tone"), ("🤾‍♀️", "woman playing handball"), ("🤾🏻‍♀️", "woman playing handball: light skin tone"), ("🤹", "person juggling"), ("🤹🏻", "person juggling: light skin tone"), ("🤹‍♂️", "man juggling"), ("🤹🏻‍♂️", "man juggling: light skin tone"), ("🤹‍♀️", "woman juggling"), ("🤹🏻‍♀️", "woman juggling: light skin tone"), ("🧘", "person in lotus position"), ("🧘🏻", "person in lotus position: light skin tone"), ("🧘‍♂️", "man in lotus position"), ("🧘🏻‍♂️", "man in lotus position: light skin tone"), ("🧘‍♀️", "woman in lotus position"), ("🧘🏻‍♀️", "woman in lotus position: light skin tone"), ("🛀", "person taking bath"), ("🛀🏻", "person taking bath: light skin tone"), ("🛌", "person in bed"), ("🛌🏻", "person in bed: light skin tone")],
    "Love & Family": [("🧑‍🤝‍🧑", "people holding hands"), ("🧑🏻‍🤝‍🧑🏻", "people holding hands: light skin tone"), ("👭", "women holding hands"), ("👭🏻", "women holding hands: light skin tone"), ("👫", "woman and man holding hands"), ("👫🏻", "woman and man holding hands: light skin tone"), ("👬", "men holding hands"), ("👬🏻", "men holding hands: light skin tone"), ("💏", "kiss"), ("💏🏻", "kiss: light skin tone"), ("👩‍❤️‍💋‍👨", "kiss: woman, man"), ("👩🏻‍❤️‍💋‍👨🏻", "kiss: woman, man, light skin tone"), ("👨‍❤️‍💋‍👨", "kiss: man, man"), ("👨🏻‍❤️‍💋‍👨🏻", "kiss: man, man, light skin tone"), ("👩‍❤️‍💋‍👩", "kiss: woman, woman"), ("👩🏻‍❤️‍💋‍👩🏻", "kiss: woman, woman, light skin tone"), ("💑", "couple with heart"), ("💑🏻", "couple with heart: light skin tone"), ("👩‍❤️‍👨", "couple with heart: woman, man"), ("👩🏻‍❤️‍👨🏻", "couple with heart: woman, man, light skin tone"), ("👨‍❤️‍👨", "couple with heart: man, man"), ("👨🏻‍❤️‍👨🏻", "couple with heart: man, man, light skin tone"), ("👩‍❤️‍👩", "couple with heart: woman, woman"), ("👩🏻‍❤️‍👩🏻", "couple with heart: woman, woman, light skin tone"), ("👨‍👩‍👦", "family: man, woman, boy"), ("👨‍👩‍👧", "family: man, woman, girl"), ("👨‍👩‍👧‍👦", "family: man, woman, girl, boy"), ("👨‍👩‍👦‍👦", "family: man, woman, boy, boy"), ("👨‍👩‍👧‍👧", "family: man, woman, girl, girl"), ("👨‍👨‍👦", "family: man, man, boy"), ("👨‍👨‍👧", "family: man, man, girl"), ("👨‍👨‍👧‍👦", "family: man, man, girl, boy"), ("👨‍👨‍👦‍👦", "family: man, man, boy, boy"), ("👨‍👨‍👧‍👧", "family: man, man, girl, girl"), ("👩‍👩‍👦", "family: woman, woman, boy"), ("👩‍👩‍👧", "family: woman, woman, girl"), ("👩‍👩‍👧‍👦", "family: woman, woman, girl, boy"), ("👩‍👩‍👦‍👦", "family: woman, woman, boy, boy"), ("👩‍👩‍👧‍👧", "family: woman, woman, girl, girl"), ("👨‍👦", "family: man, boy"), ("👨‍👦‍👦", "family: man, boy, boy"), ("👨‍👧", "family: man, girl"), ("👨‍👧‍👦", "family: man, girl, boy"), ("👨‍👧‍👧", "family: man, girl, girl"), ("👩‍👦", "family: woman, boy"), ("👩‍👦‍👦", "family: woman, boy, boy"), ("👩‍👧", "family: woman, girl"), ("👩‍👧‍👦", "family: woman, girl, boy"), ("👩‍👧‍👧", "family: woman, girl, girl"), ("🗣️", "speaking head"), ("👤", "bust in silhouette"), ("👥", "busts in silhouette"), ("🫂", "people hugging"), ("👪", "family"), ("🧑‍🧑‍🧒", "family: adult, adult, child"), ("🧑‍🧑‍🧒‍🧒", "family: adult, adult, child, child"), ("🧑‍🧒", "family: adult, child"), ("🧑‍🧒‍🧒", "family: adult, child, child"), ("👣", "footprints"), ("🫆", "fingerprint")],
    "Animals": [("🐵", "monkey face"), ("🐒", "monkey"), ("🦍", "gorilla"), ("🦧", "orangutan"), ("🐶", "dog face"), ("🐕", "dog"), ("🦮", "guide dog"), ("🐕‍🦺", "service dog"), ("🐩", "poodle"), ("🐺", "wolf"), ("🦊", "fox"), ("🦝", "raccoon"), ("🐱", "cat face"), ("🐈", "cat"), ("🐈‍⬛", "black cat"), ("🦁", "lion"), ("🐯", "tiger face"), ("🐅", "tiger"), ("🐆", "leopard"), ("🐴", "horse face"), ("🫎", "moose"), ("🫏", "donkey"), ("🐎", "horse"), ("🦄", "unicorn"), ("🦓", "zebra"), ("🦌", "deer"), ("🦬", "bison"), ("🐮", "cow face"), ("🐂", "ox"), ("🐃", "water buffalo"), ("🐄", "cow"), ("🐷", "pig face"), ("🐖", "pig"), ("🐗", "boar"), ("🐽", "pig nose"), ("🐏", "ram"), ("🐑", "ewe"), ("🐐", "goat"), ("🐪", "camel"), ("🐫", "two-hump camel"), ("🦙", "llama"), ("🦒", "giraffe"), ("🐘", "elephant"), ("🦣", "mammoth"), ("🦏", "rhinoceros"), ("🦛", "hippopotamus"), ("🐭", "mouse face"), ("🐁", "mouse"), ("🐀", "rat"), ("🐹", "hamster"), ("🐰", "rabbit face"), ("🐇", "rabbit"), ("🐿️", "chipmunk"), ("🦫", "beaver"), ("🦔", "hedgehog"), ("🦇", "bat"), ("🐻", "bear"), ("🐻‍❄️", "polar bear"), ("🐨", "koala"), ("🐼", "panda"), ("🦥", "sloth"), ("🦦", "otter"), ("🦨", "skunk"), ("🦘", "kangaroo"), ("🦡", "badger"), ("🐾", "paw prints"), ("🦃", "turkey"), ("🐔", "chicken"), ("🐓", "rooster"), ("🐣", "hatching chick"), ("🐤", "baby chick"), ("🐥", "front-facing baby chick"), ("🐦", "bird"), ("🐧", "penguin"), ("🕊️", "dove"), ("🦅", "eagle"), ("🦆", "duck"), ("🦢", "swan"), ("🦉", "owl"), ("🦤", "dodo"), ("🪶", "feather"), ("🦩", "flamingo"), ("🦚", "peacock"), ("🦜", "parrot"), ("🪽", "wing"), ("🐦‍⬛", "black bird"), ("🪿", "goose"), ("🐦‍🔥", "phoenix"), ("🐸", "frog"), ("🐊", "crocodile"), ("🐢", "turtle"), ("🦎", "lizard"), ("🐍", "snake"), ("🐲", "dragon face"), ("🐉", "dragon"), ("🦕", "sauropod"), ("🦖", "T-Rex"), ("🐳", "spouting whale"), ("🐋", "whale"), ("🐬", "dolphin"), ("🫍", "orca"), ("🦭", "seal"), ("🐟", "fish"), ("🐠", "tropical fish"), ("🐡", "blowfish"), ("🦈", "shark"), ("🐙", "octopus"), ("🐚", "spiral shell"), ("🪸", "coral"), ("🪼", "jellyfish"), ("🦀", "crab"), ("🦞", "lobster"), ("🦐", "shrimp"), ("🦑", "squid"), ("🦪", "oyster"), ("🐌", "snail"), ("🦋", "butterfly"), ("🐛", "bug"), ("🐜", "ant"), ("🐝", "honeybee"), ("🪲", "beetle"), ("🐞", "lady beetle"), ("🦗", "cricket"), ("🪳", "cockroach"), ("🕷️", "spider"), ("🕸️", "spider web"), ("🦂", "scorpion"), ("🦟", "mosquito"), ("🪰", "fly"), ("🪱", "worm"), ("🦠", "microbe")],
    "Plants": [("💐", "bouquet"), ("🌸", "cherry blossom"), ("💮", "white flower"), ("🪷", "lotus"), ("🏵️", "rosette"), ("🌹", "rose"), ("🥀", "wilted flower"), ("🌺", "hibiscus"), ("🌻", "sunflower"), ("🌼", "blossom"), ("🌷", "tulip"), ("🪻", "hyacinth"), ("🌱", "seedling"), ("🪴", "potted plant"), ("🌲", "evergreen tree"), ("🌳", "deciduous tree"), ("🌴", "palm tree"), ("🌵", "cactus"), ("🌾", "sheaf of rice"), ("🌿", "herb"), ("☘️", "shamrock"), ("🍀", "four leaf clover"), ("🍁", "maple leaf"), ("🍂", "fallen leaf"), ("🍃", "leaf fluttering in wind"), ("🪹", "empty nest"), ("🪺", "nest with eggs"), ("🍄", "mushroom"), ("🪾", "leafless tree")],
    "Food & Dining": [("🍇", "grapes"), ("🍈", "melon"), ("🍉", "watermelon"), ("🍊", "tangerine"), ("🍋", "lemon"), ("🍋‍🟩", "lime"), ("🍌", "banana"), ("🍍", "pineapple"), ("🥭", "mango"), ("🍎", "red apple"), ("🍏", "green apple"), ("🍐", "pear"), ("🍑", "peach"), ("🍒", "cherries"), ("🍓", "strawberry"), ("🫐", "blueberries"), ("🥝", "kiwi fruit"), ("🍅", "tomato"), ("🫒", "olive"), ("🥥", "coconut"), ("🥑", "avocado"), ("🍆", "eggplant"), ("🥔", "potato"), ("🥕", "carrot"), ("🌽", "ear of corn"), ("🌶️", "hot pepper"), ("🫑", "bell pepper"), ("🥒", "cucumber"), ("🥬", "leafy green"), ("🥦", "broccoli"), ("🧄", "garlic"), ("🧅", "onion"), ("🥜", "peanuts"), ("🫘", "beans"), ("🌰", "chestnut"), ("🫚", "ginger root"), ("🫛", "pea pod"), ("🍄‍🟫", "brown mushroom"), ("🫜", "root vegetable"), ("🍞", "bread"), ("🥐", "croissant"), ("🥖", "baguette bread"), ("🫓", "flatbread"), ("🥨", "pretzel"), ("🥯", "bagel"), ("🥞", "pancakes"), ("🧇", "waffle"), ("🧀", "cheese wedge"), ("🍖", "meat on bone"), ("🍗", "poultry leg"), ("🥩", "cut of meat"), ("🥓", "bacon"), ("🍔", "hamburger"), ("🍟", "french fries"), ("🍕", "pizza"), ("🌭", "hot dog"), ("🥪", "sandwich"), ("🌮", "taco"), ("🌯", "burrito"), ("🫔", "tamale"), ("🥙", "stuffed flatbread"), ("🧆", "falafel"), ("🥚", "egg"), ("🍳", "cooking"), ("🥘", "shallow pan of food"), ("🍲", "pot of food"), ("🫕", "fondue"), ("🥣", "bowl with spoon"), ("🥗", "green salad"), ("🍿", "popcorn"), ("🧈", "butter"), ("🧂", "salt"), ("🥫", "canned food"), ("🍱", "bento box"), ("🍘", "rice cracker"), ("🍙", "rice ball"), ("🍚", "cooked rice"), ("🍛", "curry rice"), ("🍜", "steaming bowl"), ("🍝", "spaghetti"), ("🍠", "roasted sweet potato"), ("🍢", "oden"), ("🍣", "sushi"), ("🍤", "fried shrimp"), ("🍥", "fish cake with swirl"), ("🥮", "moon cake"), ("🍡", "dango"), ("🥟", "dumpling"), ("🥠", "fortune cookie"), ("🥡", "takeout box"), ("🍦", "soft ice cream"), ("🍧", "shaved ice"), ("🍨", "ice cream"), ("🍩", "doughnut"), ("🍪", "cookie"), ("🎂", "birthday cake"), ("🍰", "shortcake"), ("🧁", "cupcake"), ("🥧", "pie"), ("🍫", "chocolate bar"), ("🍬", "candy"), ("🍭", "lollipop"), ("🍮", "custard"), ("🍯", "honey pot"), ("🍼", "baby bottle"), ("🥛", "glass of milk"), ("☕", "hot beverage"), ("🫖", "teapot"), ("🍵", "teacup without handle"), ("🍶", "sake"), ("🍾", "bottle with popping cork"), ("🍷", "wine glass"), ("🍸", "cocktail glass"), ("🍹", "tropical drink"), ("🍺", "beer mug"), ("🍻", "clinking beer mugs"), ("🥂", "clinking glasses"), ("🥃", "tumbler glass"), ("🫗", "pouring liquid"), ("🥤", "cup with straw"), ("🧋", "bubble tea"), ("🧃", "beverage box"), ("🧉", "mate"), ("🧊", "ice"), ("🥢", "chopsticks"), ("🍽️", "fork and knife with plate"), ("🍴", "fork and knife"), ("🥄", "spoon"), ("🔪", "kitchen knife"), ("🫙", "jar"), ("🏺", "amphora")],
    "Places & Buildings": [("🌍", "globe showing Europe-Africa"), ("🌎", "globe showing Americas"), ("🌏", "globe showing Asia-Australia"), ("🌐", "globe with meridians"), ("🗺️", "world map"), ("🗾", "map of Japan"), ("🧭", "compass"), ("🏔️", "snow-capped mountain"), ("⛰️", "mountain"), ("🛘", "landslide"), ("🌋", "volcano"), ("🗻", "mount fuji"), ("🏕️", "camping"), ("🏖️", "beach with umbrella"), ("🏜️", "desert"), ("🏝️", "desert island"), ("🏞️", "national park"), ("🏟️", "stadium"), ("🏛️", "classical building"), ("🏗️", "building construction"), ("🧱", "brick"), ("🪨", "rock"), ("🪵", "wood"), ("🛖", "hut"), ("🏘️", "houses"), ("🏚️", "derelict house"), ("🏠", "house"), ("🏡", "house with garden"), ("🏢", "office building"), ("🏣", "Japanese post office"), ("🏤", "post office"), ("🏥", "hospital"), ("🏦", "bank"), ("🏨", "hotel"), ("🏩", "love hotel"), ("🏪", "convenience store"), ("🏫", "school"), ("🏬", "department store"), ("🏭", "factory"), ("🏯", "Japanese castle"), ("🏰", "castle"), ("💒", "wedding"), ("🗼", "Tokyo tower"), ("🗽", "Statue of Liberty"), ("⛪", "church"), ("🕌", "mosque"), ("🛕", "hindu temple"), ("🕍", "synagogue"), ("⛩️", "shinto shrine"), ("🕋", "kaaba"), ("⛲", "fountain"), ("⛺", "tent"), ("🌁", "foggy"), ("🌃", "night with stars"), ("🏙️", "cityscape"), ("🌄", "sunrise over mountains"), ("🌅", "sunrise"), ("🌆", "cityscape at dusk"), ("🌇", "sunset"), ("🌉", "bridge at night"), ("♨️", "hot springs"), ("🎠", "carousel horse"), ("🛝", "playground slide"), ("🎡", "ferris wheel"), ("🎢", "roller coaster"), ("💈", "barber pole"), ("🎪", "circus tent")],
    "Travel": [("🚂", "locomotive"), ("🚃", "railway car"), ("🚄", "high-speed train"), ("🚅", "bullet train"), ("🚆", "train"), ("🚇", "metro"), ("🚈", "light rail"), ("🚉", "station"), ("🚊", "tram"), ("🚝", "monorail"), ("🚞", "mountain railway"), ("🚋", "tram car"), ("🚌", "bus"), ("🚍", "oncoming bus"), ("🚎", "trolleybus"), ("🚐", "minibus"), ("🚑", "ambulance"), ("🚒", "fire engine"), ("🚓", "police car"), ("🚔", "oncoming police car"), ("🚕", "taxi"), ("🚖", "oncoming taxi"), ("🚗", "automobile"), ("🚘", "oncoming automobile"), ("🚙", "sport utility vehicle"), ("🛻", "pickup truck"), ("🚚", "delivery truck"), ("🚛", "articulated lorry"), ("🚜", "tractor"), ("🏎️", "racing car"), ("🏍️", "motorcycle"), ("🛵", "motor scooter"), ("🦽", "manual wheelchair"), ("🦼", "motorized wheelchair"), ("🛺", "auto rickshaw"), ("🚲", "bicycle"), ("🛴", "kick scooter"), ("🛹", "skateboard"), ("🛼", "roller skate"), ("🚏", "bus stop"), ("🛣️", "motorway"), ("🛤️", "railway track"), ("🛢️", "oil drum"), ("⛽", "fuel pump"), ("🛞", "wheel"), ("🚨", "police car light"), ("🚥", "horizontal traffic light"), ("🚦", "vertical traffic light"), ("🛑", "stop sign"), ("🚧", "construction"), ("⚓", "anchor"), ("🛟", "ring buoy"), ("⛵", "sailboat"), ("🛶", "canoe"), ("🚤", "speedboat"), ("🛳️", "passenger ship"), ("⛴️", "ferry"), ("🛥️", "motor boat"), ("🚢", "ship"), ("✈️", "airplane"), ("🛩️", "small airplane"), ("🛫", "airplane departure"), ("🛬", "airplane arrival"), ("🪂", "parachute"), ("💺", "seat"), ("🚁", "helicopter"), ("🚟", "suspension railway"), ("🚠", "mountain cableway"), ("🚡", "aerial tramway"), ("🛰️", "satellite"), ("🚀", "rocket"), ("🛸", "flying saucer"), ("🛎️", "bellhop bell"), ("🧳", "luggage")],
    "Time": [("⌛", "hourglass done"), ("⏳", "hourglass not done"), ("⌚", "watch"), ("⏰", "alarm clock"), ("⏱️", "stopwatch"), ("⏲️", "timer clock"), ("🕰️", "mantelpiece clock"), ("🕛", "twelve o’clock"), ("🕧", "twelve-thirty"), ("🕐", "one o’clock"), ("🕜", "one-thirty"), ("🕑", "two o’clock"), ("🕝", "two-thirty"), ("🕒", "three o’clock"), ("🕞", "three-thirty"), ("🕓", "four o’clock"), ("🕟", "four-thirty"), ("🕔", "five o’clock"), ("🕠", "five-thirty"), ("🕕", "six o’clock"), ("🕡", "six-thirty"), ("🕖", "seven o’clock"), ("🕢", "seven-thirty"), ("🕗", "eight o’clock"), ("🕣", "eight-thirty"), ("🕘", "nine o’clock"), ("🕤", "nine-thirty"), ("🕙", "ten o’clock"), ("🕥", "ten-thirty"), ("🕚", "eleven o’clock"), ("🕦", "eleven-thirty")],
    "Sky & Weather": [("🌑", "new moon"), ("🌒", "waxing crescent moon"), ("🌓", "first quarter moon"), ("🌔", "waxing gibbous moon"), ("🌕", "full moon"), ("🌖", "waning gibbous moon"), ("🌗", "last quarter moon"), ("🌘", "waning crescent moon"), ("🌙", "crescent moon"), ("🌚", "new moon face"), ("🌛", "first quarter moon face"), ("🌜", "last quarter moon face"), ("🌡️", "thermometer"), ("☀️", "sun"), ("🌝", "full moon face"), ("🌞", "sun with face"), ("🪐", "ringed planet"), ("⭐", "star"), ("🌟", "glowing star"), ("🌠", "shooting star"), ("🌌", "milky way"), ("☁️", "cloud"), ("⛅", "sun behind cloud"), ("⛈️", "cloud with lightning and rain"), ("🌤️", "sun behind small cloud"), ("🌥️", "sun behind large cloud"), ("🌦️", "sun behind rain cloud"), ("🌧️", "cloud with rain"), ("🌨️", "cloud with snow"), ("🌩️", "cloud with lightning"), ("🌪️", "tornado"), ("🌫️", "fog"), ("🌬️", "wind face"), ("🌀", "cyclone"), ("🌈", "rainbow"), ("🌂", "closed umbrella"), ("☂️", "umbrella"), ("☔", "umbrella with rain drops"), ("⛱️", "umbrella on ground"), ("⚡", "high voltage"), ("❄️", "snowflake"), ("☃️", "snowman"), ("⛄", "snowman without snow"), ("☄️", "comet"), ("🔥", "fire"), ("💧", "droplet"), ("🌊", "water wave")],
    "Events": [("🎃", "jack-o-lantern"), ("🎄", "Christmas tree"), ("🎆", "fireworks"), ("🎇", "sparkler"), ("🧨", "firecracker"), ("✨", "sparkles"), ("🎈", "balloon"), ("🎉", "party popper"), ("🎊", "confetti ball"), ("🎋", "tanabata tree"), ("🎍", "pine decoration"), ("🎎", "Japanese dolls"), ("🎏", "carp streamer"), ("🎐", "wind chime"), ("🎑", "moon viewing ceremony"), ("🧧", "red envelope"), ("🎀", "ribbon"), ("🎁", "wrapped gift"), ("🎗️", "reminder ribbon"), ("🎟️", "admission tickets"), ("🎫", "ticket")],
    "Awards & Sports": [("🎖️", "military medal"), ("🏆", "trophy"), ("🏅", "sports medal"), ("🥇", "1st place medal"), ("🥈", "2nd place medal"), ("🥉", "3rd place medal"), ("⚽", "soccer ball"), ("⚾", "baseball"), ("🥎", "softball"), ("🏀", "basketball"), ("🏐", "volleyball"), ("🏈", "american football"), ("🏉", "rugby football"), ("🎾", "tennis"), ("🥏", "flying disc"), ("🎳", "bowling"), ("🏏", "cricket game"), ("🏑", "field hockey"), ("🏒", "ice hockey"), ("🥍", "lacrosse"), ("🏓", "ping pong"), ("🏸", "badminton"), ("🥊", "boxing glove"), ("🥋", "martial arts uniform"), ("🥅", "goal net"), ("⛳", "flag in hole"), ("⛸️", "ice skate"), ("🎣", "fishing pole"), ("🤿", "diving mask"), ("🎽", "running shirt"), ("🎿", "skis"), ("🛷", "sled"), ("🥌", "curling stone")],
    "Objects": [("🎯", "bullseye"), ("🪀", "yo-yo"), ("🪁", "kite"), ("🔫", "water pistol"), ("🎱", "pool 8 ball"), ("🔮", "crystal ball"), ("🪄", "magic wand"), ("🎮", "video game"), ("🕹️", "joystick"), ("🎰", "slot machine"), ("🎲", "game die"), ("🧩", "puzzle piece"), ("🧸", "teddy bear"), ("🪅", "piñata"), ("🪩", "mirror ball"), ("🪆", "nesting dolls"), ("♠️", "spade suit"), ("♥️", "heart suit"), ("♦️", "diamond suit"), ("♣️", "club suit"), ("♟️", "chess pawn"), ("🃏", "joker"), ("🀄", "mahjong red dragon"), ("🎴", "flower playing cards"), ("🎭", "performing arts"), ("🖼️", "framed picture"), ("🎨", "artist palette"), ("🧵", "thread"), ("🪡", "sewing needle"), ("🧶", "yarn"), ("🪢", "knot"), ("👓", "glasses"), ("🕶️", "sunglasses"), ("🥽", "goggles"), ("🥼", "lab coat"), ("🦺", "safety vest"), ("👔", "necktie"), ("👕", "t-shirt"), ("👖", "jeans"), ("🧣", "scarf"), ("🧤", "gloves"), ("🧥", "coat"), ("🧦", "socks"), ("👗", "dress"), ("👘", "kimono"), ("🥻", "sari"), ("🩱", "one-piece swimsuit"), ("🩲", "briefs"), ("🩳", "shorts"), ("👙", "bikini"), ("👚", "woman’s clothes"), ("🪭", "folding hand fan"), ("👛", "purse"), ("👜", "handbag"), ("👝", "clutch bag"), ("🛍️", "shopping bags"), ("🎒", "backpack"), ("🩴", "thong sandal"), ("👞", "man’s shoe"), ("👟", "running shoe"), ("🥾", "hiking boot"), ("🥿", "flat shoe"), ("👠", "high-heeled shoe"), ("👡", "woman’s sandal"), ("🩰", "ballet shoes"), ("👢", "woman’s boot"), ("🪮", "hair pick"), ("👑", "crown"), ("👒", "woman’s hat"), ("🎩", "top hat"), ("🎓", "graduation cap"), ("🧢", "billed cap"), ("🪖", "military helmet"), ("⛑️", "rescue worker’s helmet"), ("📿", "prayer beads"), ("💄", "lipstick"), ("💍", "ring"), ("💎", "gem stone"), ("🔇", "muted speaker"), ("🔈", "speaker low volume"), ("🔉", "speaker medium volume"), ("🔊", "speaker high volume"), ("📢", "loudspeaker"), ("📣", "megaphone"), ("📯", "postal horn"), ("🔔", "bell"), ("🔕", "bell with slash"), ("🎼", "musical score"), ("🎵", "musical note"), ("🎶", "musical notes"), ("🎙️", "studio microphone"), ("🎚️", "level slider"), ("🎛️", "control knobs"), ("🎤", "microphone"), ("🎧", "headphone"), ("📻", "radio"), ("🎷", "saxophone"), ("🎺", "trumpet"), ("🪊", "trombone"), ("🪗", "accordion"), ("🎸", "guitar"), ("🎹", "musical keyboard"), ("🎻", "violin"), ("🪕", "banjo"), ("🥁", "drum"), ("🪘", "long drum"), ("🪇", "maracas"), ("🪈", "flute"), ("🪉", "harp"), ("📱", "mobile phone"), ("📲", "mobile phone with arrow"), ("☎️", "telephone"), ("📞", "telephone receiver"), ("📟", "pager"), ("📠", "fax machine"), ("🔋", "battery"), ("🪫", "low battery"), ("🔌", "electric plug"), ("💻", "laptop"), ("🖥️", "desktop computer"), ("🖨️", "printer"), ("⌨️", "keyboard"), ("🖱️", "computer mouse"), ("🖲️", "trackball"), ("💽", "computer disk"), ("💾", "floppy disk"), ("💿", "optical disk"), ("📀", "dvd"), ("🧮", "abacus"), ("🎥", "movie camera"), ("🎞️", "film frames"), ("📽️", "film projector"), ("🎬", "clapper board"), ("📺", "television"), ("📷", "camera"), ("📸", "camera with flash"), ("📹", "video camera"), ("📼", "videocassette"), ("🔍", "magnifying glass tilted left"), ("🔎", "magnifying glass tilted right"), ("🕯️", "candle"), ("💡", "light bulb"), ("🔦", "flashlight"), ("🏮", "red paper lantern"), ("🪔", "diya lamp"), ("📔", "notebook with decorative cover"), ("📕", "closed book"), ("📖", "open book"), ("📗", "green book"), ("📘", "blue book"), ("📙", "orange book"), ("📚", "books"), ("📓", "notebook"), ("📒", "ledger"), ("📃", "page with curl"), ("📜", "scroll"), ("📄", "page facing up"), ("📰", "newspaper"), ("🗞️", "rolled-up newspaper"), ("📑", "bookmark tabs"), ("🔖", "bookmark"), ("🏷️", "label"), ("🪙", "coin"), ("💰", "money bag"), ("🪎", "treasure chest"), ("💴", "yen banknote"), ("💵", "dollar banknote"), ("💶", "euro banknote"), ("💷", "pound banknote"), ("💸", "money with wings"), ("💳", "credit card"), ("🧾", "receipt"), ("💹", "chart increasing with yen"), ("✉️", "envelope"), ("📧", "e-mail"), ("📨", "incoming envelope"), ("📩", "envelope with arrow"), ("📤", "outbox tray"), ("📥", "inbox tray"), ("📦", "package"), ("📫", "closed mailbox with raised flag"), ("📪", "closed mailbox with lowered flag"), ("📬", "open mailbox with raised flag"), ("📭", "open mailbox with lowered flag"), ("📮", "postbox"), ("🗳️", "ballot box with ballot"), ("✏️", "pencil"), ("✒️", "black nib"), ("🖋️", "fountain pen"), ("🖊️", "pen"), ("🖌️", "paintbrush"), ("🖍️", "crayon"), ("📝", "memo"), ("💼", "briefcase"), ("📁", "file folder"), ("📂", "open file folder"), ("🗂️", "card index dividers"), ("📅", "calendar"), ("📆", "tear-off calendar"), ("🗒️", "spiral notepad"), ("🗓️", "spiral calendar"), ("📇", "card index"), ("📈", "chart increasing"), ("📉", "chart decreasing"), ("📊", "bar chart"), ("📋", "clipboard"), ("📌", "pushpin"), ("📍", "round pushpin"), ("📎", "paperclip"), ("🖇️", "linked paperclips"), ("📏", "straight ruler"), ("📐", "triangular ruler"), ("✂️", "scissors"), ("🗃️", "card file box"), ("🗄️", "file cabinet"), ("🗑️", "wastebasket"), ("🔒", "locked"), ("🔓", "unlocked"), ("🔏", "locked with pen"), ("🔐", "locked with key"), ("🔑", "key"), ("🗝️", "old key"), ("🔨", "hammer"), ("🪓", "axe"), ("⛏️", "pick"), ("⚒️", "hammer and pick"), ("🛠️", "hammer and wrench"), ("🗡️", "dagger"), ("⚔️", "crossed swords"), ("💣", "bomb"), ("🪃", "boomerang"), ("🏹", "bow and arrow"), ("🛡️", "shield"), ("🪚", "carpentry saw"), ("🔧", "wrench"), ("🪛", "screwdriver"), ("🔩", "nut and bolt"), ("⚙️", "gear"), ("🗜️", "clamp"), ("⚖️", "balance scale"), ("🦯", "white cane"), ("🔗", "link"), ("⛓️‍💥", "broken chain"), ("⛓️", "chains"), ("🪝", "hook"), ("🧰", "toolbox"), ("🧲", "magnet"), ("🪜", "ladder"), ("🪏", "shovel"), ("⚗️", "alembic"), ("🧪", "test tube"), ("🧫", "petri dish"), ("🧬", "dna"), ("🔬", "microscope"), ("🔭", "telescope"), ("📡", "satellite antenna"), ("💉", "syringe"), ("🩸", "drop of blood"), ("💊", "pill"), ("🩹", "adhesive bandage"), ("🩼", "crutch"), ("🩺", "stethoscope"), ("🩻", "x-ray"), ("🚪", "door"), ("🛗", "elevator"), ("🪞", "mirror"), ("🪟", "window"), ("🛏️", "bed"), ("🛋️", "couch and lamp"), ("🪑", "chair"), ("🚽", "toilet"), ("🪠", "plunger"), ("🚿", "shower"), ("🛁", "bathtub"), ("🪤", "mouse trap"), ("🪒", "razor"), ("🧴", "lotion bottle"), ("🧷", "safety pin"), ("🧹", "broom"), ("🧺", "basket"), ("🧻", "roll of paper"), ("🪣", "bucket"), ("🧼", "soap"), ("🫧", "bubbles"), ("🪥", "toothbrush"), ("🧽", "sponge"), ("🧯", "fire extinguisher"), ("🛒", "shopping cart"), ("🚬", "cigarette"), ("⚰️", "coffin"), ("🪦", "headstone"), ("⚱️", "funeral urn"), ("🧿", "nazar amulet"), ("🪬", "hamsa"), ("🗿", "moai"), ("🪧", "placard"), ("🪪", "identification card")],
    "Signs & Symbols": [("🏧", "ATM sign"), ("🚮", "litter in bin sign"), ("🚰", "potable water"), ("♿", "wheelchair symbol"), ("🚹", "men’s room"), ("🚺", "women’s room"), ("🚻", "restroom"), ("🚼", "baby symbol"), ("🚾", "water closet"), ("🛂", "passport control"), ("🛃", "customs"), ("🛄", "baggage claim"), ("🛅", "left luggage"), ("⚠️", "warning"), ("🚸", "children crossing"), ("⛔", "no entry"), ("🚫", "prohibited"), ("🚳", "no bicycles"), ("🚭", "no smoking"), ("🚯", "no littering"), ("🚱", "non-potable water"), ("🚷", "no pedestrians"), ("📵", "no mobile phones"), ("🔞", "no one under eighteen"), ("☢️", "radioactive"), ("☣️", "biohazard"), ("⬆️", "up arrow"), ("↗️", "up-right arrow"), ("➡️", "right arrow"), ("↘️", "down-right arrow"), ("⬇️", "down arrow"), ("↙️", "down-left arrow"), ("⬅️", "left arrow"), ("↖️", "up-left arrow"), ("↕️", "up-down arrow"), ("↔️", "left-right arrow"), ("↩️", "right arrow curving left"), ("↪️", "left arrow curving right"), ("⤴️", "right arrow curving up"), ("⤵️", "right arrow curving down"), ("🔃", "clockwise vertical arrows"), ("🔄", "counterclockwise arrows button"), ("🔙", "BACK arrow"), ("🔚", "END arrow"), ("🔛", "ON! arrow"), ("🔜", "SOON arrow"), ("🔝", "TOP arrow"), ("🛐", "place of worship"), ("⚛️", "atom symbol"), ("🕉️", "om"), ("✡️", "star of David"), ("☸️", "wheel of dharma"), ("☯️", "yin yang"), ("✝️", "latin cross"), ("☦️", "orthodox cross"), ("☪️", "star and crescent"), ("☮️", "peace symbol"), ("🕎", "menorah"), ("🔯", "dotted six-pointed star"), ("🪯", "khanda"), ("♈", "Aries"), ("♉", "Taurus"), ("♊", "Gemini"), ("♋", "Cancer"), ("♌", "Leo"), ("♍", "Virgo"), ("♎", "Libra"), ("♏", "Scorpio"), ("♐", "Sagittarius"), ("♑", "Capricorn"), ("♒", "Aquarius"), ("♓", "Pisces"), ("⛎", "Ophiuchus"), ("🔀", "shuffle tracks button"), ("🔁", "repeat button"), ("🔂", "repeat single button"), ("▶️", "play button"), ("⏩", "fast-forward button"), ("⏭️", "next track button"), ("⏯️", "play or pause button"), ("◀️", "reverse button"), ("⏪", "fast reverse button"), ("⏮️", "last track button"), ("🔼", "upwards button"), ("⏫", "fast up button"), ("🔽", "downwards button"), ("⏬", "fast down button"), ("⏸️", "pause button"), ("⏹️", "stop button"), ("⏺️", "record button"), ("⏏️", "eject button"), ("🎦", "cinema"), ("🔅", "dim button"), ("🔆", "bright button"), ("📶", "antenna bars"), ("🛜", "wireless"), ("📳", "vibration mode"), ("📴", "mobile phone off"), ("♀️", "female sign"), ("♂️", "male sign"), ("⚧️", "transgender symbol"), ("✖️", "multiply"), ("➕", "plus"), ("➖", "minus"), ("➗", "divide"), ("🟰", "heavy equals sign"), ("♾️", "infinity"), ("‼️", "double exclamation mark"), ("⁉️", "exclamation question mark"), ("❓", "red question mark"), ("❔", "white question mark"), ("❕", "white exclamation mark"), ("❗", "red exclamation mark"), ("〰️", "wavy dash"), ("💱", "currency exchange"), ("💲", "heavy dollar sign"), ("⚕️", "medical symbol"), ("♻️", "recycling symbol"), ("⚜️", "fleur-de-lis"), ("🔱", "trident emblem"), ("📛", "name badge"), ("🔰", "Japanese symbol for beginner"), ("⭕", "hollow red circle"), ("✅", "check mark button"), ("☑️", "check box with check"), ("✔️", "check mark"), ("❌", "cross mark"), ("❎", "cross mark button"), ("➰", "curly loop"), ("➿", "double curly loop"), ("〽️", "part alternation mark"), ("✳️", "eight-spoked asterisk"), ("✴️", "eight-pointed star"), ("❇️", "sparkle"), ("©️", "copyright"), ("®️", "registered"), ("™️", "trade mark"), ("🫟", "splatter"), ("#️⃣", "keycap: #"), ("*️⃣", "keycap: *"), ("0️⃣", "keycap: 0"), ("1️⃣", "keycap: 1"), ("2️⃣", "keycap: 2"), ("3️⃣", "keycap: 3"), ("4️⃣", "keycap: 4"), ("5️⃣", "keycap: 5"), ("6️⃣", "keycap: 6"), ("7️⃣", "keycap: 7"), ("8️⃣", "keycap: 8"), ("9️⃣", "keycap: 9"), ("🔟", "keycap: 10"), ("🔠", "input latin uppercase"), ("🔡", "input latin lowercase"), ("🔢", "input numbers"), ("🔣", "input symbols"), ("🔤", "input latin letters"), ("🅰️", "A button (blood type)"), ("🆎", "AB button (blood type)"), ("🅱️", "B button (blood type)"), ("🆑", "CL button"), ("🆒", "COOL button"), ("🆓", "FREE button"), ("ℹ️", "information"), ("🆔", "ID button"), ("Ⓜ️", "circled M"), ("🆕", "NEW button"), ("🆖", "NG button"), ("🅾️", "O button (blood type)"), ("🆗", "OK button"), ("🅿️", "P button"), ("🆘", "SOS button"), ("🆙", "UP! button"), ("🆚", "VS button"), ("🈁", "Japanese “here” button"), ("🈂️", "Japanese “service charge” button"), ("🈷️", "Japanese “monthly amount” button"), ("🈶", "Japanese “not free of charge” button"), ("🈯", "Japanese “reserved” button"), ("🉐", "Japanese “bargain” button"), ("🈹", "Japanese “discount” button"), ("🈚", "Japanese “free of charge” button"), ("🈲", "Japanese “prohibited” button"), ("🉑", "Japanese “acceptable” button"), ("🈸", "Japanese “application” button"), ("🈴", "Japanese “passing grade” button"), ("🈳", "Japanese “vacancy” button"), ("㊗️", "Japanese “congratulations” button"), ("㊙️", "Japanese “secret” button"), ("🈺", "Japanese “open for business” button"), ("🈵", "Japanese “no vacancy” button"), ("🔴", "red circle"), ("🟠", "orange circle"), ("🟡", "yellow circle"), ("🟢", "green circle"), ("🔵", "blue circle"), ("🟣", "purple circle"), ("🟤", "brown circle"), ("⚫", "black circle"), ("⚪", "white circle"), ("🟥", "red square"), ("🟧", "orange square"), ("🟨", "yellow square"), ("🟩", "green square"), ("🟦", "blue square"), ("🟪", "purple square"), ("🟫", "brown square"), ("⬛", "black large square"), ("⬜", "white large square"), ("◼️", "black medium square"), ("◻️", "white medium square"), ("◾", "black medium-small square"), ("◽", "white medium-small square"), ("▪️", "black small square"), ("▫️", "white small square"), ("🔶", "large orange diamond"), ("🔷", "large blue diamond"), ("🔸", "small orange diamond"), ("🔹", "small blue diamond"), ("🔺", "red triangle pointed up"), ("🔻", "red triangle pointed down"), ("💠", "diamond with a dot"), ("🔘", "radio button"), ("🔳", "white square button"), ("🔲", "black square button"), ("🇺🇸", "flag: United States")],
}
CATEGORY_ICONS = {
    "Smileys":           "😀",  "Hearts":            "❤️",
    "Emotions":          "💯",  "Hands":             "👋",
    "Body":              "💪",  "People Actions":    "🏃",
    "People Roles":      "👩\u200d⚕️","People Activities": "🏄",
    "Love & Family":     "🤝",  "Animals":           "🐶",
    "Plants":            "🌸",  "Food & Dining":     "🍕",
    "Places & Buildings":"🏛️",  "Travel":            "✈️",
    "Time":              "⏰",  "Sky & Weather":     "⛅",
    "Events":            "🎃",  "Awards & Sports":   "🏆",
    "Objects":           "🎯",  "Signs & Symbols":   "🔣",
}

# ════════════════════════════════════════════════════════════════════
#  THEME
# ════════════════════════════════════════════════════════════════════
BG         = "#1e1e2e"
BG_SIDEBAR = "#161622"
BG_CARD    = "#2a2a3d"
BG_HOVER   = "#3d3d58"
BG_SEL     = "#0078d4"
FG         = "#cdd6f4"
FG_DIM     = "#555570"
ACCENT     = "#89b4fa"

FONT_EMOJI  = ("Segoe UI Emoji", 17)
FONT_UI     = ("Segoe UI", 9)
FONT_SIDE   = ("Segoe UI Emoji", 9)

WIN_W, WIN_H = 780, 520
CELL         = 46   # px per emoji cell (grid)
SB_W         = 154  # sidebar width

# ════════════════════════════════════════════════════════════════════
#  WIN32 CLIPBOARD  — reliably handles multi-codepoint emoji
# ════════════════════════════════════════════════════════════════════
def _win32_copy(text: str) -> bool:
    """Copy text to clipboard via Win32 API. Returns True on success."""
    try:
        k32 = ctypes.windll.kernel32
        u32 = ctypes.windll.user32
        CF_UNICODETEXT = 13
        GMEM_MOVEABLE  = 0x0002
        raw = text.encode("utf-16-le") + b"\x00\x00"
        h   = k32.GlobalAlloc(GMEM_MOVEABLE, len(raw))
        ptr = k32.GlobalLock(h)
        ctypes.memmove(ptr, raw, len(raw))
        k32.GlobalUnlock(h)
        u32.OpenClipboard(0)
        u32.EmptyClipboard()
        u32.SetClipboardData(CF_UNICODETEXT, h)
        u32.CloseClipboard()
        return True
    except Exception:
        return False


# ════════════════════════════════════════════════════════════════════
#  EMOJI PICKER
# ════════════════════════════════════════════════════════════════════
class EmojiPicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self._cur_cat       = None
        self._search_active = False
        self._photo_cache   = {}   # emoji_char -> ImageTk.PhotoImage (or None)
        self._pil_font      = None

        self._dpi_aware()
        self._load_pil_font()
        self._build_ui()
        self._position()

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        # Defer first render — window appears immediately, then populates
        self.root.after(0, lambda: self._sel_cat(next(iter(EMOJI_DATA))))
        self.root.mainloop()

    # ── DPI ──────────────────────────────────────────────────────────
    def _dpi_aware(self):
        if platform.system() == "Windows":
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass

    # ── PIL font ─────────────────────────────────────────────────────
    def _load_pil_font(self):
        if not HAS_PIL:
            return
        candidates = [
            r"C:\Windows\Fonts\seguiemj.ttf",
            os.path.expandvars(r"%WINDIR%\Fonts\seguiemj.ttf"),
        ]
        size = CELL - 10
        for path in candidates:
            try:
                self._pil_font = ImageFont.truetype(path, size)
                return
            except Exception:
                continue

    # ── Emoji → PhotoImage (lazy, cached) ────────────────────────────
    def _get_photo(self, emoji: str):
        if emoji in self._photo_cache:
            return self._photo_cache[emoji]
        if not HAS_PIL or not self._pil_font:
            self._photo_cache[emoji] = None
            return None
        try:
            sz   = CELL - 4
            img  = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            # measure and center
            bb = draw.textbbox((0, 0), emoji, font=self._pil_font,
                               embedded_color=True)
            ew, eh = bb[2] - bb[0], bb[3] - bb[1]
            ox = (sz - ew) // 2 - bb[0]
            oy = (sz - eh) // 2 - bb[1]
            draw.text((ox, oy), emoji, font=self._pil_font,
                      embedded_color=True)
            photo = ImageTk.PhotoImage(img)
            self._photo_cache[emoji] = photo
            return photo
        except Exception:
            self._photo_cache[emoji] = None
            return None

    # ── Position near cursor (multi-monitor safe) ─────────────────────
    def _position(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        pt = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        mx, my = pt.x, pt.y

        # Prefer opening below-right; flip if near screen edge
        x = mx + 10
        y = my + 10
        if x + WIN_W > sw:
            x = mx - WIN_W - 10
        if y + WIN_H > sh:
            y = my - WIN_H - 10
        # Do NOT clamp to 0 — supports negative coords on left-of-primary monitors
        self.root.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

    # ── Build UI ─────────────────────────────────────────────────────
    def _build_ui(self):
        r = self.root
        r.title("Emoji Picker")
        r.configure(bg=BG)
        r.resizable(True, True)
        r.minsize(540, 380)

        # ttk style — correct naming: prefix.Vertical.TScrollbar
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Custom.Vertical.TScrollbar",
                    troughcolor=BG_SIDEBAR, background=BG_CARD,
                    arrowcolor=FG_DIM, borderwidth=0, relief="flat",
                    width=10)
        s.map("Custom.Vertical.TScrollbar",
              background=[("active", BG_HOVER), ("!active", BG_CARD)])

        r.bind("<Escape>",   lambda e: r.destroy())
        r.bind("<FocusOut>", self._focus_out)

        outer = tk.Frame(r, bg=BG)
        outer.pack(fill=tk.BOTH, expand=True)

        # ── SIDEBAR ────────────────────────────────────────────────
        sb = tk.Frame(outer, bg=BG_SIDEBAR, width=SB_W)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        sb.pack_propagate(False)

        tk.Label(sb, text="Categories", bg=BG_SIDEBAR, fg=FG_DIM,
                 font=FONT_UI, anchor="w", padx=10, pady=7).pack(fill=tk.X)
        tk.Frame(sb, bg=BG_CARD, height=1).pack(fill=tk.X)

        # Sidebar scrolls if needed (20 cats usually fit; keep for safety)
        sbc = tk.Canvas(sb, bg=BG_SIDEBAR, highlightthickness=0, bd=0)
        sbv = ttk.Scrollbar(sb, orient="vertical", command=sbc.yview,
                            style="Custom.Vertical.TScrollbar")
        sbc.configure(yscrollcommand=sbv.set)
        sbv.pack(side=tk.RIGHT, fill=tk.Y)
        sbc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        cf = tk.Frame(sbc, bg=BG_SIDEBAR)
        sbc.create_window(0, 0, anchor="nw", window=cf)
        cf.bind("<Configure>",
                lambda e: sbc.configure(scrollregion=sbc.bbox("all")))
        sbc.bind("<MouseWheel>",
                 lambda e: sbc.yview_scroll(-1*(e.delta//120), "units"))

        self._cat_btns = {}
        for cat in EMOJI_DATA:
            icon = CATEGORY_ICONS.get(cat, "")
            lbl = tk.Label(cf, text=f"  {icon}  {cat}",
                           bg=BG_SIDEBAR, fg=FG, font=FONT_SIDE,
                           anchor="w", pady=5, cursor="hand2")
            lbl.pack(fill=tk.X)
            lbl.bind("<Button-1>", lambda e, c=cat: self._sel_cat(c))
            lbl.bind("<Enter>",    lambda e, b=lbl, c=cat: self._sb_hover(b, c, True))
            lbl.bind("<Leave>",    lambda e, b=lbl, c=cat: self._sb_hover(b, c, False))
            self._cat_btns[cat] = lbl

        # ── RIGHT PANEL ─────────────────────────────────────────────
        rp = tk.Frame(outer, bg=BG)
        rp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Search bar
        sf = tk.Frame(rp, bg=BG_SIDEBAR, padx=8, pady=6)
        sf.pack(fill=tk.X)
        self._sv = tk.StringVar()
        self._se = tk.Entry(sf, textvariable=self._sv,
                            bg=BG_CARD, fg=FG_DIM, insertbackground=FG,
                            font=FONT_UI, relief="flat",
                            highlightthickness=1,
                            highlightbackground=BG_HOVER,
                            highlightcolor=ACCENT)
        self._se.pack(fill=tk.X, ipady=5)
        self._se.insert(0, "🔍  Search emoji names…")
        self._se.bind("<FocusIn>",  self._search_in)
        self._se.bind("<FocusOut>", self._search_out)
        self._sv.trace_add("write", self._on_search)

        tk.Frame(rp, bg=BG_CARD, height=1).pack(fill=tk.X)

        # ── Emoji grid: Canvas (fast) + auto-hide Scrollbar ─────────
        gf = tk.Frame(rp, bg=BG)
        gf.pack(fill=tk.BOTH, expand=True)
        gf.columnconfigure(0, weight=1)
        gf.rowconfigure(0, weight=1)

        self._cv  = tk.Canvas(gf, bg=BG, highlightthickness=0, bd=0)
        self._vsb = ttk.Scrollbar(gf, orient="vertical",
                                   command=self._cv.yview,
                                   style="Custom.Vertical.TScrollbar")
        self._cv.configure(yscrollcommand=self._vsb.set)

        # Use grid so we can show/hide the scrollbar without breaking layout
        self._cv.grid(row=0, column=0, sticky="nsew")
        # Scrollbar starts hidden; _update_sb() shows it when needed

        self._cv.bind("<Configure>", self._on_cv_resize)
        self._cv.bind("<MouseWheel>", self._wheel)

        # Status bar
        self._stat = tk.StringVar(value="Click an emoji to copy it to the clipboard")
        tk.Frame(rp, bg=BG_CARD, height=1).pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(rp, textvariable=self._stat,
                 bg=BG_SIDEBAR, fg=FG_DIM,
                 font=FONT_UI, anchor="w", padx=10, pady=4
                 ).pack(fill=tk.X, side=tk.BOTTOM)

    # ── Sidebar hover ─────────────────────────────────────────────
    def _sb_hover(self, btn, name, on):
        if name != self._cur_cat:
            btn.config(bg=BG_CARD if on else BG_SIDEBAR)

    # ── Category select ───────────────────────────────────────────
    def _sel_cat(self, name):
        if self._search_active:
            self._sv.set("")
            self._se.config(fg=FG_DIM)
            self._se.delete(0, tk.END)
            self._se.insert(0, "🔍  Search emoji names…")
            self._search_active = False
        if self._cur_cat and self._cur_cat in self._cat_btns:
            self._cat_btns[self._cur_cat].config(bg=BG_SIDEBAR, fg=FG)
        self._cur_cat = name
        if name in self._cat_btns:
            self._cat_btns[name].config(bg=BG_SEL, fg="#ffffff")
        self._render(EMOJI_DATA.get(name, []))

    # ── Render emoji grid via Canvas items ───────────────────────
    def _render(self, emoji_list):
        cv = self._cv
        cv.delete("all")

        if not emoji_list:
            cv.create_text(200, 40, text="No results found",
                           fill=FG_DIM, font=FONT_UI)
            cv.configure(scrollregion=(0, 0, 1, 1))
            self._update_sb()
            return

        cv.update_idletasks()
        w = cv.winfo_width()
        if w < CELL:
            w = WIN_W - SB_W - 20

        cols = max(1, w // CELL)
        pad  = (w - cols * CELL) // 2   # horizontal centering

        for idx, (emoji, name) in enumerate(emoji_list):
            row, col = divmod(idx, cols)
            x = pad + col * CELL
            y = row * CELL + 2
            tag = f"c{idx}"

            # Card background
            cv.create_rectangle(x+1, y+1, x+CELL-2, y+CELL-2,
                                 fill=BG_CARD, outline="", tags=tag)

            # Emoji: prefer PIL image (color); fallback to text
            photo = self._get_photo(emoji) if HAS_PIL else None
            if photo:
                cv.create_image(x + CELL//2, y + CELL//2,
                                image=photo, anchor="center", tags=tag)
            else:
                cv.create_text(x + CELL//2, y + CELL//2,
                               text=emoji, font=FONT_EMOJI, fill=FG,
                               tags=tag)

            # Hover / click bindings (bound to tag covering rect + content)
            cv.tag_bind(tag, "<Enter>",
                lambda e, t=tag, n=name: self._hon(t, n))
            cv.tag_bind(tag, "<Leave>",
                lambda e, t=tag: self._hoff(t))
            cv.tag_bind(tag, "<Button-1>",
                lambda e, em=emoji: self._pick(em))
            cv.tag_bind(tag, "<MouseWheel>", self._wheel)

        rows = (len(emoji_list) + cols - 1) // cols
        cv.configure(scrollregion=(0, 0, w, rows * CELL + 4))
        cv.yview_moveto(0)
        self._update_sb()

    def _hon(self, tag, name):
        # Recolor first item in tag (the rectangle)
        items = self._cv.find_withtag(tag)
        if items:
            self._cv.itemconfig(items[0], fill=BG_HOVER)
        self._stat.set(name)

    def _hoff(self, tag):
        items = self._cv.find_withtag(tag)
        if items:
            self._cv.itemconfig(items[0], fill=BG_CARD)
        self._stat.set("Click an emoji to copy it to the clipboard")

    # ── Pick / copy emoji ────────────────────────────────────────
    def _pick(self, emoji):
        ok = _win32_copy(emoji)
        if not ok:
            # Fallback to tkinter clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(emoji)
            self.root.update()
        self._stat.set(f"Copied  {emoji}  — paste with Ctrl+V")
        self.root.after(140, self.root.destroy)

    # ── Auto-hide scrollbar ──────────────────────────────────────
    def _update_sb(self):
        try:
            sr = self._cv.cget("scrollregion")
            parts = str(sr).split() if sr else []
            content_h = float(parts[3]) if len(parts) >= 4 else 0
            view_h    = self._cv.winfo_height()
            if content_h > view_h + 2:
                self._vsb.grid(row=0, column=1, sticky="ns")
            else:
                self._vsb.grid_remove()
        except Exception:
            pass

    # ── Re-render on canvas resize ───────────────────────────────
    def _on_cv_resize(self, event):
        if self._cur_cat and not self._search_active:
            self._render(EMOJI_DATA.get(self._cur_cat, []))
        self._update_sb()

    # ── Mouse wheel ──────────────────────────────────────────────
    def _wheel(self, event):
        self._cv.yview_scroll(-1 * (event.delta // 120), "units")

    # ── Search ───────────────────────────────────────────────────
    def _search_in(self, _):
        if not self._search_active:
            self._se.delete(0, tk.END)
            self._se.config(fg=FG)
            self._search_active = True
            if self._cur_cat and self._cur_cat in self._cat_btns:
                self._cat_btns[self._cur_cat].config(bg=BG_SIDEBAR, fg=FG)
            self._cur_cat = None

    def _search_out(self, _):
        if self._search_active and not self._sv.get().strip():
            self._se.config(fg=FG_DIM)
            self._se.delete(0, tk.END)
            self._se.insert(0, "🔍  Search emoji names…")
            self._search_active = False
            self._sel_cat(next(iter(EMOJI_DATA)))

    def _on_search(self, *_):
        if not self._search_active:
            return
        q = self._sv.get().strip().lower()
        if not q:
            self._render([])
            return
        results = [(em, nm) for emojis in EMOJI_DATA.values()
                   for em, nm in emojis if q in nm.lower() or q in em]
        self._render(results)

    # ── Focus-out close ──────────────────────────────────────────
    def _focus_out(self, e):
        if e.widget == self.root:
            self.root.after(200, self._check_focus)

    def _check_focus(self):
        try:
            if self.root.focus_get() is None:
                self.root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    EmojiPicker()
