import json

parts = command.split()

class CHMod:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def chmod(self):
        try:
            path = parts[2]
        except IndexError:
            print('chmod: missing object to chmod')
            print('usage: chmod <permissions> <object name or path to the object>')
            return
        try:
            perms = parts[1]
        except IndexError:
            print('chmod: missing permissions to set')
            print('usage: chmod <permissions> <object name or path to the object>')
            return

        if not 'root' in self.curr_user_groups:
            print('chmod: you don\'t have permissions to change file permissions')
        
        path = memu.get_abs_path(path)

        name = path.split('/')[-1]

        perms = perms.split(',')

        perms_check = perms
        if not 'r' in perms:
            print('chmod: at least object must have read permission')
            return

        perms.pop(perms.index('r'))

        if perms != [] and not 'w' in perms:
            print('chmod: incorrect permissions')
            return

        perms.append('r')

        memu.update_permission(path, ','.join(perms))



CHMod().chmod()
