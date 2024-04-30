from urllib.error import HTTPError
from pytube import YouTube,Playlist
from math import ceil
import sys
import threading
import progress
import os
import signal


def signal_handler(*_):
   exit()

def exit():
    try:
       sys.exit(0)
    except SystemExit:
       os._exit(0)
   

def getPlaylist():
    try:
        inp = input("Enter playlist url: ")
        if len(inp) == 0 or inp is None or not inp.startswith("https://www.youtube.com/playlist?list="):
            raise ValueError
        return Playlist(inp)
    except ValueError:
        progress.out.write('\nFailed: Invalid url.\n')
        progress.out.close()
        exit()

def getUseOAuth():
    return "y" == input("Use OAuth? (y/n): ")
            

def getOutputPath(playlist):
    try:
        output_path = input("Enter path to download to (leave blank for current directory): ")
        progress.out.write("Playlist getting started...\n")
        folder = playlist.title + "(" + playlist.owner + ")/"
        if output_path:
           return  output_path + "/" +folder 
        else:
            return  folder
    except HTTPError:
        progress.out.write('\nFailed: Playlist not found.\n')
        progress.out.close()
        exit()

def chunkPlaylist(playlist,chunk):
    for i in range(0,len(playlist),chunk):
        yield playlist[i:i+chunk]

def downloader(playlist,complete,total,output_path,useOAuth=False):   
    for i in playlist:
        try:
            yt = YouTube(url=i,use_oauth=useOAuth)
            ys = yt.streams.get_highest_resolution()
            ys.download(
                output_path=output_path
            )
            complete.append(1)
            progress.progress(len(complete),total)
        except Exception as e:
            with open(output_path+"error.log","a+") as error_log:
                error_log.write(f"Failed: Unable to download {i}: {e}\n")
            


def main():
    playlist = getPlaylist()
    outputPath = getOutputPath(playlist)
    useOAuth = getUseOAuth()
    threadCount = os.cpu_count() if os.cpu_count() else 4
    progress.out.write("Playlist Name : {}\nChannel Name  : {}\nTotal Videos  : {}\nTotal Download Treads : {}\nError Log : {}\nEnjoy!\n".format(playlist.title,playlist.owner,playlist.length,threadCount,outputPath+"error.log"))
    allVideoList = [url for url in playlist.video_urls]
    chunkList = list(chunkPlaylist(allVideoList,ceil(len(allVideoList)/threadCount)))
    progress.out.write("Starting Downloading...\n")
    complete = []
    total = len(allVideoList)
    progress.progress(0,total)
    for chunk in chunkList:
        try:
            threading.Thread(target=downloader,args=(chunk,complete,total,outputPath,useOAuth)).start()
        except:
            pass

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, signal_handler)
        main()
    except:
        pass