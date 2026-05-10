import os
from docx import Document

def split_by_names_list(docx_path, names_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. ئىسىملارنى ئوقۇش (ئايرىم txt ھۆججىتىدىن)
    # بۇ ھۆججەتتە بېت نومۇرى بولمىسا تېخىمۇ ياخشى
    with open(names_file, 'r', encoding='utf-8') as f:
        target_names = [line.strip() for line in f if line.strip()]
    
    print(f"[*] تىزىملىكتىن {len(target_names)} شەخس ئىسمى ئوقۇلدى.")

    doc = Document(docx_path)
    
    current_person = None
    current_content = []
    found_count = 0

    print("[*] بىر تەرەپ قىلىش باشلاندى...")

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # ئىسىملارنى تەكشۈرۈش
        # ئەگەر بۇ قۇر بىزنىڭ تىزىملىكىمىزدىكى بىرەر ئىسىم بىلەن باشلانسا
        is_name_row = False
        matched_name = ""
        
        for name in target_names:
            # ھەم تولۇق ماسلىشىشنى ھەم ئىسىم بىلەن باشلىنىشنى تەكشۈرىمىز
            # (ۋوردتا ئىسىمنىڭ ئارقىسىدا بوشلۇق ياكى بېت نومۇرى بولۇشى مۇمكىن)
            if text.startswith(name):
                is_name_row = True
                matched_name = name
                break

        if is_name_row:
            # بۇرۇنقى شەخسنى ساقلاش (ئەگەر مەزمۇنى بولسا)
            # بىز پەقەت مەزمۇنى بار (4 ئابزاستىن كۆپ) شەخسلەرنىلا ئالىمىز، 
            # بۇنداق بولغاندا باش تەرەپتىكى قىسقا مۇندەرىجىدىن ئۆتۈپ كېتىدۇ.
            if current_person and len(current_content) > 2:
                save_to_txt(current_person, current_content, output_dir)
                found_count += 1
            
            current_person = matched_name
            current_content = [text] # ئىسىمنىڭ ئۆزىنى بىرىنچى قۇر قىلىمىز
        else:
            if current_person:
                current_content.append(text)

    # ئەڭ ئاخىرقى شەخس
    if current_person and len(current_content) > 2:
        save_to_txt(current_person, current_content, output_dir)
        found_count += 1

    print(f"\n[OK] جەمئىي {found_count} شەخسنىڭ تەرجىمىھالى ئايرىلدى.")

def save_to_txt(name, content, output_dir):
    forbidden = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\t', '\n']
    safe_name = "".join([c for c in name if c not in forbidden]).strip()
    
    file_path = os.path.join(output_dir, f"{safe_name[:100]}.txt")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))

# يوللارنى جەزملەشتۈرۈڭ
docx_file = "/media/abdulla-arishi/Volume/arishi.wiki/data/tarihi_shehisler/mesh_hur_shehisler.docx"
names_txt = "/media/abdulla-arishi/Volume/arishi.wiki/data/tarihi_shehisler/munderije.txt" # ئىسىملار بار ھۆججەت
output_path = "/media/abdulla-arishi/Volume/arishi.wiki/data/processed_files/tarihi_shehisler"

if __name__ == "__main__":
    split_by_names_list(docx_file, names_txt, output_path)
