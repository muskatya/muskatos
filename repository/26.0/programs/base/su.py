import json

class SU:
    def __init__(self):
        self.users = json.loads(memu.get_info(f'{disk}/config/users.json')['content'])

    def su(self):
        try:
            user = command.split()[1]
        except IndexError:
            print('su: missing user to change to')
            print('usage: su <user>')
            return

        if user in self.users:
            password = input('password: ')
            if password == self.users[user]['password']:
                memu.write_file(f'{disk}/usr/curr_user', user)
                memu.write_file(f'{disk}/usr/cwd', self.users[user]['home'])
            else:
                print('su: incorrect password, try again')
                return
        else:
            print('su: incorrect username, try again')
            return

SU().su()
