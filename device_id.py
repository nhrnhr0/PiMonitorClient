import uuid

_device_id = None
def get_device_id():
    global _device_id
    if _device_id is None:
        try:
            with open("device_id.txt", "r") as f:
                _device_id = f.read()
        except:
            _device_id = str(uuid.uuid4())
            with open("device_id.txt", "w") as f:
                f.write(_device_id)
    return _device_id