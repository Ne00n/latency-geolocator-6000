import geoip2.database, subprocess, ipaddr, random, json, sys

#python3 cutter.py country e.g ES
print("Loading","GeoLite2")
reader = geoip2.database.Reader("GeoLite2-Country.mmdb")


ips = []

try:
    with open("cache.json") as handle:
        cache = json.loads(handle.read())
except:
    cache = {}

with open("asn.dat") as file:
    for line in file:
        if len(line.split("\t")) == 1: continue
        subnet, asn = line.split("\t")
        if subnet.endswith("/32") or subnet.endswith("/31"): continue
        network = ipaddr.IPv4Network(subnet)
        randomIP = ipaddr.IPv4Address(random.randrange(int(network.network) + 1, int(network.broadcast) - 1))
        if subnet in cache:
            ips.append(str(randomIP))
            for i in range(3):
                network = ipaddr.IPv4Network(subnet)
                randomIP = ipaddr.IPv4Address(random.randrange(int(network.network) + 1, int(network.broadcast) - 1))
                if not randomIP in ips: ips.append(str(randomIP))
        else:
            try:
                response = reader.country(randomIP)
                if response.country.iso_code ==  sys.argv[1]:
                    print(f"Found {subnet} in {response.country.iso_code}") 
                    cache[subnet] = sys.argv[1]
                    ips.append(str(randomIP))
                    for i in range(3):
                        network = ipaddr.IPv4Network(subnet)
                        randomIP = ipaddr.IPv4Address(random.randrange(int(network.network) + 1, int(network.broadcast) - 1))
                        if not randomIP in ips: ips.append(str(randomIP))
            except Exception as e:
                print("Skipping",subnet)

with open("cache.json", 'w') as f:
    json.dump(cache, f)

with open("targets.json", 'w') as f:
    json.dump(ips, f)
