import requests
import string, random, json

ip, port = "127.0.0.1", 8000
url = f"http://{ip}:{port}/users"

print(f"{url = }")

gen_name = lambda x : "".join([ random.choice(string.ascii_letters) for i in range(x) ])
email, name, country = f"{gen_name(7)}.{gen_name(7)}@gmail.com", gen_name(7), gen_name(7)
data = {"email": email, "name": name}

print(data)
resp = requests.post(url, json=data)
print(f"{resp.status_code = }")

if random.choice([True, False]):
    data["country"] = gen_name(9)
    print(f"{data = }")
    resp = requests.put(url, json=data)

