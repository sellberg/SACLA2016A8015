# SACLA2016A8015
Data analysis repository for SACLA experiment between June 23-26, 2016 (proposal number: 2016A8015)

--------------------------------------------------------------------------------

DataConvert
-----------

- VPN into your SACLA account using CISCO:
  
  `hpc.spring8.or.jp`

- Login to one of the analysis nodes at SACLA:

  `ssh -X fperakis@xhpcfep`
  
  `qsub -I -vDISPLAY`

- Run `MakeTagList` to extract tag numbers from data:

  `MakeTagList -b 3 -r 219560 -inp condition0001.txt -out tag_number0001.list`

- Run `DataConvert4` to extract the data to HDF5 format:

  #`DataConvert4 -dir ~/data/test -o 259782.h5 -each -mode 30 -r 259782 -starttag 447317100 -endtag 447352620`
  `DataConvert4 -f test0001.conf -l tag_number0001.list -dir ./ -o test0001.h5`

- Run `DataCompress3.py` using Python 2.7 to produce averages for each scan position:

  `python2.7 dataCompress3.py -f 259782.h5 -c run259782_out.csv -a`

Information
-----------

- Check run status in experiment spreadsheet on [Google Drive](https://docs.google.com/spreadsheets/d/1mlTXdHCwUw_FIHRlHByn0cMgm1xvo-ZFaNCFqEkugac/edit?usp=sharing)
  `Data` sheet shows login information
  `Runs` sheet shows run information

- Check experiment run log on [Google Drive](https://docs.google.com/document/d/1R8stG8Zd-NlBmGYMFF89Fu7rCpGJ6E7tZLkVuVlXT2Y/edit?usp=sharing)

- Check data analysis information at [HPC](http://xhpcfep.hpc.spring8.or.jp/manuals/)
