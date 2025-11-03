from dataclasses import dataclass
import re


@dataclass
class Client:
    """
    A client/customer who receives invoices.
    Pure Python domain model - no database or API dependencies.
    """
    name: str
    billing_address: str
    email: str
    phone_number: str
    id: int | None = None

    def validate(self):
        """Business rule validation"""
        if not self.name or len(self.name) < 2:
            raise ValueError("Client name must be at least 2 characters")

        if not self.billing_address:
            raise ValueError("Billing address is required")

        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")

        # Phone validation
        phone_pattern = r'^\+?[\d\s\-()]+$'
        if not re.match(phone_pattern, self.phone_number):
            raise ValueError("Invalid phone number format")

    @property
    def display_name(self) -> str:
        """Business logic for display"""
        return self.name.upper()
