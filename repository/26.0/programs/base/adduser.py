import json

class Adduser:
    def __init__(self):
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        self.users = json.loads(memu.get_info(f'{disk}/config/users.json')['content'])
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def adduser(self):
        if not 'root' in self.curr_user_groups:
            print('adduser: you don\'t have permissions to add new users')
            return

        try:
            user = command.split()[1]
        except IndexError:
            print('adduser: missing user to add')
            print('usage: adduser <user> <groups>')
            return

        if user in self.users:
            print('adduser: user already exists')
            return

        try:
            groups = command.split()[2]
            groups = groups.split(',')
            for i in groups:
                if i != 'users' and i != 'root' and i != 'sudoers':
                    print('adduser: incorrect user groups')
                    return
            if not 'users' in groups:
                print('adduser: users group must be set at least')
                return
        except IndexError:
            print('adduser: missing user groups to set')
            print('usage: adduser <user> <groups>')
            return
        
        if not user == 'root':
            self.users[user] = {
                'password': '',
                'groups': groups,
                'home': f'{disk}/home/{user}'
            }
        else:
            self.users[user] = {
                'password': '',
                'groups': groups,
                'home': f'{disk}/root'
            }

        if user != 'root':
            memu.mk(f'{disk}/home', user, 'folder', 'r,w')
        else:
            memu.mk(disk, 'root', 'folder', 'r')
        memu.write_file(f'{disk}/config/users.json', json.dumps(self.users))

Adduser().adduser()
