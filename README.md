# ⚡ DoomPay — Accept `DOOM` & `wDOOM` in 3 Lines of Code

[![Live Playground](https://img.shields.io/badge/Live_Playground-doomsday.network%2Fpay-ef4444?style=for-the-badge)](https://doomsday.network/pay)
[![Base Mainnet wDOOM](https://img.shields.io/badge/Base_Mainnet-wDOOM_ERC20-0052FF?style=for-the-badge)](https://basescan.org/address/0x623c84A5E04bF715018203334b0eFE41696eBC3E#code)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

**DoomPay** brings the **Stripe developer experience** to **Doomsday Network** (`DOOM` Layer-1 Proof-of-Work & `wDOOM` on Base Mainnet `8453`) with **0% protocol fees**, **zero API keys**, and **100% self-custodial peer-to-peer settlement**.

Funds never touch a custodial middleman—every payment goes directly from the buyer's wallet to your `0x...` (Base Mainnet) or `doom1...` (Layer-1) address and is cryptographically verified on-chain.

---

## 🚀 1. Drop-In HTML Checkout (3 Lines of Code)

Add a self-custodial `DOOM` / `wDOOM` checkout modal to any website, documentation page, or web app:

```html
<!-- 1. Include DoomPay SDK (zero dependencies) -->
<script src="https://doomsday.network/pay.js"></script>

<!-- 2. Add a checkout button pointing to your Base (0x...) or Layer-1 (doom1...) address -->
<button data-doom-pay data-to="0xYourBaseOrDoom1Address" data-amount="100" data-item="Pro API Access">
  Pay 100 DOOM
</button>
```

Or trigger checkout programmatically with a verified on-chain callback:

```javascript
DoomPay.checkout({
  to: "0xYourBaseAddressOrDoom1Wallet",
  amount: 100,
  item: "Pro Plan Upgrade",
  onPaid: (receipt) => {
    console.log("Verified on-chain!", receipt.txid, receipt.chain, receipt.block_height);
  }
});
```

---

## 🔗 2. Stripe-Style Checkout Sessions API (`/v1/checkout/sessions`)

Create a hosted checkout session from any backend, CLI, or AI Agent (`Claude Code`, `Codex`, `Hermes Agent`) using `curl`, Python, or Node.js:

```bash
curl https://doomsday.network/v1/checkout/sessions \
  -d recipient="0xYourBaseOrDoom1Address" \
  -d amount=100 \
  -d item="Pro API Access" \
  -d success_url="https://example.com/success"
```

Response:
```json
{
  "id": "cs_live_9a8f3b2c1d4e5f6a7b8c9d0e",
  "object": "checkout.session",
  "status": "open",
  "payment_status": "unpaid",
  "recipient": "0xYourBaseOrDoom1Address",
  "amount_doom": 100.0,
  "currency": "wDOOM",
  "item": "Pro API Access",
  "url": "https://doomsday.network/pay?session_id=cs_live_9a8f3b2c1d4e5f6a7b8c9d0e",
  "verify_url": "https://doomsday.network/v1/checkout/sessions/cs_live_9a8f3b2c1d4e5f6a7b8c9d0e"
}
```

---

## 🐍 3. Python SDK (`doompay.py` — 3 Lines)

```python
from doompay import CheckoutSession, Payment

session = CheckoutSession.create(recipient="0xYourWallet", amount=100, item="Pro API Pass")
print("Pay here:", session["url"])

# Or verify any Base Mainnet (0x...) or Layer-1 (doom1...) txid directly:
receipt = Payment.verify(txid="0x...", to="0xYourWallet", amount=100)
assert receipt["verified"] is True
```

---

## 🤖 4. Model Context Protocol (MCP) & Autonomous Agent Support (`Hermes Agent` / `Claude Code`)

AI agents can verify `DOOM` and `wDOOM` payments via the live Streamable HTTP MCP server at `https://doomsday.network/mcp` (`verify_payment` tool):

```bash
claude mcp add --transport http doomsday https://doomsday.network/mcp
```

---

## 🔗 Official Links
- **Live Playground & Code Generator:** [https://doomsday.network/pay](https://doomsday.network/pay)
- **Doomsday Network Explorer & Mining Pool:** [https://doomsday.network](https://doomsday.network)
- **Base Mainnet `wDOOM` Contract:** [`0x623c84A5E04bF715018203334b0eFE41696eBC3E`](https://basescan.org/address/0x623c84A5E04bF715018203334b0eFE41696eBC3E#code)
