import os
import pandas as pd
import numpy as np
import subprocess

import argparse

def get_label_groups(label_path="./labeled-data"):
    label_groups = []
    for dir in os.listdir(label_path):
        if dir.endswith("_labeled"):
            continue

        label_group = {}
        label_group["name"] = dir
        
        csv_path = None
        # h5_file = None
        png_paths = []
        for file in os.listdir(os.path.join(label_path, dir)):
            if file.endswith(".png"):
                png_paths.append(os.path.join(label_path, dir, file))
            elif file.endswith(".csv"):
                csv_path = os.path.join(label_path, dir, file)
            # elif file.endswith(".h5"):
            #     h5_file = os.path.join(label_path, dir, file)
                
        label_group["csv_path"] = csv_path
        label_group["png_paths"] = png_paths

        label_groups.append(label_group)
    return label_groups

def make_dest_dir(dest_dir="./labeled-data-resized"):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

def resize_png_in_group(png_paths=[],width=960,height=-1,group_name="",dest_dir="./labeled-data-resized"):
    make_dest_dir(os.path.join(dest_dir,group_name))
    for png_path in png_paths:
        command = f'ffmpeg -y -i "{png_path}" -vf "scale={width}:{height}" -frames:v 1 -update 1 "{os.path.join(dest_dir,group_name,os.path.basename(png_path))}"'
        subprocess.run(command, shell=True)

def resize_csv_in_group(csv_path="",width_ratio=1,height_ratio=1,group_name="",dest_dir="./labeled-data-resized"):
    df = pd.read_csv(csv_path,header=None)
    df_simplified = df.copy()
    
    df_simplified.columns = df_simplified.iloc[1].astype(str) + "_" + df_simplified.iloc[2].astype(str)
    df_simplified = df_simplified.drop([0,1,2])

    df_simplified.index = np.asarray(df_simplified.iloc[:,2].astype(str))

    df_simplified = df_simplified.drop(df_simplified.columns[0:3], axis=1)

    for col_name in df_simplified.columns:
        if col_name.endswith("_x"):
            df_simplified[col_name] = df_simplified[col_name].astype(float)
            df_simplified[col_name] = df_simplified[col_name] * width_ratio
        elif col_name.endswith("_y"):
            df_simplified[col_name] = df_simplified[col_name].astype(float)
            df_simplified[col_name] = df_simplified[col_name] * height_ratio

    left_part = df.iloc[3:, :3]
    left_part.index = df_simplified.index

    df_simplified = pd.concat([left_part, df_simplified], axis=1, ignore_index=True)
    df_simplified = pd.concat([df.iloc[:3], df_simplified], axis=0)

    df_simplified.to_csv(os.path.join(dest_dir,group_name,os.path.basename(csv_path)),index=False,header=False)

def resize_all_groups(label_path="./labeled-data",ratio=1,width=-1,height=-1,dest_dir="./labeled-data-resized"):
    label_groups = get_label_groups(label_path)
    for label_group in label_groups:
        png_sample_path = label_group["png_paths"][0]
        command = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1:nk=1 "{png_sample_path}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        width_ori = result.stdout.split("\n")[0]
        height_ori = result.stdout.split("\n")[1]
        width_ori = int(width_ori)
        height_ori = int(height_ori)

        if width == -1 and height == -1:
            width = width_ori * ratio
            height = height_ori * ratio

            width = round(width)
            height = round(height)

        elif width != -1 and height == -1:
            ratio = width / width_ori
            height = round(height_ori * ratio)

        elif width == -1 and height != -1:
            ratio = height / height_ori
            width = round(width_ori * ratio)

        
        width_ratio = width / width_ori
        height_ratio = height / height_ori
        
        resize_png_in_group(label_group["png_paths"],width,height,label_group["name"],dest_dir)
        resize_csv_in_group(label_group["csv_path"],width_ratio,height_ratio,label_group["name"],dest_dir)

def backup_label_data(label_path="./labeled-data"):
    if os.path.exists(label_path + "-ori"):
        backup_label_data(label_path=label_path+"-ori")
    os.rename(label_path, label_path+"-ori")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--label_path", type=str, default="./labeled-data")
    parser.add_argument("--ratio", type=float, default=1)
    parser.add_argument("--width", type=int, default=-1)
    parser.add_argument("--height", type=int, default=-1)
    parser.add_argument("--dest_dir", type=str, default="./labeled-data-resized")
    parser.add_argument("--convertcsv2h5", type=str, default="no")
    parser.add_argument("--config_path", type=str, default="./config.yaml")

    args = parser.parse_args()

    resize_all_groups(args.label_path,args.ratio,args.width,args.height,args.dest_dir)

    if args.convertcsv2h5 == "yes":
        import deeplabcut

        label_path_current = os.path.join(os.path.dirname(args.label_path),"labeled-data")
        backup_label_data(label_path=label_path_current)
        os.rename(args.dest_dir, label_path_current)

        deeplabcut.convertcsv2h5(args.config_path,userfeedback=False)
