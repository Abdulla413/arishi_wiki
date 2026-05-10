import os
import re

def final_sync_split(input_txt, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_txt, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    # 1. مۇندەرىجىدىن ئىسىملارنى ئېلىش (پاكىزلاش)
    # مۇندەرىجە ئادەتتە بىرىنچى قۇردىن باشلاپ 'مۇندەرىجە' ياكى شۇنىڭغا ئوخشاش سۆز بىلەن باشلىنىدۇ
    # بىز 18-بەتكىچە بولغان تېكىستنى ئالىمىز
    toc_limit = 800 
    raw_toc = all_lines[:toc_limit]
    content_body = all_lines[toc_limit:]
    
    clean_names = []
    for line in raw_toc:
        t = line.strip()
        if not t: continue
        # رەقەم، چېكىت ۋە ئارتۇق بوشلۇقنى ئۆچۈرۈش
        name = re.sub(r'[\d\.]+', '', t).strip()
        if len(name) > 2:
            if name not in clean_names: # تەكرارلىقنى سۈزۈش
                clean_names.append(name)

    print(f"[*] مۇندەرىجىدىن {len(clean_names)} پاكىز ئىسىم ئېنىقلاندى.")

    # 2. مەزمۇننى پارچىلاش
    current_person = None
    current_content = []
    found_count = 0
    used_names = set()

    for line in content_body:
        text = line.strip()
        if not text: continue

        is_header = False
        matched_name = ""

        # مۇندەرىجىدىكى ھەر بىر ئىسىمنى مەزمۇن قۇرى بىلەن سېلىشتۇرۇش
        for target in clean_names:
            if target in used_names: continue
            
            # لوگىكا: ئەگەر مۇندەرىجىدىكى ئىسىم مەزمۇن قۇرىنىڭ ئىچىدە بولسا 
            # ۋە مەزمۇن قۇرى بەك ئۇزۇن بولمىسا (ئەڭ كۆپ بولغاندا ئىسىمدىن 10 ھەرپ ئارتۇق)
            if target in text and len(text) < len(target) + 15:
                is_header = True
                matched_name = target
                break

        if is_header:
            if current_person and current_content:
                save_file(current_person, current_content, output_dir)
                found_count += 1
            
            current_person = matched_name
            used_names.add(matched_name)
            current_content = [line.strip()]
        else:
            if current_person:
                current_content.append(line.strip())

    # ئاخىرقى شەخس
    if current_person:
        save_file(current_person, current_content, output_dir)
        found_count += 1

    print(f"[نەتىجە] جەمئىي {found_count} شەخس ئايرىلدى.")

def save_file(name, content, folder):
    safe_name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    with open(os.path.join(folder, f"{safe_name}.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(content))

if __name__ == "__main__":
    final_sync_split("/media/abdulla-arishi/Volume/arishi.wiki/data/tarihi_shehisler/mesh_hur_shehisler.txt", "final_processed")




