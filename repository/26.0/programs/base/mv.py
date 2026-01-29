import json

parts = command.split()

class CP:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def cp(self):
        try:
            path = parts[1]
        except IndexError:
            print('mv: missing source directory or file to move')
            print('usage: mv <source> <dest>')
            return

        try:
            dest = parts[2]
        except IndexError:
            print('mv: missing destination path to move')
            print('usage: mv <source> <dest>')
            return

        path = memu.get_abs_path(path)

        info = memu.get_info(path)
        children = memu.get_children(path)

        dest = memu.get_abs_path(dest)
        dest_info = memu.get_info(dest)

        if not dest_info:
            print('mv: destination directory path does not exist')
            return

        if dest_info['type'] != 'folder':
            print(f'mv: {dest} is not a folder')
            return           
        
        if not info:
            print('mv: source object does not exist')
            return

        if info['type'] == 'folder' and children:
            print(f'mv: {path} is not empty')
            return

        if not 'w' in info['permissions'].split(',') and not 'root' in self.curr_user_groups:
            print(f'mv: you don\'t have permission to move {path}')
            return

        if not 'w' in dest_info['permissions'].split(',') and not 'root' in self.curr_user_groups:
            print(f'mv: you don\'t have permission to move objects into {path}')
            return

        memu.mk(dest, info['name'], info['type'], info['permissions'])
        if info['type'] == 'file':
            memu.write_file(f'{dest}/{info['name']}', info['content'])
        memu.rm(path)

CP().cp()
