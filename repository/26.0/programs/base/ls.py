parts = command.split()

class LS:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']

    def ls(self, path = False):
        if isinstance(path, list):
            path = path[1]

        if not path:
            path = self.cwd
        else:
            path = memu.get_abs_path(path)

        if path == 'mnt':
            print('ls: access denied')
            return
        
        path_info = memu.get_info(path)

        if not path_info:
            print(f'ls: cannot access \'{path}\': No such file or directory')
            return

        if path_info['type'] != 'folder':
            print(f'ls: {path} is not a directory')
            return

        children = memu.get_children(path)

        if not children:
            return
        
        for child in children:
            child_info = memu.get_info(child)
            perms = {
                'r': f'{colors['GREEN']}r{colors['RESET']}',
                'w': f'{colors['RED']}w{colors['RESET']}'
            }
            
            if child_info['type'] == 'folder':
                name = f'{colors['BLUE']}{child_info['name']}{colors['RESET']}'
                child_perms = f'{colors['BLUE']}d{colors['RESET']}'

            elif child_info['type'] == 'file':
                name = child_info['name']
                child_perms = f'{colors['BRIGHT_BLACK']}.{colors['RESET']}'

            for i in child_info['permissions'].split(','):
                child_perms += perms[i]

            if child_info['size'] == None:
                size = f'{colors['BRIGHT_BLACK']}-{colors['RESET']}'
            else:
                size = f'{colors['CYAN']}{child_info['size']}b{colors['RESET']}'

            date_parts = child_info['creation_date'].split('T')
            date = date_parts[0].split('-')
            time = date_parts[1].split(':')
            months = {
                '01': 'Jan',
                '02': 'Feb',
                '03': 'Mar',
                '04': 'Apr',
                '05': 'May',
                '06': 'Jun',
                '07': 'Jul',
                '08': 'Aug',
                '09': 'Sept',
                '10': 'Oct',
                '11': 'Nov',
                '12': 'Dec'
            }
            cr_time = f'{time[0]}:{time[1]}'
            creation_date = f'{months[date[1]]} {date[2]} {cr_time}'

            print(f'{child_perms} {size} root {colors['BLUE']}{creation_date}{colors['RESET']} {name}')

ls = LS()

if len(parts) > 1:
    ls.ls(parts[1])
else:
    ls.ls()
