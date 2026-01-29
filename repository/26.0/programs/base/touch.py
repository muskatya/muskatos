import json

parts = command.split()

class Touch:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def touch(self):
        try:
            path = parts[1]
        except IndexError:
            print('touch: missing file to create')
            print('usage: touch <file name or path to file>')
            return

        path = memu.get_abs_path(path)

        name = path.split('/')[-1]

        if memu.get_info(path):
            print('touch: file already exists')
            return

        path_parts = path.split('/')
        path_parts.pop(-1)
        parent = '/'.join(path_parts)
        parent_info = memu.get_info(parent)
        if not parent_info:
            print(f'touch: cannot access parent \'{parent}\': No such file or directory')
            return
        parent_perms = parent_info['permissions'].split(',')

        if parent_info['type'] != 'folder':
            print('touch: parent is not a directory')
            return

        if not 'w' in parent_perms and not 'root' in self.curr_user_groups:
            print(f'touch: you don\'t have permissions to make files in {parent_info['path']}')
            return

        if not memu.mk(parent, name, 'file', 'r,w'):
            print(f'touch: something went wrong when making {path}')

Touch().touch()
