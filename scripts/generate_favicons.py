#!/usr/bin/env python3
"""
Favicon Generator for DramaBench
Converts SVG to multiple PNG sizes for favicon usage
"""

try:
    from cairosvg import svg2png
    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False
    print("⚠️  cairosvg not available. Install with: pip install cairosvg")

from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent.parent
ASSETS_DIR = SCRIPT_DIR / "assets"
SVG_FILE = ASSETS_DIR / "favicon.svg"

# Favicon sizes
SIZES = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "favicon-96x96.png": 96,
    "apple-touch-icon.png": 180,
    "favicon-512x512.png": 512,
}

def generate_favicons():
    """Generate PNG favicons from SVG source"""

    if not CAIROSVG_AVAILABLE:
        print("❌ Cannot generate PNG files without cairosvg")
        print("📝 Install: pip install cairosvg")
        print("📝 Or use online converter: https://convertio.co/svg-png/")
        return False

    if not SVG_FILE.exists():
        print(f"❌ SVG file not found: {SVG_FILE}")
        return False

    print(f"🎨 Generating favicons from {SVG_FILE.name}...")
    print("=" * 60)

    # Read SVG content
    with open(SVG_FILE, 'r') as f:
        svg_content = f.read()

    # Generate each size
    success_count = 0
    for filename, size in SIZES.items():
        output_path = ASSETS_DIR / filename
        try:
            svg2png(
                bytestring=svg_content.encode('utf-8'),
                write_to=str(output_path),
                output_width=size,
                output_height=size
            )
            print(f"✅ Generated: {filename} ({size}x{size})")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to generate {filename}: {e}")

    print("=" * 60)
    print(f"✨ Successfully generated {success_count}/{len(SIZES)} favicon files")

    # Generate favicon.ico (multi-size icon)
    try:
        from PIL import Image

        # Load PNG images
        images = []
        for filename in ["favicon-16x16.png", "favicon-32x32.png", "favicon-96x96.png"]:
            img_path = ASSETS_DIR / filename
            if img_path.exists():
                images.append(Image.open(img_path))

        if images:
            ico_path = ASSETS_DIR / "favicon.ico"
            images[0].save(
                ico_path,
                format='ICO',
                sizes=[(16, 16), (32, 32), (96, 96)]
            )
            print(f"✅ Generated: favicon.ico (multi-size)")
    except ImportError:
        print("⚠️  Pillow not available for ICO generation")
        print("📝 Install: pip install Pillow")
    except Exception as e:
        print(f"⚠️  ICO generation failed: {e}")

    return True

def print_html_usage():
    """Print HTML usage instructions"""
    print("\n" + "=" * 60)
    print("📝 Add these lines to your HTML <head> section:")
    print("=" * 60)
    print("""
<!-- Favicons -->
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="96x96" href="assets/favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
<link rel="shortcut icon" href="assets/favicon.ico">
""")

if __name__ == "__main__":
    print("🚀 DramaBench Favicon Generator")
    print("=" * 60)

    if generate_favicons():
        print_html_usage()
        print("\n✅ Favicon generation complete!")
    else:
        print("\n❌ Favicon generation failed")
        print("\n💡 Alternative: Use online SVG to PNG converter")
        print("   - https://convertio.co/svg-png/")
        print("   - Upload favicon.svg")
        print("   - Download as PNG at sizes: 16x16, 32x32, 96x96, 180x180, 512x512")
