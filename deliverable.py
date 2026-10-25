"""
doom_pay_checkout.py

Implements a clean, modular, production-ready 3-line DoomPay checkout session and a mining share benchmark,
as described in https://github.com/doomsday-network/doom-pay/issues/1

Constraints:
- No external dependencies.
- No use of subprocess, ctypes, socket, sys.exit, os.system, or eval.
- Pure Python, passes AST security scan.

Author: [Your Name]
"""

import time
import random
from typing import Dict, Any, Tuple, Optional


class DoomPayCheckoutSession:
    """
    Represents a 3-line DoomPay checkout session.
    """

    def __init__(self, merchant_id: str, amount_wdoom: int, session_id: Optional[str] = None) -> None:
        """
        Initialize a checkout session.

        Args:
            merchant_id (str): Unique merchant identifier.
            amount_wdoom (int): Amount in wDOOM (integer, smallest unit).
            session_id (Optional[str]): Optional session identifier.
        """
        self.merchant_id = merchant_id
        self.amount_wdoom = amount_wdoom
        self.session_id = session_id or self._generate_session_id()
        self.created_at = int(time.time())
        self.paid = False
        self.payment_reference = None

    def _generate_session_id(self) -> str:
        """
        Generate a unique session ID.

        Returns:
            str: Session ID.
        """
        return f"doom_{self.merchant_id}_{int(time.time())}_{random.randint(1000, 9999)}"

    def get_checkout_lines(self) -> Tuple[str, str, str]:
        """
        Returns the 3-line checkout session as a tuple.

        Returns:
            Tuple[str, str, str]: (merchant_id, session_id, amount_wdoom)
        """
        return (
            self.merchant_id,
            self.session_id,
            str(self.amount_wdoom)
        )

    def mark_paid(self, payment_reference: str) -> None:
        """
        Mark the session as paid.

        Args:
            payment_reference (str): Reference for the payment.
        """
        self.paid = True
        self.payment_reference = payment_reference

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize session to dictionary.

        Returns:
            Dict[str, Any]: Session data.
        """
        return {
            "merchant_id": self.merchant_id,
            "amount_wdoom": self.amount_wdoom,
            "session_id": self.session_id,
            "created_at": self.created_at,
            "paid": self.paid,
            "payment_reference": self.payment_reference
        }


def benchmark_mining_share(
    difficulty: int = 100000,
    max_attempts: int = 1000000
) -> Dict[str, Any]:
    """
    Simulate and benchmark a mining share by finding a nonce such that
    hash(session_id + nonce) % difficulty == 0.

    Args:
        difficulty (int): Mining difficulty (higher is harder).
        max_attempts (int): Maximum attempts before giving up.

    Returns:
        Dict[str, Any]: Benchmark results.
    """
    session = DoomPayCheckoutSession(
        merchant_id="benchmark_merchant",
        amount_wdoom=1000
    )
    session_id = session.session_id

    start_time = time.perf_counter()
    found = False
    nonce = 0
    for attempt in range(max_attempts):
        # Simple hash: sum of ordinals of session_id and nonce
        hash_input = f"{session_id}{nonce}"
        hash_value = sum(ord(c) for c in hash_input)
        if hash_value % difficulty == 0:
            found = True
            break
        nonce += 1
    elapsed = time.perf_counter() - start_time

    return {
        "session_id": session_id,
        "difficulty": difficulty,
        "found": found,
        "nonce": nonce if found else None,
        "attempts": attempt + 1,
        "elapsed_seconds": elapsed
    }


# --- TESTS ---

def _test_checkout_session() -> None:
    merchant_id = "merchant_123"
    amount = 100000
    session = DoomPayCheckoutSession(merchant_id, amount)
    lines = session.get_checkout_lines()
    assert lines[0] == merchant_id
    assert lines[2] == str(amount)
    assert isinstance(lines[1], str) and lines[1].startswith("doom_")
    session.mark_paid("tx_abc123")
    data = session.to_dict()
    assert data["paid"] is True
    assert data["payment_reference"] == "tx_abc123"
    print("Checkout session test passed.")


def _test_benchmark_mining_share() -> None:
    result = benchmark_mining_share(difficulty=1000, max_attempts=100000)
    assert result["found"] is True
    assert result["nonce"] is not None
    assert result["attempts"] > 0
    assert result["elapsed_seconds"] >= 0.0
    print("Mining share benchmark test passed.")
    print(f"Result: {result}")


if __name__ == "__main__":
    _test_checkout_session()
    _test_benchmark_mining_share()