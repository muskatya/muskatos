import json

class Shell:
    def __init__(self):
        pass
    
    def init_shell(self):
        while boot.is_running == True:
            try:
                self.users = json.loads(memu.get_info(f'{disk}/config/users.json')['content'])
                username = memu.get_info(f'{disk}/usr/curr_user')['content']
                cwd = memu.get_info(f'{disk}/usr/cwd')['content']
                if cwd == self.users[username]['home']:
                    prompt = input(f'{username} [~] {colors['RED']}=> {colors['RESET']}')
                else:
                    prompt = input(f'{username} [{cwd}] {colors['RED']}=> {colors['RESET']}')
                parts = prompt.split()

                if not parts: continue

                if not parts[0].startswith(disk) and not parts[0].startswith('.') and not parts[0].startswith('..') and not parts[0].startswith('~'):
                    path = f'{disk}/programs/{parts[0]}.py'
                else:
                    path = memu.get_abs_path(parts[0])

                program_info = memu.get_info(path)
                if not program_info:
                    print(f'{path} not found')
                    continue

                if program_info['type'] != 'file':
                    print(f'{path}: it is a {program_info['type']}')
                    continue
                
                try:
                    if not boot.start_program(path, prompt):
                        continue
                except KeyboardInterrupt:
                    print(f'\n{path} was cancelled')
                    continue
            except KeyboardInterrupt:
                print('')
                continue

Shell().init_shell()
