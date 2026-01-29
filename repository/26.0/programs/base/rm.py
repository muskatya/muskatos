import json

parts = command.split()

class RM:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def rm(self):
        try:
            path = parts[1]
        except IndexError:
            print('rm: missing file to remove')
            print('usage: rm <file>')
            return

        path = memu.get_abs_path(path)

        info = memu.get_info(path)
        children = memu.get_children(path)
        
        if not info:
            print('rm: file does not exist')
            return

        if info['type'] != 'file':
            print(f'rm: {path} is not a file')
            return

        if not 'w' in info['permissions'].split(',') and not 'root' in self.curr_user_groups:
            print(f'rm: you don\'t have permission to remove {path}')
            return

        if not memu.rm(path):
            print(f'rm: something went wrong when removing {path}')

RM().rm()
