#!/usr/bin/env python3

import argparse
import errno
import glob
import os

import update_payload
from update_payload import applier

os.environ['LD_LIBRARY_PATH'] = './lib64/'

def list_content(payload_file_name):
    with open(payload_file_name, 'rb') as payload_file:
        payload = update_payload.Payload(payload_file)
        payload.Init()

        for part in payload.manifest.partitions:
            print("{} ({} bytes)".format(part.partition_name,
                                         part.new_partition_info.size))


def extract(payload_file_name, output_dir="output", old_dir="old", partition_names=None, skip_hash=None, ignore_block_size=None):
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for i in glob.glob(old_dir + '/*.img'):
        os.rename(i, i[:-4])
    
    with open(payload_file_name, 'rb') as payload_file:
        payload = update_payload.Payload(payload_file)
        payload.Init()

        helper = applier.PayloadApplier(payload, ignore_block_size)
        for part in payload.manifest.partitions:
            if partition_names and part.partition_name not in partition_names:
                continue
            print("Extracting {}".format(part.partition_name))
            output_file = os.path.join(output_dir, part.partition_name)
            if payload.IsDelta():
                old_file    = os.path.join(old_dir,    part.partition_name)
                helper._ApplyToPartition(
                    part.operations, part.partition_name,
                    'install_operations', output_file,
                    part.new_partition_info, old_file,
                    part.old_partition_info, skip_hash)
            else:
                helper._ApplyToPartition(
                    part.operations, part.partition_name,
                    'install_operations', output_file,
                    part.new_partition_info,
                    skip_hash=skip_hash)

    for i in glob.glob(old_dir + '/*'):
        os.rename(i, i + '.img')

    for i in glob.glob(output_dir + '/*'):
        os.rename(i, i + '.img')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", metavar="payload.bin",
                        help="Path to the payload.bin")
    parser.add_argument("--output_dir", default="output",
                        help="Output directory")
    parser.add_argument("--old_dir", default="old",
                        help="Old directory")
    parser.add_argument("--partitions", type=str, nargs='+',
                        help="Name of the partitions to extract")
    parser.add_argument("--list_partitions", action="store_true",
                        help="List the partitions included in the payload.bin")
    parser.add_argument("--skip_hash", action="store_true",
                        help="Skip the hash check for individual img files")
    parser.add_argument("--ignore_block_size", action="store_true",
                        help="Ignore block size")

    args = parser.parse_args()
    if args.list_partitions:
        list_content(args.payload)
    else:
        extract(args.payload, args.output_dir, args.old_dir, args.partitions, args.skip_hash, args.ignore_block_size)
