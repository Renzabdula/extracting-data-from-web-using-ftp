import sys
import json
import time
import schedule
import pandas as pd
from os import environ, remove
from pathlib import Path
from ftplib import FTP_TLS


def get_ftp() -> FTP_TLS:

    # get ftp details
    FTPHOST = environ["FTPHOST"]
    FTPUSER = environ["FTPUSER"]
    FTPPASS = environ["FTPPASS"]

    # return authenticated FTP
    ftp = FTP_TLS(FTPHOST, FTPUSER, FTPPASS)
    ftp.prot_p()
    return ftp


def delete_file(file_source: str | Path):
    remove(file_source)


def read_csv(config: dict) -> pd.DataFrame:
    url = config["URL"]
    params = config["PARAMS"]
    return pd.read_csv(url, **params)


def pipeline():

 # load source configuration
    with open("config.json", "rb") as fp:
        config = json.load(fp)

    # get an authenticated ftp server
    ftp = get_ftp()

    # loop through each config to get the source_name and corresponding source_config
    for source_name, source_config in config.items():
        file_name = Path(source_name + ".CSV")
        df = read_csv(source_config)
        df.to_csv(file_name, index=False)

        print(f'File {file_name} has been downloaded')

        # uploaded the file to ftp folder
        upload_to_ftp(ftp, file_name)
        print(f"FIle {file_name} has been uploaded to ftp")

        # delete the file from ep3.live folder
        delete_file(file_name)
        print(f"File {file_name} has been deleted.")


def upload_to_ftp(ftp: FTP_TLS, file_source: Path):

    with open(file_source, "rb") as fp:
        ftp.storbinary(f"STOR {file_source.name}", fp)


# this is to import the function to reuse in other project
if __name__ == "__main__":

    param = sys.argv[1]

    # for manually run the pipepline
    if param == "manual":
        pipeline()

    elif param == "schedule":
        #schedule the pipeline everyday @ 17:33
        schedule.every().day.at("17:56").do(pipeline)

        while True:
            schedule.run_pending()
            time.sleep(1)
        
    else:
        print("Invalid parameter. App will not run")
