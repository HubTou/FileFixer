# FileFixer
A long time ago, on the Apple ]\[, there was a famous utility for editing disks, for example for modifying games saves (adding lives!), or removing disk protections (performing the allowed "anti-coffee" copy):
* It was known as [DISKFIXER](http://mirrors.apple2.org.za/ftp.apple.asimov.net/images/disk_utils/BitCopyII_DiskFixer_NibblesAway_QuickFull_SuperCopy_SuperDiskCopy.zip), (C) 1980, The Image Producers, Inc., A Quicksilver Softsystems utility.
* And later as [DISK EDIT](http://mirrors.apple2.org.za/ftp.apple.asimov.net/images/disk_utils/Disk%20Edit%204.0%20%28c%29%201985%20The%20Software%20Company%2C%20Inc.dsk), (C) 1985, The Software Factory, Inc. (in which the help function still mentioned DISKFIXER, and the user interface was almost identical, so I assume it was a direct successor).

40+ years later, I needed an idea for testing Tkinter GUIs for Python applications. Having just remade the Unix [strings](https://github.com/HubTou/strings) utility, I thought of re-implementing my beloved DiskFixer.

So here's a first partial version:
* it has fully functional view modes
* but it still lacks the edit functions (that I'll implement in 2022)

I'll also:
* provide a Python Package for easy install
* an internationalized version with at least French and English languages

So far, the following commands have been implemented:
```
CHUNK SELECTION:
 [DOWN/RIGHT ARROW] Next chunk of file.
 [UP/LEFT ARROW]    Previous chunk of file.
 
CHUNK VIEW:
 [A] ASCII characters view mode.
 [B] Mode ASCII-hexa (half screen each).
 [H] Hexadecimal bytes view mode.

GENERAL MODE:
 [N] Toggle hexa/decimal numbering.
 [Q] Quit the FileFixer to monitor.
 [S] Select a new file (modified from the original "Slot and drive specification").
 [Y] Toggle ASCII filter.
 
KEYBOARD EQUIVALENTS:
 [CTRL-H] <===> [LEFT ARROW] Key
 [CTRL-J] <===> [DOWN ARROW] Key
 [CTRL-K] <===> [UP ARROW] Key
 [CTRL-Q] <===> [Q] Key
 [CTRL-U] <===> [RIGHT ARROW] Key

NEW COMMANDS:
 [!] Cycle colors (from green, amber, gray, inverted gray monitors)
```

You can try the original versions with the excellent [AppleWIn](https://github.com/AppleWin/AppleWin) Apple ]\[ emulator.
