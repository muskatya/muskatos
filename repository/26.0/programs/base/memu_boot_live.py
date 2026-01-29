import json
import os

class Memu_Patched:
    def __init__(self):
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def mk(self, path, name, obj_type, permissions):
        parent_data = memu.get_info(path)

        if parent_data['type'] != 'folder':
            return False
        
        if not 'w' in parent_data['permissions'].split(','):
            if 'root' in self.curr_user_groups:
                memu.mk(path, name, obj_type, permissions)
                return True
            else:
                return False

        memu.mk(path, name, obj_type, permissions)
        return True

    def get_info(self, path):
        return memu.get_info(path)

    def get_children(self, path):
        return memu.get_children(path)

    def rm(self, path):
        file_data = memu.get_info(path)

        if not 'w' in file_data['permissions'].split(','):
            if 'root' in self.curr_user_groups:
                memu.rm(path)
                return True
            else:
                return False

        memu.rm(path)
        return True

    def write_file(self, path, content):
        file_data = memu.get_info(path)

        if not 'w' in file_data['permissions'].split(','):
            if 'root' in self.curr_user_groups:
                memu.write_file(path, content)
                return True
            else:
                return False

        memu.write_file(path, content)
        return True

    def get_abs_path_real(self, path):
        cwd = self.get_info(f'{disk}/usr/cwd')['content']
        disk = cwd.split('/')[0]
        user = self.get_info(f'{disk}/usr/curr_user')['content']
        
        if '/' in path:
            path_parts = path.split('/')
        else:
            path_parts = [path]

        result = []

        for i in path_parts:
            if i == '~':
                if user == 'root':
                    result.append(f'{disk}/root')
                else:
                    result.append(f'{disk}/home/{user}')
            elif i == '.':
                result.append(cwd)
            elif i == '..':
                if result:
                    result.pop()
                else:
                    result.append('/'.join(cwd.split('/')[:-1]))
            else:
                result.append(i)
        
        result = '/'.join(result)
        
        if not result.startswith(disk):
            result = cwd + '/' + result

        return result

    def get_abs_path(self, path):
        cwd = self.get_info(f'{disk}/usr/cwd')['content']
        user = self.get_info(f'{disk}/usr/curr_user')['content']
        
        if '/' in path:
            path_parts = path.split('/')
        else:
            path_parts = [path]
        
        if path.startswith('~'):
            if user == 'root':
                result = f'{disk}/root'.split('/')
            else:
                result = f'{disk}/home/{user}'.split('/')
            path_parts = path_parts[1:] if len(path_parts) > 1 else []
        elif path.startswith('disk'):
            result = [disk]
            p = path.split('/')
            if p[0] != disk:
                if f'{disk}.db' in os.listdir(disks):
                    result = [p[0]]
                else:
                    return False
            else:
                result = [disk]
            path_parts = path_parts[1:] if len(path_parts) > 1 else []
        else:
            result = cwd.split('/')
        
        for i in path_parts:
            if i == '' or i == '.':
                continue
            elif i == '..':
                if len(result) > 1:
                    result.pop()
            else:
                result.append(i)

        if not result[0].startswith('disk'):
            result.insert(0, cwd)
        else:
            if result[0] != disk:
                if f'{disk}.db' in os.listdir(disks):
                    pass
                else:
                    return False
            else:
                pass
        
        return '/'.join(result)

    def update_permission(self, path, perms):
        if 'root' in self.curr_user_groups:
            memu.update_permission(path, perms)
            return True
        else:
            return False

    def clear_display(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')

class Boot:
    def __init__(self):
        self.is_running = False
        self.system_name = 'muskatos'
        self.version = '26.0'
    
    def boot(self):
        self.is_running = True
        memu.clear_display()

        print(f"[ {colors['GREEN']}OK{colors['RESET']} ] Booting from {disk}...")

        if not memu.get_info(f'{disk}/config/users.json'):
            memu.mk(f'{disk}/config', 'users.json', 'file', 'r')

            # Only for live system
            users = {
                'root': {
                    'password': 'root',
                    'groups': ['users', 'sudoers', 'root'],
                    'home': f'{disk}/root'
                },
                'live': {
                    'password': 'live',
                    'groups': ['users', 'sudoers'],
                    'home': f'{disk}/home/live'
                }
            }
            data = json.dumps(users, indent=4)
            memu.write_file(f'{disk}/config/users.json', data)

            memu.mk(disk, 'root', 'folder', 'r')
            memu.mk(f'{disk}/home', 'live', 'folder', 'r,w')
        print(f'[ {colors['GREEN']}OK{colors['RESET']} ] Initialized users')

        if not memu.get_info(f'{disk}/usr/curr_user'):
            memu.mk(f'{disk}/usr', 'curr_user', 'file', 'r')
        memu.write_file(f'{disk}/usr/curr_user', '')
        print(f'[ {colors['GREEN']}OK{colors['RESET']} ] Reset current user')

        print(f'[ {colors['GREEN']}OK{colors['RESET']} ] Initializing shell...')
        memu.clear_display()

        self.login()

        memu.clear_display()
        print(f'\n* {colors['BLUE']}MuskatOS {self.version}{colors['RESET']}\n')
        self.start_program(f'{disk}/programs/muskatya_shell.py')

    def start_program(self, path, command = False):
        if path == f'{disk}/programs/su.py' or path == f'{disk}/programs/tetstrap.py':
            context = {
                'command': command,
                'memu': memu,
                'boot': self,
                'disk': disk,
                'colors': colors,
                'disks': os.listdir(disks),
                'memu_path': memu_path
            }
        
        else:
            context = {
                'command': command,
                'memu': Memu_Patched(),
                'boot': self,
                'disk': disk,
                'disks': os.listdir(disks),
                'colors': colors,
                'memu_path': memu_path
            }

        program = memu.get_info(path)
        content = program.get('content')

        try:
            exec(content, context)
            return True
        except Exception as e:
            print(f'error when executing {path}: {e}')
            return False

    def login(self):
        try:
            users_raw = memu.get_info(f'{disk}/config/users.json')['content']
            users = json.loads(users_raw)

            user = input('username: ')
            password = input('password: ')

            if user in users and password == users[user]['password']:
                memu.write_file(f'{disk}/usr/curr_user', user)
                if not memu.get_info(f'{disk}/usr/cwd'):
                    memu.mk(f'{disk}/usr', 'cwd', 'file', 'r,w')
                memu.write_file(f'{disk}/usr/cwd', users[user]['home'])
            else:
                print('incorrect username or password, try again\n')
                self.login()
        except KeyboardInterrupt:
            print('\n')
            self.login()
    
    def shutdown(self):
        print('Goodbye!\n')
        self.is_running = False
        return True

Boot().boot()
