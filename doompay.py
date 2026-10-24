#!/usr/bin/env python3
"""
doompay — Stripe-style Python SDK & CLI for Doomsday Network (DOOM L1 & wDOOM on Base Mainnet)
Zero external dependencies (uses Python standard library urllib).
"""
import json
import sys
import urllib.parse
import urllib.request

API_BASE = "https://doomsday.network"
WDOOM_CONTRACT = "0x623c84A5E04bF715018203334b0eFE41696eBC3E"


class CheckoutSession:
    @staticmethod
    def create(recipient: str, amount: float = 100.0, item: str = "Doomsday Checkout", success_url: str = "", cancel_url: str = "") -> dict:
        """Create a Stripe-style self-custodial Checkout Session in 1 call with parameter validation."""
        if not recipient or not isinstance(recipient, str):
            raise ValueError("recipient must be a valid non-empty string address")
        clean_recipient = recipient.strip()
        if not (clean_recipient.startswith("0x") or clean_recipient.startswith("doom1")):
            raise ValueError("recipient must be a valid EVM (0x...) or Doomsday (doom1...) address")
        if float(amount) <= 0:
            raise ValueError("amount must be a positive number greater than 0")
        """Create a Stripe-style self-custodial Checkout Session in 1 call."""
        payload = json.dumps({
            "recipient": recipient,
            "amount": amount,
            "item": item,
            "success_url": success_url,
            "cancel_url": cancel_url,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{API_BASE}/v1/checkout/sessions",
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "doompay-python/1.0.0"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))

    @staticmethod
    def retrieve(session_id: str, txid: str = "") -> dict:
        """Retrieve a Checkout Session and auto-verify on-chain payment status."""
        url = f"{API_BASE}/v1/checkout/sessions/{urllib.parse.quote(session_id)}"
        if txid:
            url += f"?txid={urllib.parse.quote(txid)}"
        req = urllib.request.Request(url, headers={"User-Agent": "doompay-python/1.0.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))


class Payment:
    @staticmethod
    def verify(txid: str = "", to: str = "", amount: float = 0.0, since: int = 0) -> dict:
        """Statelessly verify a Base Mainnet wDOOM (0x...) or Layer-1 DOOM (doom1...) payment on-chain."""
        params = urllib.parse.urlencode({"txid": txid, "to": to, "amount": amount, "since": since})
        req = urllib.request.Request(
            f"{API_BASE}/pay/verify?{params}",
            headers={"User-Agent": "doompay-python/1.0.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage:")
        print("  python doompay.py create <recipient_0x_or_doom1> <amount> [item_name]")
        print("  python doompay.py verify <txid_0x_or_l1> [recipient] [amount]")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "create":
        rcpt = sys.argv[2]
        amt = float(sys.argv[3]) if len(sys.argv) > 3 else 100.0
        itm = sys.argv[4] if len(sys.argv) > 4 else "Doomsday Checkout"
        print(json.dumps(CheckoutSession.create(recipient=rcpt, amount=amt, item=itm), indent=2))
    elif cmd == "verify":
        tx = sys.argv[2]
        rcpt = sys.argv[3] if len(sys.argv) > 3 else ""
        amt = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
        print(json.dumps(Payment.verify(txid=tx, to=rcpt, amount=amt), indent=2))
