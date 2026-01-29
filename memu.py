from pathlib import Path
from datetime import datetime
import json
import sqlite3
import os
import types

COLORS = {
    'BLACK': '\033[30m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'WHITE': '\033[37m',
    'RESET': '\033[0m',
    
    'BRIGHT_BLACK': '\033[90m',
    'BRIGHT_RED': '\033[91m',
    'BRIGHT_GREEN': '\033[92m',
    'BRIGHT_YELLOW': '\033[93m',
    'BRIGHT_BLUE': '\033[94m',
    'BRIGHT_MAGENTA': '\033[95m',
    'BRIGHT_CYAN': '\033[96m',
    'BRIGHT_WHITE': '\033[97m',
    
    'BG_BLACK': '\033[40m',
    'BG_RED': '\033[41m',
    'BG_GREEN': '\033[42m',
    'BG_YELLOW': '\033[43m',
    'BG_BLUE': '\033[44m',
    'BG_MAGENTA': '\033[45m',
    'BG_CYAN': '\033[46m',
    'BG_WHITE': '\033[47m',
    
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'REVERSED': '\033[7m',
}

class Memu:
    def __init__(self):
        self.memu_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        self.repository_path = Path(f'{self.memu_dir}/repository')
        self.disks_path = Path(f'{self.memu_dir}/disks')
        try:
            with open(f'{self.memu_dir}/config.json', 'r') as data:
                self.config = json.load(data)
        except FileNotFoundError:
            data = {
                'disks_number': 1,
                'boot_device': 'live',
                'live_system': 'muskatos',
                'live_version': '26.0'
            }
            with open('config.json', 'w') as file:
                json.dump(data, file, indent=4)
            with open('config.json', 'r') as data:
                self.config = json.load(data)
    
    def mkdisk(self, disk = False):
        if not disk:
            disk = f'disk{len(os.listdir(self.disks_path))}'
        
        conn = sqlite3.connect(f'{self.memu_dir}/disks/{disk}.db')
        curs = conn.cursor()

        curs.execute('''
            CREATE TABLE IF NOT EXISTS fs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                parent TEXT,
                path TEXT,
                type TEXT,
                permissions TEXT,
                creation_date TEXT,
                content TEXT,
                size INTEGER
            )''')
        curs.execute('''
            INSERT INTO fs (name, parent, path, type, permissions, creation_date) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            disk, '/', disk, 'folder', 'r', datetime.now().isoformat()
        )
        )
        conn.commit()
        conn.close()

        self.mk(disk, 'mnt', 'folder', 'r')
    
    def mk(self, path, name, obj_type, permissions):
        parts = path.split('/')
        disk = parts[0]

        conn = sqlite3.connect(f'{self.memu_dir}/disks/{disk}.db')
        curs = conn.cursor()

        curs.execute('''
            INSERT INTO fs (name, parent, path, type, permissions, creation_date) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            name, path, f'{path}/{name}', obj_type, permissions, datetime.now().isoformat()
        )
        )

        conn.commit()
        conn.close()

    def rm(self, path):
        parts = path.split('/')

        conn = sqlite3.connect(f'{self.memu_dir}/disks/{parts[0]}.db')
        curs = conn.cursor()

        curs.execute('''
            DELETE FROM fs WHERE path = ?
        ''', (path,))

        conn.commit()
        conn.close()

    def write_file(self, path, content):
        parts = path.split('/')

        conn = sqlite3.connect(f'{self.memu_dir}/disks/{parts[0]}.db')
        curs = conn.cursor()
        
        info = self.get_info(path)
        
        if info['type'] == 'file':
            curs.execute('''
                UPDATE fs SET content = ?, size = ? WHERE path = ?''', 
                (
                    content, len(content), path,
                ))
        else:
            return False

        conn.commit()
        conn.close()

    def update_permission(self, path, perms):
        parts = path.split('/')

        conn = sqlite3.connect(f'{self.memu_dir}/disks/{parts[0]}.db')
        curs = conn.cursor()

        curs.execute('''
            UPDATE fs SET permissions = ? WHERE path = ?''',
            (perms, path,))

        conn.commit()
        conn.close()

    def get_info(self, path):
        conn = sqlite3.connect(f'{self.memu_dir}/disks/{path.split('/')[0]}.db')
        conn.row_factory = sqlite3.Row 
        curs = conn.cursor()

        curs.execute('''
            SELECT * FROM fs WHERE path = ? LIMIT 1
        ''', (path,))
        data = curs.fetchone()

        conn.close()

        if data:
            return dict(data)
        else: return False

    def get_children(self, src_path):
        parts = src_path.split('/')
        conn = sqlite3.connect(f'{self.memu_dir}/disks/{parts[0]}.db')
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()

        curs.execute('''
            SELECT * FROM fs WHERE parent = ?
        ''', (src_path,))

        children = []
        for child in curs.fetchall():
            children.append(child['path'])

        conn.close()

        if children:
            return children
        else: return False

    def clear_display(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')

    def muskatos_live(self):
        version = self.config['live_version']
        
        # Creating live disk
        disk = f'disk{len(os.listdir(self.disks_path))}'
        self.mkdisk(disk)

        # Installing fresh live system

        # Creating live system default folders and files
        root_objects = [
            ('memu', 'folder', 'r'),
            ('programs', 'folder', 'r'),
            ('config', 'folder', 'r'),
            ('usr', 'folder', 'r'),
            ('home', 'folder', 'r')
        ]
        for name, obj_type, perm in root_objects:
            self.mk(disk, name, obj_type, perm)

        objects = [
            (f'memu', 'boot.py', 'file', 'r'),
            (f'config', 'hostname', 'file', 'r')
        ]

        for path, name, obj_type, perm in objects:
            self.mk(f'{disk}/{path}', name, obj_type, perm)

        # Reading information from repository
        try:
            base = os.listdir(Path(self.memu_dir) / self.repository_path / version / 'programs' / 'base')
            tetris = Path(self.memu_dir) / self.repository_path / version / 'programs' / 'tetris'
        except FileNotFoundError:
            print(f'{COLORS['RED']}incorrect version: {self.config['live_version']}{COLORS['RESET']}')
            return False

        base.pop(base.index('muskatos'))

        with open(Path(self.memu_dir) / self.repository_path / version / 'programs' / 'base' / 'memu_boot_live.py', 'r') as f:
            self.write_file(f'{disk}/memu/boot.py', f.read())
        base.pop(base.index('memu_boot.py'))

        for program in base:
            with open(Path(self.memu_dir) / self.repository_path / version / 'programs' / 'base' / program, 'r') as f:
                self.mk(f'{disk}/programs', program, 'file', 'r')
                self.write_file(f'{disk}/programs/{program}', f.read())

        with open(tetris / 'tetstrap.py', 'r') as f:
            program = 'tetstrap.py'
            self.mk(f'{disk}/programs', program, 'file', 'r')
            self.write_file(f'{disk}/programs/{program}', f.read())

        self.write_file(f'{disk}/config/hostname', 'muskatos')

        # Booting into live

        self.boot(disk)

        # Removing live disk

        os.remove(f'{self.memu_dir}/disks/{disk}.db')

    def boot(self, disk):
        if not Path(f'{self.memu_dir}/disks/{disk}.db').exists():
            print(f"{COLORS['RED']}cant't boot from {disk}: disk not exist{COLORS['RESET']}")
            return

        boot_info = self.get_info(f'{disk}/memu/boot.py')
        context = {
            'memu': self,
            'colors': COLORS,
            'disk': disk,
            'mode': 'boot',
            'disks': self.disks_path,
            'memu_path': self.memu_dir
        }
        if boot_info:
            exec(boot_info['content'], context)
        else:
            print(f"{COLORS['RED']}cant't boot from {disk}: boot.py not found{COLORS['RESET']}")

memu = Memu()

memu.disks_path.mkdir(exist_ok=True)

disks_num = memu.config['disks_number']

i = len(os.listdir(memu.disks_path))
while i < int(disks_num):
    memu.mkdisk()
    i += 1

boot_device = memu.config['boot_device']
live_system = memu.config['live_system']

if boot_device == 'live':
    if live_system == 'muskatos':
        memu.muskatos_live()
    elif live_system == 'quickpyre':
        print(f'{COLORS['RED']}Quickpyre support is in development{COLORS['RESET']}')
    else:
        print(f'{COLORS['RED']}Unknown operating system: {live_system}{COLORS['RESET']}')
else:
    memu.boot(boot_device)
