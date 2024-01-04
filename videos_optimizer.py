"""
- Author: Rios Rugel Renzo
- Last modified: 2023-12-06
"""

from moviepy.editor import VideoFileClip
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Function to obtain input, output, and PDF report paths
def get_paths(base_folder):
    input_folder = base_folder
    output_folder = os.path.join(base_folder, 'optimized_videos')
    pdf_report = os.path.join(base_folder, 'optimized_videos_report.pdf')

    # Ensure the output folder exists; if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    return input_folder, output_folder, pdf_report

# Function to obtain a list of video files in the input folder
def get_files(input_folder, extensions=('mp4', 'avi', 'mkv')):
    input_files = [file for file in os.listdir(input_folder) if file.lower().endswith(extensions)]
    return input_files

# Function to optimize a video file and return original and optimized sizes
def optimize_video(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    original_size = os.path.getsize(input_path)
    optimized_size = os.path.getsize(output_path)
    clip.close()
    return original_size, optimized_size

# Function to generate a PDF report with video optimization information
def generate_pdf_report(pdf_report, video_info, input_folder):
    doc = SimpleDocTemplate(pdf_report, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    table_style = styles['Normal']

    # Title spacing adjustments
    title_style.spaceAfter = 36

    content = []

    # Report title
    content.append(Paragraph("Video Optimization Report", title_style))

    # Data table
    data_table = Table([['Video Name', 'Original Size', 'Optimized Size', 'Optimization Percentage']] + video_info)

    # Table style
    table_style_definition = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]

    data_table.setStyle(TableStyle(table_style_definition))
    content.append(data_table)

    # Folder path
    content.append(Paragraph(f'Folder Path: {input_folder}', table_style))

    # Add content to the PDF report
    doc.build(content)

# Function to process each video in the input folder and collect optimization information
def process_videos(input_folder, output_folder):
    video_info = []

    input_files = get_files(input_folder)

    for file in input_files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f'optimized_{file}')

        original_size, optimized_size = optimize_video(input_path, output_path)

        optimization_percentage = f'{((original_size - optimized_size) / original_size) * 100:.2f}%'

        video_info.append([file, original_size, optimized_size, optimization_percentage])

    return video_info

def main():
    base_folder = r'C:\Users\user\Desktop\final project'
    input_folder, output_folder, pdf_report = get_paths(base_folder)

    video_info = process_videos(input_folder, output_folder)

    generate_pdf_report(pdf_report, video_info, input_folder)

    print("Process completed. Report generated at:", pdf_report)

if __name__ == "__main__":
    main()
