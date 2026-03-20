import sys, os, os.path, traceback


class ScanRoMMPath():
    # Class scans the RoMM path for games supported by PlayStation 3. When the game is detected, class creates a symbolic link at proper PS3NetSrv path

    def __init__(self, romm_path='/ps3netsrv/ROMM_LIBRARY/', ps3netsrv_path = '/ps3netsrv/'):
        # Init can handle 2 arguments
        #
        # | arg            | default value            |
        # |----------------|--------------------------|
        # | romm_path      | /ps3netsrv/ROMM_LIBRARY/ |
        # | ps3netsrv_path | /ps3netsrv/              |
        #

        self.romm_path = romm_path
        self.ps3netsrv_path = ps3netsrv_path


    def _find(self, path, type):
        # Returns list of files paths with defined extension in given path
        items = [item for item in os.listdir(path) if str.lower(item).endswith(type)]
        return [os.path.join(path, item) for item in items]


    def _scan(self):
        # Scan follows RoMM and PS3NetSrv folders structure
        # RoMM folder structure doc: https://docs.romm.app/latest/Getting-Started/Folder-Structure/
        # PS3NetSrv doc: https://github.com/aldostools/webMAN-MOD/wiki/~-PS3-NET-Server

        # Supported platforms and mapping between RoMM and PS3NetSrv
        platforms = ['psp', 'ps3', 'ps2', 'ps']
        dir_mapping = {
            'psp': 'PSPISO',
            'ps3': 'PS3ISO',
            'ps2': 'PS2ISO',
            'ps':  'PSXISO'
        }

        for platform in platforms:
            # Scans each supported platform
            platform_path = os.path.join(self.romm_path, platform)

            if not os.path.exists(platform_path):
                # If platform is not defined at RoMM - skip
                continue

            # Generic ISOs scan for PSP, PS3, PS2, PSX at root dir
            isoGames = self._find(platform_path, '.iso')

            if platform == 'ps3':
            # PS3NetSrv supports 3 variations for PlayStation 3: PS3ISO, GAME, PKG
            # Following code covers GAME and PKG at platforms root dir as ISOs are generic for PSP, PS3, PS2, PSX
                pkgFiles = self._find(platform_path, '.pkg')
                # To do: add support for game folders

            dirs = [item for item in os.listdir(platform_path) if os.path.isdir(os.path.join(platform_path, item))]
            for dir in dirs:
                # Scans subdirs at platforms root dir

                # Generic ISOs scan for PSP, PS3, PS2, PSX at platforms subdirs
                isoGames += self._find(os.path.join(platform_path, dir), '.iso')

                if platform == 'ps3':
                # PS3NetSrv supports 3 variations for PlayStation 3: PS3ISO, GAME, PKG
                # Following code covers GAME and PKG at platforms subdirs as ISOs are generic for PSP, PS3, PS2, PSX
                # Also, RoMM prefers to store DLC at a dedicated DLC dir at the game location
                # Following code covers PKG stored at DLC folder
                    pkgFiles += self._find(os.path.join(platform_path, dir), '.pkg')
                    # To do: add support for game folders

                    if os.path.exists(platform_path + '/' + dir + '/dlc'):
                        pkgFiles += self._find(os.path.join(platform_path, dir + '/dlc'), '.pkg')

            # Generic symbolic link creation for PSP, PS3, PS2, PSX ISOs at PS3NetSrv location
            [os.symlink(isoGame, os.path.join(self.ps3netsrv_path, dir_mapping[platform] + "/" + os.path.basename(isoGame))) for isoGame in isoGames]

            if platform == 'ps3':
                # PS3NetSrv supports 3 variations for PlayStation 3: PS3ISO, GAME, PKG
                # Following code covers symbolic link creation for GAME and PKG at PS3NetSrv location
                [os.symlink(pkgFile, os.path.join(self.ps3netsrv_path, "PKG/" + os.path.basename(pkgFile))) for pkgFile in pkgFiles]


    def run(self):
        # Handle errors
        # To do: enhance handling
        try:
            self._scan()
        except Exception as e:
            print(traceback.format_exc())


if __name__ == '__main__':
    # Main script
    # To do: enhance args handling
    try:
        if sys.argv[1]: romm_path = sys.argv[1] 
        if sys.argv[2]: ps3netsrv_path = sys.argv[2]
    except:
        romm_path = None
        ps3netsrv_path = None

    ScanRoMMPath(romm_path, ps3netsrv_path).run() if romm_path and ps3netsrv_path else ScanRoMMPath().run()