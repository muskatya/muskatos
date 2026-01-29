import json

class PASSWD:
    def __init__(self):
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        self.users = json.loads(memu.get_info(f'{disk}/config/users.json')['content'])
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def passwd(self):
        if not 'root' in self.curr_user_groups:
            print('adduser: you don\'t have permissions to add new users')
            return

        try:
            user = command.split()[1]
        except IndexError:
            print('passwd: missing user to change password')
            print('usage: passwd <user>')
            return

        if not user in self.users:
            print('passwd: user doesn\'t exist')
            return
        
        password = input('new password: ')

        self.users[user]['password'] = str(password)

        memu.write_file(f'{disk}/config/users.json', json.dumps(self.users))

PASSWD().passwd()
