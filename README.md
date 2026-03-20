<div align="center">
  
  ![banner](https://github.com/AccuraHub/RomM-PS3NetSrv-Cross-Mapping/blob/main/banner.png?raw=true)

  ### Store and play your ROMs with class

  ![Static Badge](https://img.shields.io/badge/Phase-Under%20development-gold)
   
</div>

# Overview
<div align="justify">
  
[PS3NetSrv](https://github.com/aldostools/webMAN-MOD/) is a wonderful tool that allows us to easily run our ROMs over the network, but it lacks library management. On the other hand, we have a modern [RomM](https://romm.app/) for managing ROMs collection - so why not combine the features of both projects?

**RomM-PS3NetSrv-Cross-Mapping** is an simple python script that maps RomM folder structure to PS3NetSrv - simply by creating symbolic links at PS3NetSrv path.

</div>

## How it works
Script scans the RomM library and then links supported items to the appropriate PS3NetSrv folders inside docker container.

## Usage
> [!IMPORTANT]
> This script is in the development phase and does not have full error handling. Use with caution!

```bash
git clone https://github.com/AccuraHub/RomM-PS3NetSrv-Cross-Mapping.git
cd RomM-PS3NetSrv-Cross-Mapping
python ./RomM-PS3NetSrv-Cross-Mapping.py "/romm/library/roms/" "/ps3netsrv"
```
### Arguments
| Variable | Default value | Description |
|---|---|---|
| argv[1] | `/ps3netsrv/ROMM_LIBRARY/` | path for RomM library |
| argv[2] | `/ps3netsrv` | path for PS3NetSrv |