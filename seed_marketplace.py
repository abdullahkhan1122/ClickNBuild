import json
from app import create_app
from app.models import db, VendorMarketplace
from datetime import datetime

app = create_app()

with app.app_context():
    with open('app/static/data/vendor_marketplace.json') as f:
        data = json.load(f)
        for item in data:
            # Parse created_at to datetime
            created_at = datetime.fromisoformat(item["created_at"]) if item["created_at"] else None
            
            product = VendorMarketplace(
                product_id=item["product_id"],
                name=item["name"],
                description=item["description"],
                price_pkr=item["price_pkr"],
                category=item["category"],
                vendor_name=item["vendor_name"],
                contact_number=item["contact_number"],  #  Added line
                created_at=created_at,
                image=item["image"]
            )
            db.session.add(product)
        db.session.commit()
        print(" Marketplace seeded successfully.")
