#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Barcode Label Generator - Generate and print barcode labels for Inventarium.

This module generates barcode labels with product information using PIL/Pillow
and Code128 barcodes. Labels can be printed or saved as PNG files.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import sys
import subprocess
from datetime import date

from PIL import Image, ImageDraw, ImageFont

# Try to import barcode libraries (code128 or python-barcode)
code128 = None
python_barcode = None

try:
    import code128
except ImportError:
    pass

if not code128:
    try:
        import barcode
        from barcode.writer import ImageWriter
        python_barcode = barcode
    except ImportError:
        pass


class BarcodeLabel:
    """Generate and print barcode labels."""

    # Label dimensions (pixels)
    LABEL_WIDTH = 440
    LABEL_HEIGHT = 260

    # Barcode settings
    BARCODE_HEIGHT = 80
    BARCODE_X = 10
    BARCODE_Y = 80

    def __init__(self, engine):
        """
        Initialize barcode label generator.

        Args:
            engine: Application engine for database access and settings
        """
        self.engine = engine
        self.font_path = self._get_font_path()
        self.barcodes_dir = self._ensure_barcodes_dir()

    def _get_font_path(self):
        """Get font path for label text."""
        # Try to get font from engine settings
        if hasattr(self.engine, 'get_font'):
            font = self.engine.get_font()
            if font and os.path.exists(font):
                return font

        # Try local fonts directory first, then system fonts
        font_paths = [
            os.path.join(os.path.dirname(__file__), "fonts", "arial.ttf"),
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path

        return None  # Will use default font

    def _ensure_barcodes_dir(self):
        """Ensure barcodes directory exists."""
        barcodes_dir = self.engine.get_file("barcodes")
        if not os.path.exists(barcodes_dir):
            os.makedirs(barcodes_dir)
        return barcodes_dir

    def _get_font(self, size):
        """Get font with specified size."""
        try:
            if self.font_path:
                return ImageFont.truetype(self.font_path, size)
        except Exception:
            pass
        return ImageFont.load_default()

    def get_label_data(self, label_id):
        """
        Get label data from database.

        Args:
            label_id: Label ID to get data for

        Returns:
            Dict with label data or None if not found
        """
        sql = """
            SELECT
                lb.label_id,
                lb.tick,
                p.description AS product_name,
                b.description AS lot,
                b.expiration,
                c.description AS conservation,
                pk.in_the_dark
            FROM labels lb
            JOIN batches b ON b.batch_id = lb.batch_id
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN conservations c ON c.conservation_id = pk.conservation_id
            WHERE lb.label_id = ?
        """
        return self.engine.read(False, sql, (label_id,))

    def generate_label(self, label_id, show_only=False):
        """
        Generate and optionally print a barcode label.

        Args:
            label_id: Label ID to generate barcode for
            show_only: If True, only show the label, don't print

        Returns:
            Path to generated label image or None on error
        """
        # Get label data
        data = self.get_label_data(label_id)
        if not data:
            return None

        # Extract data
        tick = data.get("tick") or label_id
        product_name = data.get("product_name", "")[:38]  # Limit length
        lot = data.get("lot", "")
        expiration = data.get("expiration", "")
        conservation = data.get("conservation", "")
        in_the_dark = data.get("in_the_dark", 0)

        # Format expiration date
        if expiration and "-" in expiration:
            parts = expiration.split("-")
            if len(parts) == 3:
                expiration = f"{parts[2]}/{parts[1]}/{parts[0]}"

        # Get lab name for footer
        lab_name = self.engine.get_setting("lab_name", "")

        # Create label image
        image = self._create_label_image(
            barcode_value=str(tick),
            product_name=product_name,
            lot=lot,
            expiration=expiration,
            conservation=conservation,
            in_the_dark=in_the_dark,
            footer=lab_name
        )

        # Save image
        file_name = f"{tick}.png"
        path = os.path.join(self.barcodes_dir, file_name)
        image.save(path, 'PNG')

        # Print or show
        if show_only:
            image.show()
        else:
            self._print_label(path)

        return path

    def _create_label_image(self, barcode_value, product_name, lot, expiration,
                           conservation="", in_the_dark=False, footer=""):
        """
        Create label image with barcode and text.

        Args:
            barcode_value: Value to encode in barcode
            product_name: Product name/description
            lot: Batch/lot number
            expiration: Expiration date string
            conservation: Conservation method
            in_the_dark: If True, add "Al buio" indicator
            footer: Footer text (e.g., lab name)

        Returns:
            PIL Image object
        """
        # Create white background
        image = Image.new('RGB', (self.LABEL_WIDTH, self.LABEL_HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Fonts
        title_font = self._get_font(22)
        lot_font = self._get_font(18)
        footer_font = self._get_font(16)

        # Draw product name (top)
        draw.text(
            (40, 20),
            product_name,
            fill=(0, 0, 0),
            font=title_font,
            stroke_width=1,
            stroke_fill="gray"
        )

        # Draw lot and expiration
        draw.text((40, 50), f"Lotto: {lot}", fill=(0, 0, 0), font=lot_font)
        draw.text((250, 50), f"Scad: {expiration}", fill=(0, 0, 0), font=lot_font)

        # Generate and paste barcode
        barcode_generated = False

        if code128:
            try:
                barcode_img = code128.image(barcode_value, height=self.BARCODE_HEIGHT)
                image.paste(barcode_img, (self.BARCODE_X, self.BARCODE_Y))
                barcode_generated = True
            except Exception:
                pass

        if not barcode_generated and python_barcode:
            try:
                # Use python-barcode library
                Code128 = python_barcode.get_barcode_class('code128')
                bc = Code128(barcode_value, writer=ImageWriter())
                # Generate to BytesIO and open with PIL
                from io import BytesIO
                buffer = BytesIO()
                bc.write(buffer, options={
                    'module_height': self.BARCODE_HEIGHT * 0.3,
                    'module_width': 0.25,
                    'quiet_zone': 2,
                    'write_text': False
                })
                buffer.seek(0)
                barcode_img = Image.open(buffer)
                # Convert to RGB if needed (for paste compatibility)
                if barcode_img.mode != 'RGB':
                    barcode_img = barcode_img.convert('RGB')
                # Resize to fit
                barcode_img = barcode_img.resize(
                    (self.LABEL_WIDTH - 20, self.BARCODE_HEIGHT),
                    Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
                )
                image.paste(barcode_img, (self.BARCODE_X, self.BARCODE_Y))
                barcode_generated = True
            except Exception:
                pass

        if not barcode_generated:
            # No barcode library available, draw text placeholder
            draw.rectangle(
                [self.BARCODE_X, self.BARCODE_Y,
                 self.LABEL_WIDTH - 10, self.BARCODE_Y + self.BARCODE_HEIGHT],
                outline=(128, 128, 128)
            )
            draw.text(
                (40, self.BARCODE_Y + 30),
                barcode_value,
                fill=(0, 0, 0),
                font=title_font
            )

        # Draw barcode value below barcode (left side)
        draw.text((40, 165), str(barcode_value), fill=(0, 0, 0), font=lot_font)

        # Draw conservation info aligned to right edge
        if conservation:
            cons_text = conservation[:20]
            if in_the_dark:
                cons_text += " | Al buio"
            # Calculate position from right edge
            bbox = draw.textbbox((0, 0), cons_text, font=footer_font)
            cons_width = bbox[2] - bbox[0]
            cons_x = self.LABEL_WIDTH - cons_width - 30  # 30px margin from right
            draw.text((cons_x, 165), cons_text, fill=(0, 0, 0), font=footer_font)

        # Draw footer (lab name) at bottom - centered
        if not footer:
            footer = self.engine.get_setting("lab_name", "")
        if footer:
            bbox = draw.textbbox((0, 0), footer, font=footer_font)
            text_width = bbox[2] - bbox[0]
            x_centered = (self.LABEL_WIDTH - text_width) // 2
            draw.text((x_centered, 210), footer, fill=(0, 0, 0), font=footer_font)

        return image

    def _print_label(self, path):
        """
        Print label image.

        Args:
            path: Path to label image file
        """
        if not os.path.exists(path):
            return False

        try:
            if sys.platform == 'win32':
                # Windows: use ShellExecute
                try:
                    import win32api
                    # Try to print to BARCODE printer
                    printer_name = self.engine.get_setting("barcode_printer", "BARCODE")
                    win32api.ShellExecute(0, "printto", path, printer_name, ".", 0)
                    return True
                except ImportError:
                    # win32api not available, show image
                    img = Image.open(path)
                    img.show()
                    return True

            elif sys.platform == 'darwin':
                # macOS: use lpr
                subprocess.run(['lpr', path], check=True)
                return True

            else:
                # Linux: use lpr
                try:
                    subprocess.run(['lpr', path], check=True)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # lpr not available, show image
                    img = Image.open(path)
                    img.show()
                    return True

        except Exception as e:
            # Fallback: show image
            try:
                img = Image.open(path)
                img.show()
            except Exception:
                pass
            return False

    def generate_simple_label(self, text_lines, footer="", font_size=28):
        """
        Generate a simple text label without barcode.

        Args:
            text_lines: List of text lines to print
            footer: Footer text
            font_size: Font size for text (16-48)

        Returns:
            Path to generated label image
        """
        image = Image.new('RGB', (self.LABEL_WIDTH, self.LABEL_HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Clamp font size
        font_size = max(16, min(48, font_size))

        title_font = self._get_font(font_size)
        text_font = self._get_font(font_size - 4)
        footer_font = self._get_font(16)

        # Calculate line spacing based on font size
        line_spacing = font_size + 12

        y = 30
        for i, line in enumerate(text_lines[:4]):  # Max 4 lines
            font = title_font if i == 0 else text_font
            draw.text(
                (30, y),
                str(line)[:40],
                fill=(0, 0, 0),
                font=font,
                stroke_width=1 if i == 0 else 0,
                stroke_fill="gray" if i == 0 else None
            )
            y += line_spacing

        if footer:
            draw.text((30, 210), footer, fill=(0, 0, 0), font=footer_font)

        # Save and return path
        tick = self.engine.get_tick()
        file_name = f"label_{tick}.png"
        path = os.path.join(self.barcodes_dir, file_name)
        image.save(path, 'PNG')

        return path


def main():
    """Test the barcode label generator."""
    print("Barcode Label Generator Test")
    print("=" * 40)

    # Create a test image without engine
    image = Image.new('RGB', (440, 240), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw test content
    draw.text((40, 20), "Test Product Name", fill=(0, 0, 0))
    draw.text((40, 50), "Lotto: ABC123", fill=(0, 0, 0))
    draw.text((250, 50), "Scad: 31/12/2025", fill=(0, 0, 0))
    draw.text((120, 165), "1234567890123456", fill=(0, 0, 0))
    draw.text((110, 200), "Test Lab", fill=(0, 0, 0))

    # Show test image
    image.show()
    print("Test image displayed")


if __name__ == "__main__":
    main()
