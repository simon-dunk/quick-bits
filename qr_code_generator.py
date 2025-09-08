import qrcode
from PIL import Image
import sys
import os

def generate_qr_code(url, filename=None, size=10, border=4):
    """
    Generate a QR code for a given URL
    
    Args:
        url (str): The URL to encode
        filename (str): Output filename (optional)
        size (int): Size of each box in pixels
        border (int): Border size in boxes
    """
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=size,  # Size of each box in pixels
        border=border,  # Border size in boxes
    )
    
    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Generate filename if not provided
    if filename is None:
        # Extract domain name for filename
        domain = url.replace("https://", "").replace("http://", "").replace("www.", "")
        domain = domain.split("/")[0].replace(".", "_")
        filename = f"qr_code_{domain}.png"
    
    # Ensure filename has .png extension
    if not filename.lower().endswith('.png'):
        filename += '.png'
    
    # Save the image
    qr_image.save(filename)
    print(f"QR code generated successfully: {filename}")
    
    return filename

def main():
    """Main function to handle command line usage"""
    
    if len(sys.argv) < 2:
        print("Usage: python qr_generator.py <URL> [filename]")
        print("Example: python qr_generator.py https://www.google.com")
        print("Example: python qr_generator.py https://www.google.com my_qr_code.png")
        return
    
    url = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Validate URL format (basic check)
    if not (url.startswith('http://') or url.startswith('https://')):
        print("Warning: URL should start with 'http://' or 'https://'")
        print("Adding 'https://' prefix...")
        url = 'https://' + url
    
    try:
        generate_qr_code(url, filename)
    except Exception as e:
        print(f"Error generating QR code: {e}")

def interactive_mode():
    """Interactive mode for generating QR codes"""
    
    print("=== QR Code Generator ===")
    print()
    
    while True:
        try:
            # Get URL from user
            url = input("Enter URL (or 'quit' to exit): ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not url:
                print("Please enter a valid URL.")
                continue
            
            # Add protocol if missing
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'https://' + url
            
            # Get optional filename
            filename = input("Enter filename (optional, press Enter to auto-generate): ").strip()
            filename = filename if filename else None
            
            # Get optional size
            size_input = input("Enter box size in pixels (default: 10): ").strip()
            try:
                size = int(size_input) if size_input else 10
            except ValueError:
                size = 10
                print("Invalid size, using default (10)")
            
            # Generate QR code
            output_file = generate_qr_code(url, filename, size)
            print(f"QR code saved as: {output_file}")
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()

if __name__ == "__main__":
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        main()
    else:
        # Run in interactive mode
        interactive_mode()
