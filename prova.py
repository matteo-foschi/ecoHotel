import redis

r = redis.Redis(host='127.0.0.1', port=6379, password='',db=0)

#Simulo che venga cambiato IP rispetto al precedente per l'admin matteofoschi
r.set("matteofoschi","1.3")
ip = r.get("matteofoschi")
print("Ok",ip)
