# Kroger API Setup (the power-up)

Free, about 15 minutes, and it turns the list into live prices and a self-loading pickup cart. Kroger-family stores only (Kroger, Fred Meyer, Ralphs, King Soopers, and the rest).

## 1. Developer account and app

1. Register at https://developer.kroger.com (free).
2. Create an application (production environment). The Products API comes by default.
3. Add `http://localhost:8000/callback` to the app's redirect URIs (needed later for the cart).

## 2. Credentials into the Keychain (never into files)

In Terminal, with your app's real values:

```
security add-generic-password -s kroger-api -a client_id -w 'YOUR_CLIENT_ID'
security add-generic-password -s kroger-api -a client_secret -w 'YOUR_CLIENT_SECRET'
```

## 3. Home store

```
cd ".claude/skills/grocery/scripts"
python3 kroger.py store YOUR_ZIP     # lists nearby stores with IDs
python3 kroger.py set-store STOREID
python3 kroger.py price "half and half"   # proof of life
```

## 4. Cart access (one-time login)

```
python3 kroger.py auth
```

Your browser opens. **Sign in with the account you SHOP with** (the one with your loyalty card), not the developer login; use a private window if the wrong account auto-signs. When the tab says connected and the terminal says authorized, you are done. If the login page spins forever on Safari, turn off iCloud Private Relay and reload.

## What the cart can and cannot do

It can load your real cart with the approved items for pickup. It cannot check out, pick a slot, pay, clip coupons, or read your order history. The last mile is deliberately yours: open the Kroger app, glance the cart, schedule, pay.

## Limits worth knowing

Public-tier rate limits are generous for one household (thousands of calls a day). The public program is aimed at personal use; if you ever run other households through one registered app, read Kroger's current terms first.
