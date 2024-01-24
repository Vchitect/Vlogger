import openai
import re
import ast

# Enter your openai key here
# Allow multiple keys to be filled in to prevent the number of visits from being restricted
openai_key = [""]

global_key_num = 0


def smart_openai_key():
    global global_key_num
    global openai_key
    openai.api_key = openai_key[global_key_num]
    global_key_num += 1
    global_key_num %= len(openai_key)


def json_completion(prompt):
    try_time = 3
    for i in range(try_time):
        try:
            smart_openai_key()
            completions = openai.ChatCompletion.create(
                model="gpt-4",  # "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": "["}
                ]
            )
            break
        except:
            print("key error: ", openai.api_key)

    message = completions['choices'][0]['message']['content']
    return message


def ExtractProtagonist(story, file_path):
    ask = f"""The following is a story enclosed in three single quotes '''{story}''', please help me summarize all the main protagonists and places that appear in the story.""" \
          f"""Provide me the answer in JSON format(do not answer anything else) with the following keys: id, name, description.""" \
          f"""You must answer like the content in following three single quotes:""" \
          f"""'''[
    {{
        "id": 1,
        "name": "Lincoln",
        "description": "(the physical characteristics description of Lincoln)",
    }},
    {{
        "id": 2,
        "name": "Everest"
        "description": "(the physical characteristics description of Everest)",
    }}
]'''""" \
          f"""The descriptions of the protagonists should adhere to the following guidelines:\n""" \
          f"""1.The description should be as simple as possible, as long as it doesn't conflict with the story\n""" \
          f"""2.Do not include another thing in the description of one thing\n""" \
          f"""3.Most important: Only the physical characteristics of the character or place need to be described in detail, such as color and class label, no mood description is required, etc. """
    
    answer = json_completion(ask)
    answer = answer.strip("'")
    answer = answer.strip("\n")
    answer = answer.strip("[")
    answer = answer.strip("\n")
    answer = answer.strip("]")
    answer = answer.strip("\n")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = "[\n" + answer + "\n]"
    f = open(file_path, "w")
    f.write(answer)
    f.close()
    protagonists_places_dict = {}
    protagonists_places = ast.literal_eval(answer)
    for protagonist_place in protagonists_places:
        protagonists_places_dict[protagonist_place["name"]] = protagonist_place["description"]
    return protagonists_places_dict


def ExtractAProtagonist(story, file_path):
    ask = f"""The following is a story enclosed in three single quotes '''{story}''', please help me summarize a main protagonist that appear in the story.""" \
          f"""Provide me the answer in JSON format(do not answer anything else) with the following keys: id, name, description.""" \
          f"""You must answer like the content in following three single quotes:""" \
          f"""'''[
    {{
        "id": 1,
        "name": "Lincoln",
        "description": "(the physical characteristics description of Lincoln)",
    }}
]'''""" \
          f"""The descriptions of the protagonist should adhere to the following guidelines:\n""" \
          f"""1.The description should be as simple as possible, as long as it doesn't conflict with the story\n""" \
          f"""2.Most important: Only the physical characteristics of the character need to be described in detail, such as color and class label, no mood description is required, etc. """
    
    answer = json_completion(ask)
    answer = answer.strip("'")
    answer = answer.strip("\n")
    answer = answer.strip("[")
    answer = answer.strip("\n")
    answer = answer.strip("]")
    answer = answer.strip("\n")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = "[\n" + answer + "\n]"
    f = open(file_path, "w")
    f.write(answer)
    f.close()
    protagonists_places_dict = {}
    protagonists_places = ast.literal_eval(answer)
    for protagonist_place in protagonists_places:
        protagonists_places_dict[protagonist_place["name"]] = protagonist_place["description"]
    return protagonists_places_dict


def protagonist_place_reference(video_list, character_places):
    new_video_list = []
    num = 1
    for video in video_list:
        prompt = str(num) + ". " + video
        new_video_list.append(prompt)
        num += 1
    key_list = []
    i = 1
    for key, value in character_places.items():
        key_list.append(str(i) + ". " + key)
        i += 1
    ask = f"""I would like to make a video. Here are this video script in the following three single quotes '''{new_video_list}''', """ \
          f"""Here are some characters and places in the following three single quotes '''{key_list}''', """ \
          f"""Please help me identify the characters or places in the list where each segment of the video script appears""" \
          f"""You can only choose characters and places that match exactly, and you can't choose even the slightest doubt.""" \
          f"""Just answer me the serial number(2 selections are possible, but no more, pick out what you think is most likely. If you select less than 2, you can fill it with 0.)""" \
          f"""Provide me the answer in JSON format(do not answer anything else) with the following keys: video segment id, character/place id.""" \
          f"""You must answer like the content in following three single quotes:""" \
          f"""'''[
    {{
        "video segment id": 1,
        "character/place id": [1, 0],
    }},
    {{
        "video segment id": 2,
        "character/place id": [1, 2],
    }},
    {{
        "video segment id": 3,
        "character/place id": [0, 0],
    }}
]'''"""

    answer = json_completion(ask)
    answer = answer.strip("'")
    answer = answer.strip("\n")
    answer = answer.strip("[")
    answer = answer.strip("\n")
    answer = answer.strip("]")
    answer = answer.strip("\n")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = "[\n" + answer + "\n]"
    f = open("MakeVideo/protagonist_place_reference.txt", "w")
    f.write(answer)
    f.close()
    print(answer)
    reference_list = []
    protagonists_places_reference = ast.literal_eval(answer)
    for protagonist_place_reference in protagonists_places_reference:
        reference_list.append(protagonist_place_reference["character/place id"])
    return reference_list


