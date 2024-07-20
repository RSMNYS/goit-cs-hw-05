import asyncio
import aiofiles
import aiofiles.os
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def copy_file(src_path, dest_path):
    async with aiofiles.open(src_path, 'rb') as src_file:
        content = await src_file.read()

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        await aiofiles.os.makedirs(dest_dir)

    async with aiofiles.open(dest_path, 'wb') as dest_file:
        await dest_file.write(content)
    logger.info(f'Copied {src_path} to {dest_path}')

async def read_folder(source_folder, dest_folder):
    for root, _, files in os.walk(source_folder):
        tasks = []
        for file in files:
            src_file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1][1:]
            dest_file_path = os.path.join(dest_folder, extension, file)
            tasks.append(copy_file(src_file_path, dest_file_path))
        await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description='Asynchronously sort files by extension')
    parser.add_argument('source_folder', help='Source folder to read files from')
    parser.add_argument('dest_folder', help='Destination folder to sort files into')
    args = parser.parse_args()

    asyncio.run(read_folder(args.source_folder, args.dest_folder))

if __name__ == '__main__':
    main()