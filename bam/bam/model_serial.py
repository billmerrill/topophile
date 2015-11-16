import os.path


def write_serial_number(serial_store, sn):
    with open(serial_store, 'wb') as fh:
        fh.write(str(sn))


def format_serial_number(sn):
    if sn > 5000:
        return '%08d' % sn
    else:
        return '%04d' % sn


def new_serial_number(serial_store):

    if not os.path.isfile(serial_store):
        sn = 1
        write_serial_number(serial_store, sn)
    else:
        with open(serial_store, 'r+') as fh:
            try:
                # print fh.read()
                sn = int(fh.read())
                sn += 1
            except ValueError:
                print "value error"
                sn = 1

            fh.seek(0)
            fh.write(str(sn))

    return format_serial_number(sn)
