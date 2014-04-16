from models import ImageHash
from models import CoreModel
from datetime import datetime
from errors import ItemExistsError, ImageRecoError


class HashModel(CoreModel):

    def create_hash(self, filename, hash):
        q = self.session.query(ImageHash).filter_by(image_hash=hash).first()

        if q:
            raise ItemExistsError('Hash already exists')

        imghash = ImageHash(image_hash=hash,
                            image_filename=filename,
                            image_created=datetime.now(),
                            active=1)
        self.session.add(imghash)
        self.session.commit()

        q = self.session.query(ImageHash).filter_by(image_hash=hash).first()
        if not q:
            raise ImageRecoError('Server error, failed to insert new image hash')

        return q.as_dict()

    def compare_hash(self, hash, hamming_distance=30):
        sql = '''
            SELECT
                image_hash,
                image_filename,
                image_created,
                BIT_COUNT(
                    CONV(image_hash, 16, 10) ^ CONV('%s', 16, 10)
                ) AS hamming_distance
            FROM
                %s
            HAVING
                hamming_distance < %s
            ORDER BY
                hamming_distance ASC''' % (hash, ImageHash.__tablename__, hamming_distance)

        res = self.db.engine.execute(sql)

        def _process_item(item):
            return {
                'image_hash': item[0],
                'image_filename': item[1],
                'hamming_distance': item[3],
                'image_link': 'http://localhost:5000/static/recos/%s' % item[1]
            }

        return [_process_item(item) for item in res]