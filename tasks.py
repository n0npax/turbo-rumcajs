import time
import celery
from lib.py3rumcajs.helpers.file_processing import parse_to_dict


@celery.task(bind=True)
def process_files(self, upload_dir, filenames):
    for i, filename in enumerate(filenames):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': len(filenames)+1,
                                'status': filename})
        time.sleep(1)

    return {'current': len(filenames),
            'total': len(filenames),
            'status': 'Task completed',
            'result': filenames}


def process_file(upload_dir, filename):
    data = parse_to_dict(upload_dir + '/' + filename)
    return data


