import re
import fitz  # PyMuPDF
print(fitz.__doc__)
print(fitz.__version__)

def split_by_chapters(pdf_path, skip_first=0, verbose=True):
    """
    Splits a PDF into separate files for each chapter using a specific regex
    that looks for chapter titles at the end of a line.
    """
    # This new pattern is the key to the fix.
    # It only matches lines that end after the chapter number.
    chapter_pattern = r"^\s*CHAPTER\s+(\d+|[IVXLCDM]+)\s*$"

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return
        
    total_pages = doc.page_count
    chapter_indices = []

    for i in range(total_pages):
        page = doc.load_page(i)
        # Using get_text("text") is correct. No change needed here.
        text = page.get_text("text").replace("\xa0", " ")

        # This search will now only succeed on the main chapter title pages
        if re.search(chapter_pattern, text, re.IGNORECASE | re.MULTILINE):
            chapter_indices.append(i)
            if verbose:
                print(f"Found chapter start on page {i+1}")

    if not chapter_indices:
        print("No chapters detected. The regex pattern might need adjustment for this PDF's format.")
        doc.close()
        return

    chapter_indices.append(total_pages)
    
    if skip_first > 0:
        chapter_indices = chapter_indices[skip_first:]

    # This loop correctly saves one file per chapter
    for i in range(len(chapter_indices) - 1):
        start_page = chapter_indices[i]
        end_page = chapter_indices[i+1]
        
        writer = fitz.open()
        
        # Insert the entire page range for the chapter at once
        writer.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)
        
        # Chapter numbers are now correctly identified based on the index
        filename = f"chapter_{i+1}.pdf"
        writer.save(filename)
        writer.close()
        
        if verbose:
            print(f"✅ Saved {filename} (pages {start_page + 1} to {end_page})")
            
    doc.close()

def merge_chapter_pairs(chapter_tuples, prefix="chapter", output_prefix="merged", verbose=True):
    """
    Merge PDFs based on tuples of chapter numbers.
    """
    for t in chapter_tuples:
        ch1, ch2 = t
        file1 = f"{prefix}_{ch1}.pdf"
        file2 = f"{prefix}_{ch2}.pdf"

        merged_pdf = fitz.open()
        for fname in [file1, file2]:
            try:
                pdf = fitz.open(fname)
                merged_pdf.insert_pdf(pdf)
                pdf.close()
            except Exception as e:
                print(f"Error processing {fname}: {e}")
                continue

        out_filename = f"{output_prefix}_{ch1}_{ch2}.pdf"
        merged_pdf.save(out_filename)
        merged_pdf.close()

        if verbose:
            print(f"Merged {file1} + {file2} -> {out_filename}")

split_by_chapters('/Users/simondunk/Downloads/Guide_To_Networking_Essentials.pdf', skip_first=12)
