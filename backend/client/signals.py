# from io import BytesIO
# import logging
# from PIL import Image
# from django.core.files.base import ContentFile
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
# from .models import PhotoProduct



# THUMBNAIL_SIZE = (250, 360)


# # @receiver(post_save, sender=PhotoProduct)
# def generate_thumbnail(sender, instance, **kwargs):
#     image = Image.open(instance.picture)
#     image = image.convert("RGB")
#     image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
#     temp_thumb = BytesIO()
#     image.save(temp_thumb, "JPEG")
#     temp_thumb.seek(0)
#     # set save=False, otherwise it will run in an infinite loop
#     instance.thumbnail.save(instance.fichier.name,ContentFile(temp_thumb.read()),save=False)
#     print('DONE')
#     temp_thumb.close()