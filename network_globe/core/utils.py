import geoip2.database


def geoip_lookup(ip):
    reader = geoip2.database.Reader("GeoLite2-City.mmdb")
    try:
        response = reader.city(ip)
        return {
            "country": response.country.name,
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude,
        }
    finally:
        reader.close()


def get_asn(ip):
    reader = geoip2.database.Reader("GeoLite2-ASN.mmdb")
    try:
        response = reader.asn(ip)
        return {
            "asn": response.autonomous_system_number,
            "asn_organization": response.autonomous_system_organization,
        }
    finally:
        reader.close()