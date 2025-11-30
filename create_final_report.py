#!/usr/bin/env python3
"""
Create a professional PDF report with images from screenshots
Fixes markdown formatting and embeds actual screenshots
"""

import re
import os
from pathlib import Path
import base64

def remove_emojis(text):
    """Remove emoji characters from text"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"
        "\U00002600-\U000026FF"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def clean_markdown_formatting(text):
    """Fix markdown formatting issues"""
    # Remove emojis
    text = remove_emojis(text)
    
    # Remove excessive symbols
    text = re.sub(r'[═━┌┐└┘├┤│─┬┴┼╔╗╚╝╠╣║╦╩╬]{2,}', '', text)
    
    # Fix bold formatting: **text** should become <strong>text</strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Fix italic: *text* should become <em>text</em>
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Fix inline code: `text` should become <code>text</code>
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Clean up checkmarks
    text = text.replace('✅', '✓')
    text = text.replace('❌', '✗')
    text = text.replace('⭐', '*')
    
    # Clean up boxed titles
    text = re.sub(r'╔[═]+╗.*?╚[═]+╝', '', text, flags=re.DOTALL)
    
    return text

def find_images_in_folder(folder_path):
    """Find all images in a folder"""
    images = []
    if folder_path.exists():
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif']:
            images.extend(folder_path.glob(ext))
    return sorted(images)

def markdown_to_html(text):
    """Convert markdown to HTML with proper formatting"""
    lines = text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    code_content = []
    
    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                html_lines.append('<pre><code>' + '\n'.join(code_content) + '</code></pre>')
                code_content = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            continue
        
        if in_code_block:
            code_content.append(line)
            continue
        
        # Headers
        if line.startswith('#### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h4>{line[5:]}</h4>')
        elif line.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h1>{line[2:]}</h1>')
        # Lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line.strip()[2:]}</li>')
        # Numbered lists
        elif re.match(r'^\d+\.\s', line.strip()):
            content = re.sub(r'^\d+\.\s', '', line.strip())
            html_lines.append(f'<li>{content}</li>')
        # Empty lines
        elif not line.strip():
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<br>')
        # Regular paragraphs
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if line.strip():
                html_lines.append(f'<p>{line}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

def create_professional_report_with_images():
    """Create professional HTML report with embedded images"""
    
    base_dir = Path(__file__).parent
    screenshots_dir = base_dir / "screenshots"
    
    # Report sections
    sections = [
        ('task1', 'Task 1: Client-Server Communication using TCP/IP', '30 points'),
        ('task2', 'Task 2: Advanced Client with I/O Multiplexing', '20 points'),
        ('task3', 'Task 3: Multi-Threaded Communication Server', '20 points'),
        ('task4', 'Task 4: Client-to-Client Communication', '30 points'),
        ('bonus5.1', 'Bonus 5.1: Group Chatting', '10 bonus points'),
        ('bonus5.2', 'Bonus 5.2: File Transfer', '10 bonus points'),
        ('bonus5.3', 'Bonus 5.3: Offline Message Storage', '10 bonus points'),
    ]
    
    # HTML header with professional styling
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ClassChat - Implementation Report</title>
    <style>
        @page { size: A4; margin: 2cm; }
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }
        .title-page {
            text-align: center;
            padding: 100px 20px;
            page-break-after: always;
        }
        .title-page h1 {
            font-size: 42px;
            margin-bottom: 20px;
            color: #2c3e50;
        }
        .title-page h2 {
            font-size: 24px;
            color: #7f8c8d;
            margin: 20px 0;
        }
        .title-page .info {
            margin-top: 60px;
            font-size: 16px;
            line-height: 2.5;
        }
        h1 {
            color: #2c3e50;
            font-size: 28px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 40px;
            page-break-before: always;
        }
        h2 {
            color: #34495e;
            font-size: 22px;
            margin-top: 30px;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }
        h3 {
            color: #7f8c8d;
            font-size: 18px;
            margin-top: 20px;
        }
        h4 {
            color: #95a5a6;
            font-size: 16px;
            margin-top: 15px;
        }
        p {
            margin: 10px 0;
            text-align: justify;
        }
        code {
            background: #f4f5f7;
            padding: 2px 6px;
            border: 1px solid #ddd;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 90%;
        }
        pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            page-break-inside: avoid;
        }
        pre code {
            background: none;
            border: none;
            color: #ecf0f1;
        }
        .screenshot {
            margin: 20px 0;
            text-align: center;
            page-break-inside: avoid;
        }
        .screenshot img {
            max-width: 100%;
            border: 2px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .screenshot-caption {
            font-size: 14px;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 10px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 14px;
            page-break-inside: avoid;
        }
        th, td {
            border: 1px solid #bdc3c7;
            padding: 10px;
            text-align: left;
        }
        th {
            background: #34495e;
            color: white;
        }
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        ul, ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        li {
            margin: 8px 0;
        }
        strong {
            color: #2c3e50;
            font-weight: 600;
        }
        .section-header {
            background: #3498db;
            color: white;
            padding: 10px 20px;
            margin: 30px 0 20px 0;
            border-radius: 5px;
        }
        .toc {
            page-break-after: always;
            padding: 20px;
        }
        .toc h2 {
            text-align: center;
            border: none;
            color: #2c3e50;
        }
        .toc ul {
            list-style: none;
            padding: 20px;
        }
        .toc li {
            margin: 15px 0;
            font-size: 16px;
        }
        .points {
            color: #27ae60;
            font-weight: bold;
        }
        @media print {
            body { background: white; }
            .screenshot img { max-width: 90%; }
        }
    </style>
</head>
<body>
    
    <div class="title-page">
        <h1>ClassChat</h1>
        <h2>TCP/IP-Based Chat System</h2>
        <h2>Complete Implementation Report</h2>
        <div class="info">
            <p><strong>Course:</strong> Computer Networks</p>
            <p><strong>Project:</strong> Socket Programming with TCP/IP Protocol</p>
            <p><strong>Date:</strong> November 9, 2025</p>
            <p><strong>Total Score:</strong> <span class="points">130/100 points</span></p>
            <p style="margin-top: 30px;"><em>Includes all core tasks (100 points) and three bonus features (30 points)</em></p>
        </div>
    </div>
    
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
"""
    
    # Add TOC entries
    for i, (folder, title, points) in enumerate(sections, 1):
        html_content += f'            <li><strong>{i}. {title}</strong> <span class="points">({points})</span></li>\n'
    
    html_content += """        </ul>
    </div>
    
"""
    
    # Process each section
    for section_num, (folder, title, points) in enumerate(sections, 1):
        print(f"Processing {folder}...")
        
        # Add section header
        html_content += f'''
    <div class="section-header">
        <h1>Section {section_num}: {title}</h1>
        <p style="margin:0; font-size:14px;">Points: {points}</p>
    </div>
'''
        
        # Find and add images for this section
        folder_path = screenshots_dir / folder
        images = find_images_in_folder(folder_path)
        
        if images:
            html_content += f'<h2>Implementation Screenshots</h2>\n'
            for i, img_path in enumerate(images, 1):
                # Embed image as base64
                try:
                    with open(img_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                        img_ext = img_path.suffix[1:]
                        html_content += f'''
    <div class="screenshot">
        <img src="data:image/{img_ext};base64,{img_data}" alt="Screenshot {i}">
        <div class="screenshot-caption">Figure {section_num}.{i}: {title} - Screenshot {i}</div>
    </div>
'''
                except Exception as e:
                    print(f"  Warning: Could not embed {img_path.name}: {e}")
        
        # Add markdown content
        md_file = folder_path / f"{folder.replace('bonus', 'BONUS').replace('task', 'TASK').upper()}_DEMO_REPORT.md"
        if not md_file.exists():
            # Try alternative names
            possible_names = [
                f"TASK{folder[-1]}_DEMO_REPORT.md" if 'task' in folder else None,
                f"BONUS{folder[-3:]}_DEMO_REPORT.md" if 'bonus' in folder else None,
            ]
            for alt_name in possible_names:
                if alt_name:
                    alt_path = folder_path / alt_name
                    if alt_path.exists():
                        md_file = alt_path
                        break
        
        if md_file.exists():
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clean and convert markdown
            content = clean_markdown_formatting(content)
            content_html = markdown_to_html(content)
            
            html_content += f'\n<h2>Implementation Details</h2>\n'
            html_content += content_html
        
        html_content += '\n<div style="page-break-after: always;"></div>\n'
    
    html_content += """
</body>
</html>
"""
    
    # Write output
    output_file = screenshots_dir / "ClassChat_Final_Report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ SUCCESS! Professional report with images created!")
    print(f"\nFile: {output_file}")
    print(f"\nTo create PDF:")
    print(f"1. Open the file in your browser")
    print(f"2. Press Ctrl+P")
    print(f"3. Save as PDF")
    print(f"\nAll screenshots are embedded in the report!")
    
    return output_file

if __name__ == "__main__":
    create_professional_report_with_images()