def protagonist_place_reference1(video_list, character_places, file_path):
    new_video_list = []
    num = 1
    for video in video_list:
        prompt = str(num) + ". " + video
        new_video_list.append(prompt)
        num += 1
    key_list = []
    i = 1
    for key, value in character_places.items():
        key_list.append(str(i) + ". " + key)
        i += 1
    ask = f"""I would like to make a video. Here are this video script in the following three single quotes '''{new_video_list}''', """ \
          f"""Here are some characters and places in the following three single quotes '''{key_list}''', """ \
          f"""Please help me identify the characters or places in the list where each segment of the video script appears""" \
          f"""You can only choose characters and places that match exactly, and you can't choose even the slightest doubt.""" \
          f"""Just answer me the serial number(1 selection is possible, but no more, pick out what you think is most likely. If you select less than 1, you can fill it with 0.)""" \
          f"""Provide me the answer in JSON format(do not answer anything else) with the following keys: video segment id, character/place id.""" \
          f"""You must answer like the content in following three single quotes:""" \
          f"""'''[
        {{
            "video segment id": 1,
            "character/place id": [1],
        }},
        {{
            "video segment id": 2,
            "character/place id": [0],
        }},
        {{
            "video segment id": 3,
            "character/place id": [2],
        }}
        ]'''"""

    answer = json_completion(ask)
    answer = answer.strip("'")
    answer = answer.strip("\n")
    answer = answer.strip("[")
    answer = answer.strip("\n")
    answer = answer.strip("]")
    answer = answer.strip("\n")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = "[\n" + answer + "\n]"
    f = open(file_path, "w")
    f.write(answer)
    f.close()
    # print(answer)
    reference_list = []
    protagonists_places_reference = ast.literal_eval(answer)
    for i, prompt in enumerate(video_list):
        prompt = prompt.lower()
        for key, value in character_places.items():
            if key.lower() in prompt:
                protagonists_places_reference[i]["character/place id"] = [1]
    for protagonist_place_reference in protagonists_places_reference:
        reference_list.append(protagonist_place_reference["character/place id"])
    return reference_list


def split_story(story, file_path):
    ask = f"""The following is a story enclosed in three single quotes '''{story}''' and I would like to request your assistance in """ \
        f"""writing a script for a video based on this story. Provide the script in JSON format(do not answer anything else) with the following keys: video fragment id, video fragment description.""" \
        f"""You must answer like the content in following three single quotes:\n""" \
        f"""'''[
{{
"video fragment id": 1,
"video fragment description": "(the description, describe the characters, actions, and backgrounds in the video fragment)",
}},
{{
"video fragment id": 2,
"video fragment description": "(the description, describe the characters, actions, and backgrounds in the video fragment)",
}}
]'''""" \
        f"""The descriptions of the video segments should adhere to the following guidelines:\n""" \
        f"""1.Fits the original storyline\n""" \
        f"""2.All video fragment descriptions cannot conflict with each other, and the descriptions corresponding to successive fragments in the original story must have a certain continuity\n""" \
        f"""3.The description only needs to describe the visual elements presented, such as the subject, action, background, etc., and do not appear useless descriptions, such as mental activities\n""" \
        f"""Each description should include the subject, place, and action as much as possible.""" \
        f"""Read this script carefully and don't pull down any details.\n""" \
        f"""As more fragment as possible, as detail as possible!\n""" \

    answer = json_completion(ask)
    answer = answer.strip("'")
    answer = answer.strip("\n")
    answer = answer.strip("[")
    answer = answer.strip("\n")
    answer = answer.strip("]")
    answer = answer.strip("\n")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = "[\n" + answer + "\n]"
    f = open(file_path, "w")
    f.write(answer)
    f.close()
    video_fragments = ast.literal_eval(answer)
    video_list = []
    for video_fragment in video_fragments:
        video_list.append(video_fragment["video fragment description"])
    return video_list


