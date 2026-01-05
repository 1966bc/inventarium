#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lot Label Generator - Generate and print lot labels (no barcode) for Inventarium.

This module generates lot labels with product information using PIL/Pillow.
Labels show product name, lot, expiration, conservation and location in large text.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import sys
import subprocess

from PIL import Image, ImageDraw, ImageFont


class LotLabel:
    """Generate and print lot labels (no barcode)."""

    # Label dimensions (same as barcode label)
    LABEL_WIDTH = 440
    LABEL_HEIGHT = 260

    def __init__(self, engine):
        """
        Initialize lot label generator.

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
        """Ensure barcodes directory exists (reuse same folder)."""
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

    def get_lot_data(self, batch_id):
        """
        Get lot data from database.

        Args:
            batch_id: Batch ID to get data for

        Returns:
            Dict with lot data or None if not found
        """
        sql = """
            SELECT
                b.batch_id,
                b.description AS lot,
                b.expiration,
                p.description AS product_name,
                pk.label_text,
                pk.label_font_size,
                pk.shelf,
                pk.packaging,
                c.description AS conservation,
                pk.in_the_dark,
                lc.description AS location_type,
                l.room AS location_room
            FROM batches b
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN conservations c ON c.conservation_id = pk.conservation_id
            LEFT JOIN locations l ON l.location_id = pk.location_id
            LEFT JOIN categories lc ON lc.category_id = l.category_id
            WHERE b.batch_id = ?
        """
        return self.engine.read(False, sql, (batch_id,))

    def generate_label(self, batch_id, show_only=False):
        """
        Generate and optionally print a lot label.

        Args:
            batch_id: Batch ID to generate label for
            show_only: If True, only show the label, don't print

        Returns:
            Path to generated label image or None on error
        """
        # Get lot data
        data = self.get_lot_data(batch_id)
        if not data:
            return None

        # Use label_text if set, otherwise use product_name
        label_text = data.get("label_text") or ""
        if not label_text:
            # Fallback: use product name (truncated)
            label_text = data.get("product_name", "")[:35]

        lot = data.get("lot", "")
        expiration = data.get("expiration", "")
        conservation = data.get("conservation", "")
        in_the_dark = data.get("in_the_dark", 0)
        location_type = data.get("location_type", "")
        location_room = data.get("location_room", "")
        shelf = data.get("shelf", "")
        font_size = data.get("label_font_size") or 36  # Default 36

        # Format expiration date
        if expiration and "-" in str(expiration):
            parts = str(expiration).split("-")
            if len(parts) == 3:
                expiration = f"{parts[2]}/{parts[1]}/{parts[0]}"

        # Create label image
        image = self._create_label_image(
            label_text=label_text,
            lot=lot,
            expiration=expiration,
            conservation=conservation,
            in_the_dark=in_the_dark,
            location_type=location_type,
            location_room=location_room,
            shelf=shelf,
            font_size=font_size
        )

        # Save image
        file_name = f"lot_{batch_id}.png"
        path = os.path.join(self.barcodes_dir, file_name)
        image.save(path, 'PNG')

        # Print or show
        if show_only:
            image.show()
        else:
            self._print_label(path)

        return path

    def _create_label_image(self, label_text, lot, expiration,
                           conservation="", in_the_dark=False, 
                           location_type="", location_room="", shelf="", font_size=36):
        """
        Create lot label image with large text (no barcode).

        Args:
            label_text: Main product text (from package.label_text)
            lot: Batch/lot number
            expiration: Expiration date string
            conservation: Conservation method
            in_the_dark: If True, add "Al buio" indicator
            location_type: Location category (e.g., "Frigorifero")
            location_room: Room name (e.g., "Stanza 4")
            shelf: Shelf/ripiano (e.g., "2")
            font_size: Font size for main text (28-52)

        Returns:
            PIL Image object
        """
        # Create white background
        image = Image.new('RGB', (self.LABEL_WIDTH, self.LABEL_HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Fonts - title size from settings, others proportional
        title_font = self._get_font(font_size)
        info_font = self._get_font(max(18, font_size - 14))
        detail_font = self._get_font(max(14, font_size - 18))

        # Calculate max chars based on font size (approx)
        max_chars = int(400 / (font_size * 0.6))

        # Draw main product text (top, large, bold effect)
        draw.text(
            (20, 10),
            label_text[:max_chars],
            fill=(0, 0, 0),
            font=title_font,
            stroke_width=1,
            stroke_fill="gray"
        )

        # Draw horizontal separator line
        draw.line([(15, 55), (self.LABEL_WIDTH - 15, 55)], fill=(128, 128, 128), width=1)

        # Draw lot
        draw.text((20, 65), f"Lotto: {lot}", fill=(0, 0, 0), font=info_font)

        # Draw expiration
        draw.text((20, 95), f"Scad.: {expiration}", fill=(0, 0, 0), font=info_font)

        # Draw conservation
        if conservation:
            cons_text = f"Cons.: {conservation[:22]}"
            if in_the_dark:
                cons_text += " | Al buio"
            draw.text((20, 130), cons_text, fill=(0, 0, 0), font=detail_font)

        # Draw location (room + type + shelf)
        location_parts = []
        if location_room:
            location_parts.append(location_room)
        if location_type:
            location_parts.append(location_type)
        if shelf:
            location_parts.append(f"Rip.{shelf}")
        if location_parts:
            location_text = " - ".join(location_parts)
            draw.text((20, 160), f"Ubic.: {location_text[:28]}", fill=(0, 0, 0), font=detail_font)

        # Draw footer with lab name
        lab_name = self.engine.get_setting("lab_name", "")
        if lab_name:
            draw.text((20, 195), lab_name, fill=(100, 100, 100), font=detail_font)

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
            # Get printer name from local config
            printer_name = self.engine.get_printer_name()

            if sys.platform == 'win32':
                # Windows: use ShellExecute
                try:
                    import win32api
                    # Use configured printer or fallback to "BARCODE"
                    printer = printer_name if printer_name else "BARCODE"
                    win32api.ShellExecute(0, "printto", path, printer, ".", 0)
                    return True
                except ImportError:
                    # win32api not available, show image
                    img = Image.open(path)
                    img.show()
                    return True

            elif sys.platform == 'darwin':
                # macOS: use lpr
                cmd = ['lpr']
                if printer_name:
                    cmd.extend(['-P', printer_name])
                cmd.append(path)
                subprocess.run(cmd, check=True)
                return True

            else:
                # Linux: use lpr
                try:
                    cmd = ['lpr']
                    if printer_name:
                        cmd.extend(['-P', printer_name])
                    cmd.append(path)
                    subprocess.run(cmd, check=True)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # lpr not available, show image
                    img = Image.open(path)
                    img.show()
                    return True

        except Exception:
            # Fallback: show image
            try:
                img = Image.open(path)
                img.show()
            except Exception:
                pass
            return False


def main():
    """Test the lot label generator."""
    print("Lot Label Generator Test")
    print("=" * 40)

    # Create a test image without engine
    image = Image.new('RGB', (440, 260), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw test content
    draw.text((20, 15), "ACETONITRILE HPLC", fill=(0, 0, 0))
    draw.line([(15, 55), (425, 55)], fill=(128, 128, 128), width=1)
    draw.text((20, 70), "Lotto: ABC123", fill=(0, 0, 0))
    draw.text((20, 105), "Scad.: 31/12/2025", fill=(0, 0, 0))
    draw.text((20, 145), "Cons.: +2/+8°C | Al buio", fill=(0, 0, 0))
    draw.text((20, 175), "Ubic.: Frigo Lab 1", fill=(0, 0, 0))
    draw.text((20, 220), "Lab Spettrometria", fill=(100, 100, 100))

    # Show test image
    image.show()
    print("Test image displayed")


if __name__ == "__main__":
    main()
