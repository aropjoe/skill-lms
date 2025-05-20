# courses/management/commands/compress_images.py

import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from PIL import Image
from pathlib import Path
from glob import glob
from django.core.files import File # Import File to assign files to ImageField

# Import your ImageContent and Course models
from content.models import ImageContent # Adjust 'content.models' to your actual app name for ImageContent
from courses.models import Course # Adjust 'courses.models' to your actual app name for Course

class Command(BaseCommand):
    help = 'Compresses images in staticfiles and media directories, creating _optimized versions and WebP.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quality',
            type=int,
            default=80,
            help='Quality for JPEG and WebP compression (0-100). Default is 80.'
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='If set, optimized files will overwrite the original ones instead of creating new _optimized files.'
        )
        parser.add_argument(
            '--no-webp',
            action='store_true',
            help='Do not generate WebP versions of images.'
        )
        parser.add_argument(
            '--static-only',
            action='store_true',
            help='Only process static files, skip media files.'
        )
        parser.add_argument(
            '--media-only',
            action='store_true',
            help='Only process media files, skip static files.'
        )
        parser.add_argument(
            '--reprocess-media-webp',
            action='store_true',
            help='Re-processes media images and updates the optimized_image_webp field (for ImageContent and Course).'
        )


    def handle(self, *args, **options):
        quality = options['quality']
        overwrite = options['overwrite']
        no_webp = options['no_webp']
        static_only = options['static_only']
        media_only = options['media_only']
        reprocess_media_webp = options['reprocess_media_webp']

        self.stdout.write(f"Starting image compression with quality: {quality}")

        if not media_only:
            self.process_static_images(quality, overwrite, no_webp)
        if not static_only:
            self.process_media_images(quality, overwrite, no_webp, reprocess_media_webp)

        self.stdout.write(self.style.SUCCESS("Image compression complete!"))

    def compress_image(self, input_path: Path, output_path_prefix: Path, quality: int, no_webp: bool):
        """
        Compresses an image, saving an optimized version and optionally a WebP version.
        Returns paths to generated files.
        """
        try:
            img = Image.open(input_path).convert("RGB") # Convert to RGB to handle transparency consistently

            output_files = []
            original_stem = output_path_prefix.stem
            original_suffix = output_path_prefix.suffix

            # 1. Save optimized original format (JPEG/PNG)
            if original_suffix.lower() in ['.jpg', '.jpeg']:
                output_path_original_fmt = output_path_prefix.with_name(f"{original_stem}_optimized.jpg")
                img.save(output_path_original_fmt, 'jpeg', quality=quality, optimize=True)
                output_files.append(output_path_original_fmt)
                self.stdout.write(f"  -> Saved optimized JPEG: {output_path_original_fmt.name}")
            elif original_suffix.lower() == '.png':
                output_path_original_fmt = output_path_prefix.with_name(f"{original_stem}_optimized.png")
                img.save(output_path_original_fmt, 'png', optimize=True)
                output_files.append(output_path_original_fmt)
                self.stdout.write(f"  -> Saved optimized PNG: {output_path_original_fmt.name}")
            else:
                self.stdout.write(f"  -> Skipping optimization for unsupported format: {input_path.name}")
                return []

            # 2. Save WebP version
            if not no_webp:
                output_path_webp = output_path_prefix.with_name(f"{original_stem}_optimized.webp")
                img.save(output_path_webp, 'webp', quality=quality, method=6) # method=6 is slower but better quality
                output_files.append(output_path_webp)
                self.stdout.write(f"  -> Saved optimized WebP: {output_path_webp.name}")

            return output_files

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {input_path}"))
            return []
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error processing {input_path.name}: {e}"))
            return []

    def replace_original(self, original_path: Path, new_path: Path):
        """Replaces the original file with the new optimized file."""
        if new_path.exists():
            original_path.unlink(missing_ok=True) # Delete original if it exists
            new_path.rename(original_path) # Rename new to original
            self.stdout.write(f"  -> Overwrote original: {original_path.name}")
        else:
            self.stderr.write(self.style.ERROR(f"New optimized file not found for overwrite: {new_path.name}"))

    def process_static_images(self, quality: int, overwrite: bool, no_webp: bool):
        self.stdout.write(self.style.HTTP_INFO("\n--- Processing Static Images ---"))
        image_extensions = ('*.jpg', '*.jpeg', '*.png')

        for static_dir in settings.STATICFILES_DIRS:
            static_path = Path(static_dir)
            if not static_path.is_dir():
                self.stdout.write(self.style.WARNING(f"Static directory not found: {static_path}"))
                continue

            self.stdout.write(f"Searching in: {static_path}")
            found_images = []
            for ext in image_extensions:
                found_images.extend(list(static_path.rglob(ext)))

            if not found_images:
                self.stdout.write(f"No images found in {static_path}")
                continue

            for img_path in found_images:
                self.stdout.write(f"Processing static image: {img_path.relative_to(static_path)}")

                generated_files = self.compress_image(img_path, img_path, quality, no_webp)

                if overwrite and generated_files:
                    if not no_webp and any(p.suffix.lower() == '.webp' for p in generated_files):
                        webp_path = next(p for p in generated_files if p.suffix.lower() == '.webp')
                        self.replace_original(img_path, webp_path)
                    elif any(p.suffix.lower() in ['.jpg', '.jpeg', '.png'] for p in generated_files):
                        original_fmt_path = next(p for p in generated_files if p.suffix.lower() in ['.jpg', '.jpeg', '.png'])
                        self.replace_original(img_path, original_fmt_path)
                    else:
                        self.stderr.write(self.style.ERROR(f"No suitable optimized file to overwrite {img_path.name} with."))


    def process_media_images(self, quality: int, overwrite: bool, no_webp: bool, reprocess_media_webp: bool):
        self.stdout.write(self.style.HTTP_INFO("\n--- Processing Media Images ---"))
        if not hasattr(settings, 'MEDIA_ROOT') or not settings.MEDIA_ROOT:
            self.stderr.write(self.style.ERROR("MEDIA_ROOT is not defined in settings. Skipping media image processing."))
            return

        media_root_path = Path(settings.MEDIA_ROOT)
        if not media_root_path.is_dir():
            self.stderr.write(self.style.ERROR(f"MEDIA_ROOT directory not found: {media_root_path}. Skipping media image processing."))
            return

        # --- Process ImageContent instances ---
        self.stdout.write(self.style.HTTP_INFO("\n  Processing ImageContent instances:"))
        for image_content in ImageContent.objects.all():
            if not image_content.image:
                continue

            original_file_path = Path(image_content.image.path)

            if not original_file_path.exists():
                self.stderr.write(self.style.ERROR(f"    Media file not found at path: {original_file_path}. Skipping."))
                continue

            if image_content.optimized_image_webp and not reprocess_media_webp:
                self.stdout.write(f"    Skipping '{original_file_path.name}': optimized WebP already exists and --reprocess-media-webp not used.")
                continue

            self.stdout.write(f"    Processing ImageContent: {original_file_path.relative_to(media_root_path)}")

            generated_files = self.compress_image(original_file_path, original_file_path, quality, no_webp)

            if not no_webp:
                webp_output_path = original_file_path.with_name(f"{original_file_path.stem}_optimized.webp")
                if webp_output_path.exists():
                    try:
                        with open(webp_output_path, 'rb') as f:
                            image_content.optimized_image_webp.save(webp_output_path.name, File(f), save=False)
                        image_content.save(update_fields=['optimized_image_webp'])
                        self.stdout.write(f"    -> Updated ImageContent for {original_file_path.name} to point to {image_content.optimized_image_webp.name}")
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"    Error updating ImageContent model for {original_file_path.name}: {e}"))
                else:
                    self.stderr.write(self.style.ERROR(f"    Optimized WebP file not found for ImageContent model update: {webp_output_path.name}"))

            if overwrite and generated_files:
                if not no_webp and any(p.suffix.lower() == '.webp' for p in generated_files):
                    webp_path_to_overwrite = next(p for p in generated_files if p.suffix.lower() == '.webp')
                    self.replace_original(original_file_path, webp_path_to_overwrite)
                elif any(p.suffix.lower() in ['.jpg', '.jpeg', '.png'] for p in generated_files):
                    original_fmt_path = next(p for p in generated_files if p.suffix.lower() in ['.jpg', '.jpeg', '.png'])
                    self.replace_original(original_file_path, original_fmt_path)
                else:
                    self.stderr.write(self.style.ERROR(f"    No suitable optimized file to overwrite {original_file_path.name} with."))

        # --- Process Course instances ---
        self.stdout.write(self.style.HTTP_INFO("\n  Processing Course instances:"))
        for course in Course.objects.all():
            if not course.image:
                continue

            original_file_path = Path(course.image.path)

            if not original_file_path.exists():
                self.stderr.write(self.style.ERROR(f"    Media file not found at path: {original_file_path}. Skipping."))
                continue

            if course.optimized_image_webp and not reprocess_media_webp:
                self.stdout.write(f"    Skipping '{original_file_path.name}': optimized WebP already exists for Course and --reprocess-media-webp not used.")
                continue

            self.stdout.write(f"    Processing Course image: {original_file_path.relative_to(media_root_path)}")

            generated_files = self.compress_image(original_file_path, original_file_path, quality, no_webp)

            if not no_webp:
                webp_output_path = original_file_path.with_name(f"{original_file_path.stem}_optimized.webp")
                if webp_output_path.exists():
                    try:
                        # Use File() to assign the file to the ImageField
                        with open(webp_output_path, 'rb') as f:
                            course.optimized_image_webp.save(webp_output_path.name, File(f), save=False)
                        course.save(update_fields=['optimized_image_webp'])
                        self.stdout.write(f"    -> Updated Course for {original_file_path.name} to point to {course.optimized_image_webp.name}")
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"    Error updating Course model for {original_file_path.name}: {e}"))
                else:
                    self.stderr.write(self.style.ERROR(f"    Optimized WebP file not found for Course model update: {webp_output_path.name}"))

            if overwrite and generated_files:
                if not no_webp and any(p.suffix.lower() == '.webp' for p in generated_files):
                    webp_path_to_overwrite = next(p for p in generated_files if p.suffix.lower() == '.webp')
                    self.replace_original(original_file_path, webp_path_to_overwrite)
                elif any(p.suffix.lower() in ['.jpg', '.jpeg', '.png'] for p in generated_files):
                    original_fmt_path = next(p for p in generated_files if p.suffix.lower() in ['.jpg', '.jpeg', '.png'])
                    self.replace_original(original_file_path, original_fmt_path)
                else:
                    self.stderr.write(self.style.ERROR(f"    No suitable optimized file to overwrite {original_file_path.name} with."))