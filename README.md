# MuskatOS
MuskatOS is a Unix-like pseudo operating system written fully in **python**. When you are installing MuskatOS you are getting:
- Fully working file system based on sqlite
- Tetris package manager
- User's programs support
- Weekly and monthly updates(nope)
# Memu
Memu is a pseudo computer emulator. MuskatOS uses it to start up. Also in future memu will support another pseudo OS written in python - <html><a href="https://github.com/LozkaDani/QuickPyre">QuickPyre</a></html>.
# Installation guide
To install MuskatOS you must follow these steps:
- Clone repository using ```git clone```
- Start live system via Memu using ```python memu.py```
- From the live system install the main system onto the first disk using ```tetstrap disk0 base``` or install specific packages. If you are installing not every package, you must to install memuboot and base system using ```tetstrap disk0 base/memuboot base/muskatos```
- Edit Memu config and change boot device from live system to the first disk
- Reboot Memu
- If you want as root create new user via ```adduser <user> <groups>``` and set password using ```passwd <user>```
Now you have got working MuskatOS! To update system run ```tetris -S tetris/tetris base``` as root user. In future there will be -Syu option in tetris.
# What's new?
MuskatOS 26.0 - a completely rewritten, fresh new version of MuskatOS. Here is the full changelog:
- Filesystem is now fully based on sqlite3
- Memu support was added
- Package manager 'tetris' was added
- Now commands are not part of the kernel, they are separate programs
- The echo command can now write text to files
- Many other changes
# MuskatOS Rust Edition
<html><a href="https://github.com/muskatya/muskatos-rust">MuskatOS Rust Edition</a></html> is a port of MuskatOS to Rust. At the moment, MOSRE doesn't support Memu, and it has no file system at all. In the future, it will be a full port of MOS to Rust, but for now, it is a very stripped-down version of MuskatOS.
