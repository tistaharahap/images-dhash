from PIL import Image


class Dhash(object):

    @classmethod
    def get_dhash(self, image, hash_size=8):
        image = image.convert('L').resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS,
        )

        difference = []
        for row in xrange(hash_size):
            for col in xrange(hash_size):
                pixel_left = image.getpixel((col, row))
                pixel_right = image.getpixel((col + 1, row))
                difference.append(pixel_left > pixel_right)

        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0

        return ''.join(hex_string)

    @classmethod
    def compute_hashes(cls, hash1, hash2):
        if not isinstance(hash1, str):
            raise TypeError('hash1 must be a string')
        if not isinstance(hash2, str):
            raise TypeError('hash2 must be a string')

        distance = Dhash.hamming_distance(s1=hash1,
                                          s2=hash2)

        prediction = 'No Match'
        if distance == 0:
            prediction = 'Exact Match'
        elif 1 <= distance <= 10:
            prediction = 'Variance Match'

        return {
            'distance': distance,
            'prediction': prediction
        }

    @classmethod
    def hamming_distance(self, s1, s2):
        if len(s1) != len(s2):
            raise ValueError("Undefined for sequences of unequal length")

        return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))