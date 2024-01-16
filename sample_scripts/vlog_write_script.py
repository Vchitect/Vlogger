import argparse
from omegaconf import OmegaConf
import os
from vlogger.planning_utils.gpt4_utils import (ExtractProtagonist)


def main(args):
    story_path = args.story_path
    save_script_path = os.path.join(story_path.rsplit('/', 1)[0], "script")
    if not os.path.exists(save_script_path):
            os.makedirs(save_script_path)
    with open(story_path, "r") as story_file:
        story = story_file.read()
        
    # summerize protagonists and places
    protagonists_places_file_path = os.path.join(save_script_path, "protagonists_places.txt")
    character_places = ExtractProtagonist(story, protagonists_places_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./configs/vlog_write_script.yaml")
    args = parser.parse_args()
    omega_conf = OmegaConf.load(args.config)
    main(omega_conf)