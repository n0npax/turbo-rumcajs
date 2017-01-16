import celery
from lib.py3rumcajs.helpers.file_processing import parse_to_dict
from lib.py3rumcajs.algorithms.common import calibrate


@celery.task(bind=True)
def process_files(self, upload_dir, filenames, settings):
    for i, filename in enumerate(filenames):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': len(filenames),
                                'status': filename})

    return {'current': len(filenames),
            'total': len(filenames),
            'status': 'Task completed',
            'result': filenames}


def process_file(upload_dir, filename, settings):
    data = parse_to_dict(upload_dir + '/' + filename, settings)
    calibrate(data)
    return data


