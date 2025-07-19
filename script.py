
import os
import re
import shutil
from datetime import datetime, timedelta
from urllib.parse import unquote

ORIGIN_DIR = "origin"
POST_DIR = "_posts"
ARCHIVE_DIR = "archive"

def parse_korean_date(date_str):
    """'YYYY년 MM월 DD일 오전/오후 HH:MM' 형식의 한글 날짜 문자열을 파싱합니다."""
    try:
        # '오후' 또는 '오전' 처리
        is_pm = '오후' in date_str
        date_str = date_str.replace('오전', '').replace('오후', '').strip()
        
        # '년, 월, 일'을 하이픈으로 변경
        date_str = date_str.replace('년', '-').replace('월', '-').replace('일', '')
        
        # 날짜와 시간 분리
        date_part, time_part = date_str.split(' ')
        date_part = '-'.join([p.strip() for p in date_part.split('-') if p.strip()])
        
        dt = datetime.strptime(f"{date_part} {time_part}", '%Y-%m-%d %H:%M')

        if is_pm and dt.hour < 12:
            dt += timedelta(hours=12)
        return dt
    except Exception as e:
        print(f"날짜 파싱 오류: {date_str}, 오류: {e}")
        return datetime.now() # 파싱 실패 시 현재 시간으로 대체

def process_post(post_path):
    """단일 포스트 폴더를 처리합니다."""
    md_file = None
    for f in os.listdir(post_path):
        if f.endswith('.md'):
            md_file = f
            break
    
    if not md_file:
        print(f"{post_path}에서 마크다운 파일을 찾을 수 없습니다.")
        return

    # --- 마크다운 파일 읽고 정보 추출 ---
    with open(os.path.join(post_path, md_file), 'r', encoding='utf-8') as f:
        lines = f.readlines()

    title = ""
    created_date_str = ""
    tags = []
    content_lines = []
    content_started = False

    for i, line in enumerate(lines):
        if line.strip().startswith('# '):
            title = line.strip('# ').strip()
            content_started = True
            content_lines.append(line)
            continue
        if line.strip().startswith('Created:'):
            created_date_str = line.strip('Created:').strip()
            continue
        if line.strip().startswith('Tags:'):
            tags = [tag.strip() for tag in line.strip('Tags:').split(',')]
            continue
        
        if content_started:
            content_lines.append(line)

    if not title:
        print(f"{md_file}에서 제목을 찾을 수 없습니다. 건너뜁니다.")
        return

    content = "".join(content_lines)
    created_date = parse_korean_date(created_date_str) if created_date_str else datetime.now()
    if not tags:
        tags = ['uncategorized']

    # --- 파일명 및 경로 생성 ---
    post_date_str = created_date.strftime("%Y-%m-%d")
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')
    new_post_filename = f"{post_date_str}-{safe_title}.md"
    new_post_filepath = os.path.join(POST_DIR, new_post_filename)

    # --- 이미지 경로 설정 ---
    major_category = safe_title.split('-')[0].lower()
    chapter_match = re.search(r'(\d+)장', title)
    chapter_dir = chapter_match.group(1) if chapter_match else "misc"
    image_base_path = f"assets/images/{tags[0]}/{major_category}/{chapter_dir}"
    os.makedirs(image_base_path, exist_ok=True)

    # --- 이미지 경로 수정 및 파일 이동 함수 ---
    def replace_image_path(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        if image_path.startswith("http"):
            return f"![{alt_text}]({image_path})"
        
        original_image_fs_path = os.path.join(post_path, unquote(image_path))
        image_name = os.path.basename(unquote(image_path))
        new_image_web_path = f"/{image_base_path}/{image_name}"
        new_image_fs_path = os.path.join(image_base_path, image_name)

        if os.path.exists(original_image_fs_path):
            shutil.copy(original_image_fs_path, new_image_fs_path)
        else:
            print(f"이미지 파일을 찾을 수 없습니다: {original_image_fs_path}")
        
        return f"![{alt_text}]({new_image_web_path})"

    content = re.sub(r"!\[(.*?)\]\((.*?)\)", replace_image_path, content)

    # --- 헤더 생성 및 파일 작성 ---
    header = f"""---
layout: post
current: post
navigation: True
title: "{title}"
date: {created_date.strftime("%Y-%m-%d %H:%M:%S")}
tags: {tags}
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
"""
    with open(new_post_filepath, 'w', encoding='utf-8') as f:
        f.write(header + content)
    print(f"성공적으로 처리되었습니다: {new_post_filename}")


def main():
    if not os.path.exists(ORIGIN_DIR):
        print(f"'{ORIGIN_DIR}' 폴더를 찾을 수 없습니다.")
        return

    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    for folder_name in os.listdir(ORIGIN_DIR):
        folder_path = os.path.join(ORIGIN_DIR, folder_name)
        if os.path.isdir(folder_path):
            print(f"'{folder_name}' 폴더 처리를 시작합니다...")
            try:
                process_post(folder_path)
                # 처리 완료 후 아카이브 폴더로 이동
                shutil.move(folder_path, os.path.join(ARCHIVE_DIR, folder_name))
                print(f"'{folder_name}' 폴더를 '{ARCHIVE_DIR}'로 이동했습니다.")
            except Exception as e:
                print(f"'{folder_name}' 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
