#!/bin/bash
# Combine all ClassChat demo reports into a single PDF

echo "╔════════════════════════════════════════════════════════╗"
echo "║    Creating Combined ClassChat Project Report PDF     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ Pandoc is not installed."
    echo ""
    echo "To install pandoc:"
    echo "  sudo apt-get install pandoc texlive-latex-base texlive-latex-extra"
    echo ""
    echo "Alternative: Using markdown to HTML, then print to PDF from browser"
    echo "Creating HTML version instead..."
    echo ""
    
    # Create combined markdown file
    OUTPUT_MD="screenshots/ClassChat_Complete_Report.md"
    OUTPUT_HTML="screenshots/ClassChat_Complete_Report.html"
    
    cat > "$OUTPUT_MD" << 'HEADER'
# ClassChat - Complete Project Report
**Student Name:** [Your Name]  
**Date:** November 9, 2025  
**Course:** Computer Networks  
**Project:** TCP/IP Chat System with Bonus Features

---

HEADER
    
    # Add all reports in order
    echo "Adding Task 1 Report..."
    echo -e "\n\n# Task 1: Client-Server Communication\n" >> "$OUTPUT_MD"
    cat screenshots/task1/TASK1_DEMO_REPORT.md >> "$OUTPUT_MD"
    
    echo "Adding Task 2 Report..."
    echo -e "\n\n---\n\n# Task 2: I/O Multiplexing\n" >> "$OUTPUT_MD"
    cat screenshots/task2/TASK2_DEMO_REPORT.md >> "$OUTPUT_MD"
    
    echo "Adding Task 3 Report..."
    echo -e "\n\n---\n\n# Task 3: Multi-Threaded Server\n" >> "$OUTPUT_MD"
    cat screenshots/task3/TASK3_DEMO_REPORT.md >> "$OUTPUT_MD"
    
    echo "Adding Task 4 Report..."
    echo -e "\n\n---\n\n# Task 4: Client-Client Communication\n" >> "$OUTPUT_MD"
    cat screenshots/task4/TASK4_DEMO_REPORT.md >> "$OUTPUT_MD"
    
    echo "Adding Bonus 5.1 Report..."
    echo -e "\n\n---\n\n# Bonus 5.1: Group Chatting\n" >> "$OUTPUT_MD"
    cat screenshots/bonus5.1/BONUS5.1_DEMO_REPORT.md >> "$OUTPUT_MD"
    
    echo "Adding Bonus 5.2 Report..."
    echo -e "\n\n---\n\n# Bonus 5.2: File Transfer\n" >> "$OUTPUT_MD"
    cat screenshots/bonus5.2/BONUS5.2_DEMO_REPORT.md >> "$OUTPUT_MD"
    
    echo "Adding Bonus 5.3 Report..."
    echo -e "\n\n---\n\n# Bonus 5.3: Offline Messages\n" >> "$OUTPUT_MD"
    cat screenshots/bonus5.3/BONUS5.3_DEMO_REPORT.md >> "$OUTPUT_MD"
    
    echo "Adding GUI Guide..."
    echo -e "\n\n---\n\n# GUI Client\n" >> "$OUTPUT_MD"
    cat screenshots/gui/GUI_DEMO_GUIDE.md >> "$OUTPUT_MD"
    
    # Create simple HTML with styling
    cat > "$OUTPUT_HTML" << 'HTML_START'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ClassChat - Complete Project Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .content {
            background: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        h3 { color: #7f8c8d; }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        pre code {
            background: none;
            color: #ecf0f1;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background: #f9f9f9;
        }
        .page-break {
            page-break-after: always;
        }
        @media print {
            body { background: white; }
            .content { box-shadow: none; }
        }
    </style>
</head>
<body>
<div class="content">
HTML_START
    
    # Convert markdown to HTML (simple conversion)
    python3 -c "
import markdown
with open('$OUTPUT_MD', 'r') as f:
    md_content = f.read()
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
print(html_content)
" >> "$OUTPUT_HTML" 2>/dev/null || {
        # Fallback if markdown module not available
        sed 's/^# /\n<h1>/g; s/^## /\n<h2>/g; s/^### /\n<h3>/g' "$OUTPUT_MD" | \
        sed 's/$/<\/h1>/g' >> "$OUTPUT_HTML"
    }
    
    echo '</div></body></html>' >> "$OUTPUT_HTML"
    
    echo ""
    echo "✅ Created files:"
    echo "   📄 $OUTPUT_MD"
    echo "   🌐 $OUTPUT_HTML"
    echo ""
    echo "To create PDF:"
    echo "  1. Open $OUTPUT_HTML in your browser"
    echo "  2. Press Ctrl+P (Print)"
    echo "  3. Select 'Save as PDF'"
    echo "  4. Save as 'ClassChat_Complete_Report.pdf'"
    echo ""
    
