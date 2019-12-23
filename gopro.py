import argparse
import os
import subprocess
import json


def sync_gopro_to_original(args):
    pass


def convert_to_h264(infile, outfile):
    cmd = ["/usr/bin/ffmpeg", "-i", infile, "-c:a", "copy", "-c:v", "h264_nvenc", "-b:v", "90M", outfile]
    result = subprocess.Popen(cmd)
    out, err = result.communicate()


def get_creation_time(mp4):
    cmd = ["ffprobe", "-v", "quiet",
           mp4, "-print_format",
           "json", "-show_entries",
           "stream=index, codec_type:stream_tags = creation_time:format_tags = creation_time"]

    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    x = json.loads(out)
    return x["streams"][0]["tags"]["creation_time"][:19].replace("-", "_").replace(":", "_").replace("T", "x")


def convert_originals(args):
    orig = [i for i in os.listdir(args.original) if "MP4" in i]
    transforms = os.listdir(args.transformed)

    print(orig, transforms)

    for original in orig:
        path = os.path.join(args.original, original)
        orig_id = original.replace(".MP4", "")
        transformed = sum([orig_id in x for x in transforms])
        if not transformed:
            filename = f"{get_creation_time(path)}_{orig_id}.mp4"
            convert_to_h264(path, os.path.join(args.transformed, filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gopro tools")

    subparsers = parser.add_subparsers(help='actions')

    sync_parser = subparsers.add_parser('sync', help='sync gopro to local original folder')
    sync_parser.set_defaults(func=sync_gopro_to_original)

    convert_parser = subparsers.add_parser('convert', help='convert all original files from the original folder')
    convert_parser.set_defaults(func=convert_originals)
    convert_parser.add_argument('--original', default="/lhome/gvelkey/gopro/original", type=str)
    convert_parser.add_argument('--transformed', default="/lhome/gvelkey/gopro/transformed", type=str)

    args = parser.parse_args()
    args.func(args)
