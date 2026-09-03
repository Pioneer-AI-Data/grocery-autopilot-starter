#!/usr/bin/env python3
"""Kroger Products API helper for the grocery skill.

Credentials come from the macOS Keychain (service "kroger-api", accounts
"client_id" and "client_secret"), never from files in the vault. Stdlib only.

Usage:
  kroger.py store 43064            find nearby stores, print IDs
  kroger.py set-store LOCATIONID   remember the home store
  kroger.py price "half and half"  price one term at the home store
  kroger.py price-list             price one term per stdin line, print table
  kroger.py auth                   one-time browser login to grant cart scope
  kroger.py resolve                stdin "term | qty" lines -> UPC matches for review
  kroger.py cart-add               stdin "upc qty" lines -> add to your Kroger cart
"""
import base64
import json
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


def _ssl_ctx():
    """python.org framework builds ship with an empty trust store until their
    Install Certificates step runs; fall back to certifi so this script works
    under any Python on the machine."""
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats().get("x509_ca", 0) == 0:
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            pass
    return ctx


SSL_CTX = _ssl_ctx()

API = "https://api.kroger.com/v1"
HERE = Path(__file__).resolve().parent
CONFIG = HERE / "kroger-config.json"   # location id only; never secrets
_tok = {"value": None, "exp": 0}


def keychain(account):
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "kroger-api", "-a", account, "-w"],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("No Keychain item for kroger-api/" + account
                 + ". Add it with: security add-generic-password -s kroger-api -a "
                 + account + " -w 'VALUE'")
    return r.stdout.strip()


def keychain_set(account, value):
    subprocess.run(
        ["security", "add-generic-password", "-U", "-s", "kroger-api",
         "-a", account, "-w", value],
        check=True, capture_output=True)


def token_post(body):
    basic = base64.b64encode(
        (keychain("client_id") + ":" + keychain("client_secret")).encode()).decode()
    req = urllib.request.Request(
        API + "/connect/oauth2/token", data=urllib.parse.urlencode(body).encode(),
        headers={"Authorization": "Basic " + basic,
                 "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=20, context=SSL_CTX) as r:
        return json.load(r)


REDIRECT = "http://localhost:8000/callback"


def cmd_auth():
    """Authorization-code flow; refresh token lands in the Keychain."""
    import http.server
    import secrets
    state = secrets.token_urlsafe(16)
    url = API + "/connect/oauth2/authorize?" + urllib.parse.urlencode(
        {"response_type": "code", "client_id": keychain("client_id"),
         "redirect_uri": REDIRECT, "scope": "cart.basic:write", "state": state})
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            ok = q.get("state", [""])[0] == state and "code" in q
            if ok:
                got["code"] = q["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h2>Kroger connected. You can close this tab.</h2>" if ok
                else b"<h2>Login failed or state mismatch; rerun kroger.py auth.</h2>")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 8000), H)
    srv.timeout = 600
    print("Opening the browser for the Kroger login...")
    subprocess.run(["open", url])
    while "code" not in got:
        srv.handle_request()
    d = token_post({"grant_type": "authorization_code", "code": got["code"],
                    "redirect_uri": REDIRECT})
    keychain_set("refresh_token", d["refresh_token"])
    print("Authorized: cart scope granted, refresh token stored in Keychain.")


def user_token():
    """Kroger rotates refresh tokens on every use; always persist the new one."""
    d = token_post({"grant_type": "refresh_token",
                    "refresh_token": keychain("refresh_token")})
    if d.get("refresh_token"):
        keychain_set("refresh_token", d["refresh_token"])
    return d["access_token"]


def cmd_resolve():
    loc = home_store() or sys.exit("no home store")
    print("upc	qty	price	match")
    for line in sys.stdin:
        if not line.strip():
            continue
        term, _, qty = line.partition("|")
        term, qty = term.strip(), (qty.strip() or "1")
        rows = price_term(term, loc)
        r = rows[0] if rows else {}
        upc = r.get("upc", "")
        price = r.get("promo") or r.get("regular")
        print("{}	{}	{}	{} {} ({})".format(
            upc or "NOMATCH", qty, price if price is not None else "-",
            r.get("brand") or "", r.get("desc") or term, r.get("size") or "-"))