def patch_story_scripts(story, video_list, file_path):
    ask = f"""The following is a story enclosed in three single quotes '''{story}'''. I want to make a video according to this story, this is my video production script in the following three single quotes '''{video_list}''', a paragraph in the script corresponds to a clip """ \
          f"""of the video. However, there may be some plots in the story missing, such as important plot missing, or transitions between pictures, please check and complete it for me. """ \
          f"""Provide me the answer in JSON format(do not answer anything else) with the following keys: video fragment id, video fragment description.""" \
          f"""You must must must answer like the content in following three single quotes:\n""" \
          f"""'''[
    {{
        "video fragment id": 1,
        "video fragment description": "(the description)",
    }},
    {{
        "video fragment id": 2,
        "video fragment description": "(the description)",
    }},
    {{
        "video fragment id": 3,
        "video fragment description": "(the description)",
    }}
]'''""" \
          f"""Remember to make sure that the description of each video clip is not long, no more than fifteen words, but there can be so many video clips.\n""" \
          f"""Each description should include the subject, place, and action as much as possible.""" \
          f"""As more fragment as possible, as detail as possible!\n""" \
          f"""Read this script carefully and don't pull down any details.\n"""
        #   f"""Very important!!!: avoid character-to-character interactions and character-to-object interactions in descriptions."""

    answer = json_completion(ask)
    answer = answer.strip("'")
    answer = answer.strip("\n")
    answer = answer.strip("[")
    answer = answer.strip("\n")
    answer = answer.strip("]")
    answer = answer.strip("\n")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = "[\n" + answer + "\n]"
    f = open(file_path, "w")
    f.write(answer)
    f.close()
    video_fragments = ast.literal_eval(answer)
    video_list = []
    for video_fragment in video_fragments:
        video_list.append(video_fragment["video fragment description"])
    return video_list


def refine_story_scripts(video_list, file_path):
    ask = f"""I want to make a video, this is my video production script in the following three single quotes '''{video_list}''', a paragraph in the script corresponds to a clip """ \
          f"""of the video, But the description of some video clips is too complicated, please help me analyze and rewrite a video script, split each description into at least three short descriptions and as more as possible. """ \
          f"""For example, if there are one paragraphs in the script I gave you, then you should split it into fifteen paragraphs.""" \
          f"""Provide me the answer in JSON format(do not answer anything else) with the following keys: video fragment id, video fragment description.""" \
          f"""You must must must answer like the content in following three single quotes:\n""" \
          f"""'''[
    {{
        "video fragment id": 1,
        "video fragment description": "(the description)",
    }},
    {{
        "video fragment id": 2,
        "video fragment description": "(the description)",
    }},
    {{
        "video fragment id": 3,
        "video fragment description": "(the description)",
    }}
]'''""" \
          f"""Remember to make sure that the description of each video clip is not long, no more than ten words, but there can be so many video clips.\n""" \
          f"""Most important thing: Read this script carefully and don't pull down any details.\n""" \
          f"""Ensure that all description statements are as natural and syntactically correct as possible.\n""" \
          f"""Most important: Try to have only one character in the description and avoid complex actions in video fragment description, such as: loaded in, fight, etc.\n""" 

    answer = json_completion(ask)
    answer = answer.strip("'")
    answer = answer.strip("\n")
    answer = answer.strip("[")
    answer = answer.strip("\n")
    answer = answer.strip("]")
    answer = answer.strip("\n")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = answer.strip("'")
    answer = answer.strip("[")
    answer = answer.strip("]")
    answer = "[\n" + answer + "\n]"
    f = open(file_path, "w")
    f.write(answer)
    f.close()
    video_fragments = ast.literal_eval(answer)
    video_list = []
    for video_fragment in video_fragments:
        video_list.append(video_fragment["video fragment description"])
    return video_list


def time_scripts(video_list, file_path):
    try_times = 3
    for i in range(try_times):
        try:
            new_video_list = []
            num = 1
            for video in video_list:
                prompt = str(num) + ". " + video
                new_video_list.append(prompt)
                num += 1
            ask = f"""I want to make a video, this is my video production script in the following three single quotes '''{new_video_list}''', a paragraph in the script corresponds to a clip """ \
                f"""of the video, Now that you know that 16-frame videos have a length of 2 seconds, please help me plan how much time it will take for each video clip to fully interpret the meaning of the script.""" \
                f"""Each clip can only be 10 seconds maximum.""" \
                f"""Provide me the answer in JSON format(do not answer anything else) with the following keys: video fragment id, time.""" \
                f"""You must answer like the content in following three single quotes:\n""" \
                f"""'''[
                {{
                    "video fragment id": 1,
                    "time": 3,
                }},
                {{
                    "video fragment id": 2,
                    "time": 9,
                }},
                {{
                    "video fragment id": 3,
                    "time": 7,
                }},
                {{
                    "video fragment id": 4,
                    "time": 2,
                }},
                ]'''""" \
                f"""Remember that time must be less than 10."""
            answer = json_completion(ask)
            answer = answer.strip("'")
            answer = answer.strip("[")
            answer = answer.strip("]")
            answer = answer.strip("'")
            answer = answer.strip("[")
            answer = answer.strip("]")
            answer = answer.strip("'")
            answer = answer.strip("[")
            answer = answer.strip("]")
            answer = answer.strip("'")
            answer = answer.strip("[")
            answer = answer.strip("]")
            answer = "[\n" + answer + "\n]"
            f = open(file_path, "w")
            f.write(answer)
            f.close()
            time_scripts = ast.literal_eval(answer)
            time_list = []
            for time_script in time_scripts:
                time = time_script["time"]
                if time > 10:
                    time = 10
                time_list.append(time)
            assert len(time_list) == len(video_list)
            return time_list
        except:
            continue
    assert len(time_list) == len(video_list)
    return time_list


