import redis

r = redis.Redis(host='127.0.0.1', port=6379, password='',db=0)

#Simulo che venga cambiato IP rispetto al precedente per l'admin matteofoschi
r.set("administrator","1.3")
ip = r.get("administrator")
print("IP Changed",ip)
