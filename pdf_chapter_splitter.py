
import re
import fitz
print(fitz.__doc__)  # should show something about PyMuPDF
print(fitz.__version__)



def split_by_chapters(pdf_path, chapter_pattern=r"^\s*CHAPTER\s+(\d+|[IVXLCDM]+)\b.*", skip_first=0, verbose=True):
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count

    chapter_indices = []

    for i in range(total_pages):
        page = doc.load_page(i)
        text = page.get_text("text")
        text = text.replace("\xa0", " ")  # normalize spaces

        if re.search(chapter_pattern, text, re.IGNORECASE | re.MULTILINE):
            chapter_indices.append(i)
            if verbose:
                print(f"Detected chapter on page {i+1}")

    if not chapter_indices:
        print("No chapters detected. Check your pattern!")
        return

    chapter_indices.append(total_pages)  # sentinel
    chapter_indices = chapter_indices[skip_first:]

    for idx in range(len(chapter_indices) - 1):
        writer = fitz.open()
        for j in range(chapter_indices[idx], chapter_indices[idx+1]):
            writer.insert_pdf(doc, from_page=j, to_page=j)
        filename = f"chapter_{idx+1}.pdf"
        writer.save(filename)
        writer.close()
        if verbose:
            print(f"Saved {filename} (pages {chapter_indices[idx]+1}-{chapter_indices[idx+1]})")

import fitz  # PyMuPDF

def merge_chapter_pairs(chapter_tuples, prefix="chapter", output_prefix="merged", verbose=True):
    """
    Merge PDFs based on tuples of chapter numbers.
    
    Parameters:
    - chapter_tuples: list of tuples, e.g. [(1,2), (4,5)]
    - prefix: the prefix of chapter files, e.g. 'chapter' for 'chapter_1.pdf'
    - output_prefix: prefix for merged files
    - verbose: print progress
    """
    for t in chapter_tuples:
        ch1, ch2 = t
        file1 = f"{prefix}_{ch1}.pdf"
        file2 = f"{prefix}_{ch2}.pdf"

        # Open the PDFs
        merged_pdf = fitz.open()
        for fname in [file1, file2]:
            try:
                pdf = fitz.open(fname)
                merged_pdf.insert_pdf(pdf)
                pdf.close()
            except Exception as e:
                print(f"Error opening {fname}: {e}")
                continue

        # Save the merged PDF
        out_filename = f"{output_prefix}_{ch1}_{ch2}.pdf"
        merged_pdf.save(out_filename)
        merged_pdf.close()

        if verbose:
            print(f"Merged {file1} + {file2} -> {out_filename}")

# split_by_chapters('/Users/simondunk/Downloads/Management_ Leading & Collaborating in the Competitive World 15th Edition – PDF ebook.pdf', skip_first=12)
merge_chapter_pairs([(2, 3)])