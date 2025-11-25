from django.db import models
from django.utils.text import slugify


def category_image_upload_to(instance, filename):
    # upload to media root then this:
    return f"blogkit/category/{filename}"


class Category(models.Model):
    # ========== MAIN FIELDS ==========
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    # ========== SEO FIELDS ==========
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Comma-separated keywords"
    )
    canonical_url = models.URLField(blank=True, null=True)

    # ========== IMAGE FIELD ==========
    image = models.ImageField(
        upload_to=category_image_upload_to,
        blank=True,
        null=True
    )

    # ========== META FIELDS ==========
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["title"]

    def __str__(self):
        return self.title

    # ========== AUTO SLUG GENERATION ==========
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            unique_slug = base_slug
            counter = 1

            # Avoid duplication
            while Category.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)
