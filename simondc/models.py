from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
import base64
import sys
from PIL import Image
import io


sys.path.append(r"/media")
sys.path.append(r"C:\Users\Public\smartlink\smartlink_server\Mask_RCNN")
sys.path.append(r"C:\Users\Public\smartlink\smartlink_server\Mask_RCNN\samples\balloon")



def base64_to_image(base64_string,path):
    imgdata = base64.b64decode(base64_string)
    with open(path, 'wb') as f:
        f.write(imgdata)

def image_to_base64(image):
    img = Image.fromarray(image)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


class Smartlink(models.Model):



    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)
    base64 = models.CharField(max_length=10000000, null=True)
    tabela = models.CharField(max_length=10000,blank=True)

    def __str__(self):
        return f'Smartlink : {self.title}'

    def save(self, force_insert=True, *args, **kwargs):

        kolejka = False

        if not self.slug:
            super().save(*args, **kwargs)
            pk = str(self.pk)
            slug_field = slugify(self.title) + pk
            self.slug = slug_field
            path = settings.MEDIA_ROOT + "/" + self.slug + "_" + self.title + ".png"
            base64_to_image(self.base64, path)
            if kolejka:
                self.base64 = 1
                self.tabela = 1
                return super().save(*args, **kwargs)
            else:
                if self.title == '0':
                    from Mask_RCNN.samples.balloon import smartlink as smartlink_model
                    [img1, data] = smartlink_model.smartlink(path)
                    self.base64 = image_to_base64(img1)
                    self.tabela = data
                    return super().save(*args, **kwargs)
                elif self.title == '1':
                    from Mask_RCNN.samples.balloon import devices_program
                    [img1, data] = devices_program.detect_devices(path)
                    self.base64 = image_to_base64(img1)
                    self.tabela = data
                    return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('smartlink-detail',kwargs ={"slug":self.slug})
