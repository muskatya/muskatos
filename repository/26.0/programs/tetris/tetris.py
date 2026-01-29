import json
import os
from pathlib import Path

parts = command.split(' ', 2)

class Tetris:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def tetris(self):
        try:
            args = parts[1]
        except IndexError:
            print('tetris: missing arguments')
            return

        try:
            packages = parts[2].split()
        except IndexError:
            print('tetris: missing packages to install')
            return

        if args == '-S':
            if not 'root' in self.curr_user_groups:
                print(f'tetris: you don\'t have permissions to install packages')
                return

            for package in packages:
                if package == 'base/memuboot':
                    if memu.get_info(f'{disk}/memu/boot.py'):
                        print(f'memuboot.py is already installed - reinstalling')
                        memu.rm(f'{disk}/memu/boot.py')
                        memu.rm(f'{disk}/memu')
                    
                    memu.mk(tdisk, 'memu', 'folder', 'r')
                    memu.mk(f'{disk}/memu', 'boot.py', 'file', 'r')
                    with open((Path(memu_path) / 'repository' / boot.version / 'programs' / 'base' / 'memu_boot.py'), 'r') as f:
                        pkg_data = f.read()
                    memu.write_file(f'{disk}/memu/boot.py', pkg_data)
                    print(f'memuboot.py was successfully installed')

                else:
                    pkg_parts = package.split('/')

                    if len(pkg_parts) > 2:
                        print('tetris: incorrect package group to install')
                        return

                    path = pkg_parts[0]
                    try:
                        name = pkg_parts[1]
                    except IndexError:
                        name = False

                    if not name:
                        if (Path(memu_path) / 'repository' / boot.version / 'programs' / path).exists():
                            pkgs = os.listdir(Path(memu_path) / 'repository' / boot.version / 'programs' / path)
                            
                            if 'memu_boot.py' in pkgs:
                                if memu.get_info(f'{disk}/memu/boot.py'):
                                    print(f'memuboot.py is already installed - reinstalling')
                                    memu.rm(f'{disk}/memu/boot.py')
                                    memu.rm(f'{disk}/memu')
                                
                                memu.mk(disk, 'memu', 'folder', 'r')
                                memu.mk(f'{disk}/memu', 'boot.py', 'file', 'r')
                                with open((Path(memu_path) / 'repository' / boot.version / 'programs' / 'base' / 'memu_boot.py'), 'r') as f:
                                    pkg_data = f.read()
                                memu.write_file(f'{disk}/memu/boot.py', pkg_data)
                                print(f'memuboot.py was successfully installed')
                                pkgs.pop(pkgs.index('memu_boot.py'))
                            
                            for pkg in pkgs:
                                if (Path(memu_path) / 'repository' / boot.version / 'programs' / path / pkg).exists() and pkg != 'memu_boot.py' and pkg != 'memu_boot_live.py' and pkg != 'tetstrap.py' and pkg != 'muskatos':
                                    if memu.get_info(f'{disk}/programs/{pkg}'):
                                        print(f'{pkg} is already installed - reinstalling')
                                        memu.rm(f'{disk}/programs/{pkg}')

                                    memu.mk(f'{disk}/programs', pkg, 'file', 'r')
                                    with open((Path(memu_path) / 'repository' / boot.version / 'programs' / path / pkg), 'r') as f:
                                        pkg_data = f.read()
                                    memu.write_file(f'{disk}/programs/{pkg}', pkg_data)
                                    print(f'{pkg} was successfully installed')
                            return
                        else:
                            print('tetris: incorrect package path to install')
                            return

                    if (Path(memu_path) / 'repository' / boot.version / 'programs' / path).exists():
                        if (Path(memu_path) / 'repository' / boot.version / 'programs' / path / f'{name}.py').exists() and f'{name}.py' != 'memu_boot.py' and f'{name}.py' != 'memu_boot_live.py' and f'{name}.py' != 'tetstrap.py' and f'{name}.py' != 'muskatos':
                            pkg = f'{name}.py'

                            if memu.get_info(f'{disk}/programs/{pkg}'):
                                print(f'{pkg} is already installed - reinstalling')
                                memu.rm(f'{disk}/programs/{pkg}')

                            memu.mk(f'{disk}/programs', pkg, 'file', 'r')
                            with open((Path(memu_path) / 'repository' / boot.version / 'programs' / path / pkg), 'r') as f:
                                pkg_data = f.read()
                            memu.write_file(f'{disk}/programs/{pkg}', pkg_data)
                            print(f'{pkg} was successfully installed')
                        else:
                            print('tetris: incorrect package name to install')
                            return    
                    else:
                        print('tetris: incorrect package path to install')
                        return

        elif args == '-R':
            if not 'root' in self.curr_user_groups:
                print(f'tetris: you don\'t have permissions to install packages')
                return
            
            for pkg in packages:
                if memu.get_info(f'{disk}/programs/{pkg}.py'):
                    memu.rm(f'{disk}/programs/{pkg}.py')
                    print(f'successfully removed {pkg}')
                else:
                    print(f'tetris: {pkg} does not exist')

        elif args == '--help':
            print('args: -S - installs package, -R - removes package')

Tetris().tetris()
