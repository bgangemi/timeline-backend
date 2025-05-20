from django.core.management.base import BaseCommand
from timeline.models import Group, AbuseType, Event, EventFile, Comment
from django.contrib.auth.models import User
from datetime import date

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Abuse Types
        financial = AbuseType.objects.create(name="Financial", color="#4CAF50")
        legal = AbuseType.objects.create(name="Legal", color="#2196F3")
        psychological = AbuseType.objects.create(name="Psychological", color="#9C27B0")

        # Groups
        groups = [
            Group.objects.create(name="House A", description="Family home bought in 1995"),
            Group.objects.create(name="Company B", description="Parents’ failing business"),
            Group.objects.create(name="Loan C", description="Forged personal loan"),
            Group.objects.create(name="Savings D", description="Sister’s savings"),
            Group.objects.create(name="Apartment E", description="Rental property"),
            Group.objects.create(name="Business F", description="Side business"),
        ]

        # Events
        house_event = Event.objects.create(
            group=groups[0], date=date(1995, 3, 15), name="Purchased in Our Names",
            description="Parents bought a $200,000 house in our names without consent.",
            details="We faced mortgage and tax liabilities.", icon="house"
        )
        house_event.abuse_types.set([financial, legal])
        EventFile.objects.create(event=house_event, file="documents/mortgage.pdf")
        EventFile.objects.create(event=house_event, file="documents/tax_notice.pdf")

        company_event = Event.objects.create(
            group=groups[1], date=date(2000, 6, 10), name="Coerced Investment",
            description="Forced to invest $30,000 in failing company.",
            details="Gaslighting ensured compliance.", icon="building"
        )
        company_event.abuse_types.set([financial, psychological])
        EventFile.objects.create(event=company_event, file="documents/investment.pdf")

        # Comments
        user = User.objects.create_user(username="lawyer", password="securepass")
        Comment.objects.create(
            event=house_event, user=user,
            comment="Critical for fraud claim."
        )