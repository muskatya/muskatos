import json

class Echo:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def echo(self):
        quotes = command.split()
        if quotes[1].startswith("'"): quotes = 1
        elif quotes[1].startswith('"'): quotes = 2
        else: quotes = False
        if quotes == 1:        
            parts = command.split("'")
        elif quotes == 2:
            parts = command.split('"')
        else:
            parts = [''.join(command)]

        if len(parts) > 1:
            if len(parts) != 3:
                print('echo: incorrect usage of quotes')
                print('usage: echo <text in quotes> >(if you want to write text to file) [file]')
                return

            echo = parts[0].strip()
            text = parts[1]
            options = parts[2].strip().split()

            try:
                option = options[0]
            except IndexError:
                option = False

            try:
                file = options[1]
            except IndexError:
                if option:
                    print('echo: missing file to write')
                    print('usage: echo <text in quotes> >(if you want to write text to file) [file]')
                    return
                else:
                    file = False
                    
        else:
            parts = command.split()
            echo = parts[0]
            try:
                text = parts[1]
            except IndexError:
                print('echo: missing file to write')
                print('usage: echo <text> >(if you want to write text to file) [file]')
                return

            try:
                option = parts[2]
            except IndexError:
                option = False

            try:
                file = parts[3]
            except IndexError:
                if option:
                    print('echo: missing file to write')
                    print('usage: echo <text> >(if you want to write text to file) [file]')
                    return
                else:
                    file = False

        if option and option != '>':
            print('echo: incorrect options')
            print('usage: echo <text> >(if you want to write text to file) [file]')
            return
        
        if not option:
            print(text)
            return

        file = memu.get_abs_path(file)

        path_parts = file.split('/')
        name = path_parts[-1]
        path_parts.pop(-1)
        parent = '/'.join(path_parts)
        file_path = f'{parent}/{name}'

        file_info = memu.get_info(file_path)
        if file_info:
            if 'w' in file_info['permissions'].split(',') or 'root' in self.curr_user_groups:
                memu.write_file(file_path, text)
                return
            else:
                print(f'echo: you don\'t have permissions to edit {file_path}')

            if file_info['type'] != 'file':
                print(f'echo: cannot access {file_path} to write text: it is not file')
        else:
            parent_info = memu.get_info(parent)

            if not parent_info:
                print('echo: cannot access parent: no such file or directory')
                return

            if parent_info['type'] != 'folder':
                print('echo: cannot access parent: it is not folder')
                return

            if not 'w' in parent_info['permissions'].split(',') and not 'root' in self.curr_user_groups:
                print(f'echo: you don\'t have permissions to create files in {parent}')
                return

            memu.mk(parent, name, 'file', 'r,w')
            memu.write_file(file_path, text)

Echo().echo()
            