def translate_video_script(video_list, file_path):
    try_times = 5
    for i in range(try_times):
        try:
            ask = f"""I want to make a video, this is my video production script in the following three single quotes '''{video_list}''', """ \
                f"""please help me to translate every video fragment description into Chinese.""" \
                f"""Provide me the answer in JSON format(do not answer anything else) with the following keys: 序号, 描述.""" \
                f"""You must must must answer like the content in following three single quotes:\n""" \
                f"""'''[
                {{
                    "序号": 1,
                    "描述": "(视频片段描述)",
                }},
                {{
                    "序号": 2,
                    "描述": "(视频片段描述)",
                }}
                ]'''"""

            answer = json_completion(ask)
            answer = answer.strip("'")
            answer = answer.strip("[")
            answer = answer.strip("]")
            answer = answer.strip("'")
            answer = answer.strip("[")
            answer = answer.strip("]")
            answer = answer.strip("'")
            answer = answer.strip("[")
            answer = answer.strip("]")
            answer = answer.strip("'")
            answer = answer.strip("[")
            answer = answer.strip("]")
            answer = "[\n" + answer + "\n]"
            f = open(file_path, "w")
            f.write(answer)
            f.close()
            video_fragments = ast.literal_eval(answer)
            zh_video_list = []
            for video_fragment in video_fragments:
                zh_video_list.append(video_fragment["描述"])
            assert len(video_list) == len(zh_video_list)
            return zh_video_list
        except:
            continue
    assert len(video_list) == len(zh_video_list)
    return zh_video_list


def readscript(script_file_path):
    with open(script_file_path, "r", encoding='utf-8') as f: 
        script = f.read()
        video_fragments = ast.literal_eval(script)
        video_list = []
        for video_fragment in video_fragments:
            video_list.append(video_fragment["video fragment description"])
    return video_list


def readzhscript(zh_file_path):
    with open(zh_file_path, "r", encoding='utf-8') as f: 
        script = f.read()
        video_fragments = ast.literal_eval(script)
        video_list = []
        for video_fragment in video_fragments:
            video_list.append(video_fragment["描述"])
    return video_list


def readtimescript(time_file_path):
    with open(time_file_path, "r", encoding='utf-8') as f: 
        time_scripts = f.read()
        time_scripts = ast.literal_eval(time_scripts)
        time_list = []
        for time_script in time_scripts:
            frames = time_script["time"]
            time_list.append(frames)
    return time_list
    
    
def readprotagonistscript(protagonist_file_path):
    with open(protagonist_file_path, "r", encoding='utf-8') as f: 
        protagonist_scripts = f.read()
        protagonist_scripts = ast.literal_eval(protagonist_scripts)
        protagonists_places_dict = {}
        for protagonist_script in protagonist_scripts:
            protagonists_places_dict[protagonist_script["name"]] = protagonist_script["description"]
    return protagonists_places_dict
    
    
def readreferencescript(video_list, character_places, reference_file_path):
    new_video_list = []
    num = 1
    for video in video_list:
        prompt = str(num) + ". " + video
        new_video_list.append(prompt)
        num += 1
    key_list = []
    i = 1
    for key, value in character_places.items():
        key_list.append(str(i) + ". " + key)
    with open(reference_file_path, "r", encoding='utf-8') as f: 
        reference_file = f.read()
        reference_list = []
        protagonists_places_reference = ast.literal_eval(reference_file)
        for i, prompt in enumerate(video_list):
            prompt = prompt.lower()
            for j, key in enumerate(key_list):
                if key.lower() in prompt:
                    protagonists_places_reference[i]["character/place id"] = [j + 1]
            
        for protagonist_place_reference in protagonists_places_reference:
            reference_list.append(protagonist_place_reference["character/place id"])
    return reference_list
    
