import sys

out = sys.stdout

def progress(progress,total):
    percent = 100 * (progress/total)
    intPercent = int(percent)
    bar = "🀰" * intPercent+'-' * int(100-percent)
    out.write(f"\r{bar} {percent:.2f}%")
    if intPercent == 100:
        out.write("\nSuccessfully Downloaded\n")
        out.close()