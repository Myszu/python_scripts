from datetime import datetime, timedelta
# NUMBER OF SEGMENTS
LENGTH = 25

def progress(step: int, steps: int, errors: list = [], delta: int = 0):
    """Generates a progress bar in terminal for iterations.

    Args:
        step (int): Current iteration.
        steps (int): Max number of iterations.
        errors (list, optional): List of errors to count and print out in the end. Defaults to [].
        delta (int, optional): Timed average of iteration. Defaults to 0.
    """
    if step > steps or steps <= 0:
        print(f'Progress bar overflown!')
        return
    percent = round((step/steps)*LENGTH)
    eta = ''
    if delta:
        eta = f' ETA: {(datetime.now() + timedelta(seconds=(delta*(steps-step)))).strftime("%H:%M:%S")}'
    if not errors:
        if step < steps:
            print(f"[{'█' * percent}{'-' * (LENGTH-percent)}] {int(round(step/steps, 2)*100)}% ({step}/{steps}){eta}", end='\r')
            return
        print(f"[{'█' * percent}{'-' * (LENGTH-percent)}] {int(round(step/steps, 2)*100)}% ({step}/{steps}){eta}")
        return
    else:
        if step < steps:
            print(f"[{'█' * percent}{'-' * (LENGTH-percent)}] {int(round(step/steps, 2)*100)}% ({step}/{steps}){eta} [Err: {len(errors)}, {round(len(errors)/steps, 2)*100}%]", end='\r')
            return
        print(f"[{'█' * percent}{'-' * (LENGTH-percent)}] {int(round(step/steps, 2)*100)}% ({step}/{steps}){eta} [Err: {len(errors)}, {round(len(errors)/steps, 2)*100}%]")
        print(f'The list of iterations you might want to investigate or retry: {", ".join(errors)}')
        return
