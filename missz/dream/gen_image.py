from django.conf import settings
from PIL import Image, ImageDraw, ImageFont


def gen_image(code: int, dream: str, interpret: str):
    begin_text = '分享我的梦'
    end_text = 'MissZ http://8.141.60.45/'
    # font & background image path: /image_gen/*
    font = ImageFont.truetype(f'{settings.BASE_DIR}/image_gen/simfang.ttf', size=24)
    origin = Image.open(f'{settings.BASE_DIR}/image_gen/background.jpg', mode='r')

    row_limit = 20
    row_hight = 30
    dream_iter = range((len(dream) - 1) // row_limit + 1)
    interpret_iter = range((len(interpret) - 1) // row_limit + 1)

    back_size = origin.size
    begin_size = font.getsize(begin_text)
    end_size = font.getsize(end_text)
    dream_size = font.getsize(dream[:row_limit])
    interpret_size = font.getsize(interpret[:row_limit])

    begin_pos = (back_size[0] - begin_size[0]) // 2, 75
    end_pos = (back_size[0] - end_size[0]) // 2, back_size[1] - 90
    dream_pos = [((back_size[0] - dream_size[0]) // 2, 120 + i * row_hight)
                 for i in dream_iter]
    interpret_pos = [((back_size[0] - interpret_size[0]) // 2, 140 + (dream_iter[-1] + i + 1) * row_hight)
                     for i in interpret_iter]

    image = origin.copy()
    draw = ImageDraw.Draw(image)
    draw.text(begin_pos, u'%s' % begin_text, '#f0f8ff', font)
    draw.text(end_pos, u'%s' % end_text, '#f0f8ff', font)
    for i in dream_iter:
        draw.text(dream_pos[i], u'%s' % dream[i * row_limit:(i + 1) * row_limit], '#ffffff', font)
    for i in interpret_iter:
        draw.text(interpret_pos[i], u'%s' % interpret[i * row_limit:(i + 1) * row_limit], '#f8f8ff', font)

    path = f'{settings.MEDIA_ROOT}/{code}.png'
    image.save(path)
