import uuid
url = "hi"
id = (uuid.uuid5(uuid.NAMESPACE_URL, url))
print((str(id)))