def cmd_cart_add():
    items = []
    for line in sys.stdin:
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit():
            items.append({"upc": parts[0], "quantity": int(parts[1]),
                          "modality": "PICKUP"})
    if not items:
        sys.exit("no valid 'upc qty' lines on stdin")
    req = urllib.request.Request(
        API + "/cart/add", data=json.dumps({"items": items}).encode(),
        method="PUT",
        headers={"Authorization": "Bearer " + user_token(),
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as r:
        print("cart add HTTP", r.status, "-", len(items), "items pushed (PICKUP)")


def token():
    if _tok["value"] and time.time() < _tok["exp"] - 60:
        return _tok["value"]
    basic = base64.b64encode(
        (keychain("client_id") + ":" + keychain("client_secret")).encode()).decode()
    body = urllib.parse.urlencode(
        {"grant_type": "client_credentials", "scope": "product.compact"}).encode()
    req = urllib.request.Request(
        API + "/connect/oauth2/token", data=body,
        headers={"Authorization": "Basic " + basic,
                 "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=20, context=SSL_CTX) as r:
        d = json.load(r)
    _tok["value"] = d["access_token"]
    _tok["exp"] = time.time() + d.get("expires_in", 1800)
    return _tok["value"]


def get(path, params):
    url = API + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token()})
    with urllib.request.urlopen(req, timeout=20, context=SSL_CTX) as r:
        return json.load(r)


def home_store():
    if CONFIG.is_file():
        return json.loads(CONFIG.read_text()).get("location_id")
    return None


def cmd_store(zipcode):
    d = get("/locations", {"filter.zipCode.near": zipcode, "filter.limit": "5"})
    for loc in d.get("data", []):
        a = loc.get("address", {})
        print(loc["locationId"], "|", loc.get("name"), "|",
              a.get("addressLine1"), a.get("city"))
    print("\nPick one: kroger.py set-store LOCATIONID")


def cmd_set_store(loc_id):
    CONFIG.write_text(json.dumps({"location_id": loc_id}, indent=2) + "\n")
    print("home store set:", loc_id)


def best_item(prod):
    for it in prod.get("items", []):
        if it.get("price"):
            return it
    return (prod.get("items") or [{}])[0]


def price_term(term, loc):
    # The search endpoint 404s on some no-result terms instead of returning
    # an empty list; one bad term must not kill a whole price-list run.
    try:
        d = get("/products", {"filter.term": term, "filter.locationId": loc,
                              "filter.limit": "3"})
    except Exception as exc:
        return [{"term": term, "desc": "lookup failed ({})".format(
            getattr(exc, "code", exc))}]
    out = []
    for prod in d.get("data", []):
        it = best_item(prod)
        p = it.get("price") or {}
        aisles = ", ".join(a.get("description", "") for a in prod.get("aisleLocations", [])[:1])
        out.append({
            "term": term, "desc": prod.get("description"), "brand": prod.get("brand"),
            "upc": prod.get("upc") or (it.get("itemId") if it else None),
            "size": it.get("size"), "regular": p.get("regular"), "promo": p.get("promo"),
            "aisle": aisles})
    return out


def show(rows):
    for r in rows:
        promo = " PROMO ${:.2f}".format(r["promo"]) if r.get("promo") else ""
        reg = "${:.2f}".format(r["regular"]) if r.get("regular") else "no price"
        print("  {} | {} | {} | {}{}{}".format(
            r.get("brand") or "-", r.get("desc"), r.get("size") or "-", reg, promo,
            (" | " + r["aisle"]) if r.get("aisle") else ""))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "store":
        cmd_store(sys.argv[2])
    elif cmd == "set-store":
        cmd_set_store(sys.argv[2])
    elif cmd == "price":
        loc = home_store() or sys.exit("no home store; run: kroger.py store <zip>")
        show(price_term(" ".join(sys.argv[2:]), loc))
    elif cmd == "auth":
        cmd_auth()
    elif cmd == "resolve":
        cmd_resolve()
    elif cmd == "cart-add":
        cmd_cart_add()
    elif cmd == "price-list":
        loc = home_store() or sys.exit("no home store; run: kroger.py store <zip>")
        total = 0.0
        for line in sys.stdin:
            term = line.strip()
            if not term:
                continue
            rows = price_term(term, loc)
            print(term + ":")
            show(rows[:1] or [{"term": term, "desc": "NOT FOUND"}])
            if rows and (rows[0].get("promo") or rows[0].get("regular")):
                total += rows[0].get("promo") or rows[0].get("regular")
        print("\nestimated total (first match each): ${:.2f}".format(total))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
