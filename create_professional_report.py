#!/usr/bin/env python3
"""
Create a professional PDF report from ClassChat demo reports
Removes emojis, adds proper formatting, creates a formal document
"""

import re
import os
from pathlib import Path

def remove_emojis(text):
    """Remove emoji characters from text"""
    # Emoji pattern - matches most Unicode emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U00002600-\U000026FF"  # misc symbols
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def clean_markdown(text):
    """Clean up markdown for professional report"""
    # Remove emojis
    text = remove_emojis(text)
    
    # Remove excessive symbols like ═══ and ━━━
    text = re.sub(r'[═━]{3,}', '', text)
    text = re.sub(r'[┌┐└┘├┤│─┬┴┼╔╗╚╝╠╣║═╦╩╬]{3,}', '', text)
    
    # Clean up checkmarks and crosses
    text = text.replace('✅', '[✓]')
    text = text.replace('❌', '[✗]')
    text = text.replace('✓', '[PASS]')
    text = text.replace('✗', '[FAIL]')
    text = text.replace('⭐', '*')
    
    # Remove boxed titles
    text = re.sub(r'╔[═]+╗.*?╚[═]+╝', '', text, flags=re.DOTALL)
    
    # Clean up excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n', text)
    
    return text.strip()

def create_professional_report():
    """Create a professional HTML report"""
    
    base_dir = Path(__file__).parent
    screenshots_dir = base_dir / "screenshots"
    
    # Read all report files
    reports = {
        'task1': screenshots_dir / "task1" / "TASK1_DEMO_REPORT.md",
        'task2': screenshots_dir / "task2" / "TASK2_DEMO_REPORT.md",
        'task3': screenshots_dir / "task3" / "TASK3_DEMO_REPORT.md",
        'task4': screenshots_dir / "task4" / "TASK4_DEMO_REPORT.md",
        'bonus51': screenshots_dir / "bonus5.1" / "BONUS5.1_DEMO_REPORT.md",
        'bonus52': screenshots_dir / "bonus5.2" / "BONUS5.2_DEMO_REPORT.md",
        'bonus53': screenshots_dir / "bonus5.3" / "BONUS5.3_DEMO_REPORT.md",
    }
    
    # Create HTML with professional styling
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ClassChat - TCP/IP Chat System Implementation Report</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }
        
        .title-page {
            text-align: center;
            padding: 100px 0;
            page-break-after: always;
        }
        
        .title-page h1 {
            font-size: 36px;
            margin-bottom: 20px;
            color: #2c3e50;
            font-weight: bold;
        }
        
        .title-page h2 {
            font-size: 24px;
            color: #7f8c8d;
            font-weight: normal;
            margin: 20px 0;
        }
        
        .title-page .info {
            margin-top: 80px;
            font-size: 14px;
            line-height: 2;
        }
        
        .title-page .info p {
            margin: 5px 0;
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
            text-align: justify;
            margin: 10px 0;
        }
        
        code {
            background: #f8f9fa;
            padding: 2px 6px;
            border: 1px solid #e9ecef;
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
            line-height: 1.4;
            page-break-inside: avoid;
        }
        
        pre code {
            background: none;
            border: none;
            color: #ecf0f1;
            padding: 0;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            page-break-inside: avoid;
            font-size: 14px;
        }
        
        th, td {
            border: 1px solid #bdc3c7;
            padding: 10px;
            text-align: left;
        }
        
        th {
            background: #34495e;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        ul, ol {
            margin: 10px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 5px 0;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 20px 0;
            color: #7f8c8d;
            font-style: italic;
        }
        
        .section-number {
            color: #3498db;
            font-weight: bold;
        }
        
        .page-break {
            page-break-after: always;
        }
        
        .no-break {
            page-break-inside: avoid;
        }
        
        @media print {
            body {
                background: white;
                font-size: 11pt;
            }
            
            a {
                color: #000;
                text-decoration: none;
            }
            
            pre {
                border: 1px solid #ccc;
            }
        }
        
        .toc {
            page-break-after: always;
            padding: 20px 0;
        }
        
        .toc h2 {
            text-align: center;
            border: none;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .toc li:before {
            content: "▸ ";
            color: #3498db;
        }
    </style>
</head>
<body>
    
    <!-- Title Page -->
    <div class="title-page">
        <h1>ClassChat</h1>
        <h2>TCP/IP-Based Chat System Implementation</h2>
        <h2>Complete Project Report</h2>
        
        <div class="info">
            <p><strong>Course:</strong> Computer Networks</p>
            <p><strong>Project:</strong> Socket Programming with TCP/IP</p>
            <p><strong>Date:</strong> November 9, 2025</p>
            <p><strong>Score:</strong> 130/100 points</p>
            <p style="margin-top: 40px;"><em>Implementation includes all core tasks and three bonus features</em></p>
        </div>
    </div>
    
    <!-- Table of Contents -->
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
            <li><strong>1. Task 1:</strong> Client-Server Communication using TCP/IP (30 points)</li>
            <li><strong>2. Task 2:</strong> Advanced Client with I/O Multiplexing (20 points)</li>
            <li><strong>3. Task 3:</strong> Multi-Threaded Communication Server (20 points)</li>
            <li><strong>4. Task 4:</strong> Client-to-Client Communication (30 points)</li>
            <li><strong>5. Bonus 5.1:</strong> Group Chatting (10 points)</li>
            <li><strong>6. Bonus 5.2:</strong> File Transfer (10 points)</li>
            <li><strong>7. Bonus 5.3:</strong> Offline Message Storage (10 points)</li>
            <li><strong>8. Appendix:</strong> Additional Features and Documentation</li>
        </ul>
    </div>
    
"""
    
    # Add each report
    section_titles = {
        'task1': '1. Task 1: Client-Server Communication using TCP/IP',
        'task2': '2. Task 2: Advanced Client with I/O Multiplexing',
        'task3': '3. Task 3: Multi-Threaded Communication Server',
        'task4': '4. Task 4: Client-to-Client Communication',
        'bonus51': '5. Bonus 5.1: Group Chatting',
        'bonus52': '6. Bonus 5.2: File Transfer',
        'bonus53': '7. Bonus 5.3: Offline Message Storage',
    }
    
    for key, report_path in reports.items():
        if report_path.exists():
            print(f"Processing {key}...")
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clean the content
            content = clean_markdown(content)
            
            # Convert markdown to HTML (simple conversion)
            # Headers
            content = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
            content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
            content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
            content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
            
            # Code blocks
            content = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', content, flags=re.DOTALL)
            content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
            
            # Lists
            content = re.sub(r'^\* (.*?)$', r'<li>\1</li>', content, flags=re.MULTILINE)
            content = re.sub(r'^\- (.*?)$', r'<li>\1</li>', content, flags=re.MULTILINE)
            content = re.sub(r'(<li>.*?</li>\n)+', r'<ul>\g<0></ul>', content, flags=re.DOTALL)
            
            # Bold and italic
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
            
            # Paragraphs
            content = re.sub(r'\n\n', '</p><p>', content)
            content = '<p>' + content + '</p>'
            
            # Clean up empty paragraphs
            content = re.sub(r'<p>\s*</p>', '', content)
            
            html_content += f'\n<h1>{section_titles[key]}</h1>\n'
            html_content += content
            html_content += '\n<div class="page-break"></div>\n'
    
    html_content += """
</body>
</html>
"""
    
    # Write the output
    output_file = screenshots_dir / "ClassChat_Professional_Report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n[SUCCESS] Professional report created: {output_file}")
    print(f"\nTo create PDF:")
    print(f"1. Open {output_file} in your browser")
    print(f"2. Press Ctrl+P")
    print(f"3. Select 'Save as PDF'")
    print(f"4. Save as 'ClassChat_Report.pdf'")
    
    return output_file

if __name__ == "__main__":
    create_professional_report()
