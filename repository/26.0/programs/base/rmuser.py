import json

class RMUser:
    def __init__(self):
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        self.users = json.loads(memu.get_info(f'{disk}/config/users.json')['content'])
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def rmuser(self):
        if not 'root' in self.curr_user_groups:
            print('rmuser: you don\'t have permissions to remove users')
            return

        try:
            user = command.split()[1]
        except IndexError:
            print('rmuser: missing user to add')
            print('usage: adduser <user>')
            return

        if not user in self.users:
            print('rmuser: user doesn\'t exist')
            return
        
        memu.rm(self.users[user]['home'])
        self.users.pop(user)
        memu.write_file(f'{disk}/config/users.json', json.dumps(self.users))

RMUser().rmuser()