else
    # Pandoc is available - create PDF directly
    OUTPUT_PDF="screenshots/ClassChat_Complete_Report.pdf"
    TEMP_MD="screenshots/temp_combined.md"
    
    echo "Creating combined markdown..."
    
    cat > "$TEMP_MD" << 'HEADER'
---
title: "ClassChat - Complete Project Report"
author: "Your Name"
date: "November 9, 2025"
subject: "Computer Networks - TCP/IP Chat System"
keywords: [ClassChat, TCP/IP, Socket Programming, Python, Networking]
---

\newpage

HEADER
    
    echo "Adding Task 1..."
    echo -e "\n# Task 1: Client-Server Communication\n" >> "$TEMP_MD"
    cat screenshots/task1/TASK1_DEMO_REPORT.md >> "$TEMP_MD"
    echo -e "\n\n\\newpage\n" >> "$TEMP_MD"
    
    echo "Adding Task 2..."
    echo -e "\n# Task 2: I/O Multiplexing\n" >> "$TEMP_MD"
    cat screenshots/task2/TASK2_DEMO_REPORT.md >> "$TEMP_MD"
    echo -e "\n\n\\newpage\n" >> "$TEMP_MD"
    
    echo "Adding Task 3..."
    echo -e "\n# Task 3: Multi-Threaded Server\n" >> "$TEMP_MD"
    cat screenshots/task3/TASK3_DEMO_REPORT.md >> "$TEMP_MD"
    echo -e "\n\n\\newpage\n" >> "$TEMP_MD"
    
    echo "Adding Task 4..."
    echo -e "\n# Task 4: Client-Client Communication\n" >> "$TEMP_MD"
    cat screenshots/task4/TASK4_DEMO_REPORT.md >> "$TEMP_MD"
    echo -e "\n\n\\newpage\n" >> "$TEMP_MD"
    
    echo "Adding Bonus 5.1..."
    echo -e "\n# Bonus 5.1: Group Chatting\n" >> "$TEMP_MD"
    cat screenshots/bonus5.1/BONUS5.1_DEMO_REPORT.md >> "$TEMP_MD"
    echo -e "\n\n\\newpage\n" >> "$TEMP_MD"
    
    echo "Adding Bonus 5.2..."
    echo -e "\n# Bonus 5.2: File Transfer\n" >> "$TEMP_MD"
    cat screenshots/bonus5.2/BONUS5.2_DEMO_REPORT.md >> "$TEMP_MD"
    echo -e "\n\n\\newpage\n" >> "$TEMP_MD"
    
    echo "Adding Bonus 5.3..."
    echo -e "\n# Bonus 5.3: Offline Messages\n" >> "$TEMP_MD"
    cat screenshots/bonus5.3/BONUS5.3_DEMO_REPORT.md >> "$TEMP_MD"
    echo -e "\n\n\\newpage\n" >> "$TEMP_MD"
    
    echo "Adding GUI Guide..."
    echo -e "\n# GUI Client\n" >> "$TEMP_MD"
    cat screenshots/gui/GUI_DEMO_GUIDE.md >> "$TEMP_MD"
    
    echo ""
    echo "Converting to PDF..."
    pandoc "$TEMP_MD" -o "$OUTPUT_PDF" \
        --pdf-engine=pdflatex \
        --toc \
        --toc-depth=2 \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        -V documentclass=report
    
    rm "$TEMP_MD"
    
    echo ""
    echo "✅ PDF created successfully!"
    echo "   📄 $OUTPUT_PDF"
    echo ""
    echo "File size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo ""
fi

echo "═══════════════════════════════════════════════════════"
echo "         Report generation complete! ✅"
echo "═══════════════════════════════════════════════════════"
