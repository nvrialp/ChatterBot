import re
import yaml

def srt_to_yaml(srt_file, yaml_file):
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()

    subtitles = re.findall(r'\d+\n[\d:, -->]+\n(.+?)(?=\n\d+\n|$)', content, re.DOTALL)

    dialogues = []
    for i in range(0, len(subtitles), 2):
        if i + 1 < len(subtitles):
            dialogues.append([subtitles[i].strip().replace('\n', ' '), subtitles[i+1].strip().replace('\n', ' ')])

    with open(yaml_file, 'w', encoding='utf-8') as yaml_out:
        yaml.dump(dialogues, yaml_out, default_flow_style=False, allow_unicode=True)

srt_file = '/home/lyna/Escritorio/Applications I/Trail of the Screaming Forehead 2007 720p WEBRip x264 AAC [YTS.MX].srt'
yaml_file = 'dialogos.yaml'  
srt_to_yaml(srt_file, yaml_file)
