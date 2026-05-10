import os
import re

# يوللارنى بەلگىلەش
source_file = '/media/abdulla-arishi/Volume/arishi.wiki/data/uyghur_tibabiti/miwe_koktatlar.txt'
target_dir = '/media/abdulla-arishi/Volume/arishi.wiki/data/processed_files/miwe_koktatlar'

# ئەگەر نىشان مۇندەرىجە بولمىسا قۇرۇش
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

def process_and_split():
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # سان بىلەن باشلانغان تېمىلارنى ئاساس قىلىپ پارچىلاش
    # ئەندىزە: قۇر بېشىدا سان + سىزىقچە + ئۇيغۇرچە تېكىست
    sections = re.split(r'\n(?=\d+-\s*)', content)

    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        # بىرىنچى قۇرنى تېما قىلىش
        title = lines[0].strip()
        # ھۆججەت نامىدىكى چەكلەنگەن بەلگىلەرنى بىر تەرەپ قىلىش
        file_name = re.sub(r'[\\/*?:"<>|]', '_', title) + '.txt'
        
        # مەزمۇننى بىر تەرەپ قىلىش:
        # تېمىدىن كېيىنكى بىر قۇرنى ساقلاپ، ئارىلىقتىكى بىكار قۇرلارنى سۈزۈۋېتىش
        processed_lines = [lines[0]] # تېمىنى قوشۇش
        for line in lines[1:]:
            clean_line = line.strip()
            if clean_line: # ئەگەر قۇرۇق بولمىسا قوشۇش
                processed_lines.append(clean_line)
        
        final_content = '\n'.join(processed_lines)
        
        # ساقلاش
        file_path = os.path.join(target_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as wf:
            wf.write(final_content)
        
    print(f"مۇۋەپپەقىيەتلىك تاماملىنىپ {len(sections)} دانە ھۆججەت قۇرۇلدى.")

if __name__ == "__main__":
    process_and_split()
