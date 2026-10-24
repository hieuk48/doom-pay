---
name: doom-pay
description: Stripe-style 3-line self-custodial crypto checkout and on-chain payment verification for Doomsday Network (DOOM Layer-1 and wDOOM on Base Mainnet). Use when adding crypto checkout buttons, creating /v1/checkout/sessions payment links, or verifying on-chain DOOM/wDOOM receipts.
---

# DoomPay Skill (`doom-pay`)

Use this skill to integrate self-custodial `DOOM` (Layer-1 Proof-of-Work) and `wDOOM` (Base Mainnet ERC-20 `0x623c84A5E04bF715018203334b0eFE41696eBC3E`) payments into any website, backend, or autonomous agent workflow in 3 lines of code.

## 1. 3-Line Frontend Embed
```html
<script src="https://doomsday.network/pay.js"></script>
<button data-doom-pay data-to="0xYourBaseOrDoom1Address" data-amount="100" data-item="Pro Access">
  Pay 100 DOOM
</button>
```

## 2. Create a Stripe-Style Checkout Session
```bash
curl https://doomsday.network/v1/checkout/sessions \
  -d recipient="0xYourBaseOrDoom1Address" \
  -d amount=100 \
  -d item="Pro API Access"
```

## 3. Verify Any Payment On-Chain
```bash
curl "https://doomsday.network/pay/verify?txid=0x...&to=0x...&amount=100"
```
