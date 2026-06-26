"""Load TechNest Electronics catalog, shipping boxes, and sample orders."""

from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from boxes.models import ShippingBox
from orders.models import Order, OrderItem
from products.models import Product

PRODUCTS = [
    {
        "sku": "ELE001",
        "name": "Wireless Mouse",
        "category": "Computer Accessories",
        "length": Decimal("11"),
        "width": Decimal("6"),
        "height": Decimal("4"),
        "weight": Decimal("0.120"),
        "price": Decimal("699"),
    },
    {
        "sku": "ELE002",
        "name": "Mechanical Keyboard",
        "category": "Computer Accessories",
        "length": Decimal("45"),
        "width": Decimal("16"),
        "height": Decimal("4"),
        "weight": Decimal("1.100"),
        "price": Decimal("2499"),
    },
    {
        "sku": "ELE003",
        "name": "Laptop Stand",
        "category": "Office Accessories",
        "length": Decimal("30"),
        "width": Decimal("25"),
        "height": Decimal("5"),
        "weight": Decimal("1.200"),
        "price": Decimal("1499"),
    },
    {
        "sku": "ELE004",
        "name": "External SSD (1TB)",
        "category": "Storage Devices",
        "length": Decimal("10"),
        "width": Decimal("7"),
        "height": Decimal("2"),
        "weight": Decimal("0.080"),
        "price": Decimal("6999"),
    },
    {
        "sku": "ELE005",
        "name": "USB-C Hub",
        "category": "Computer Accessories",
        "length": Decimal("12"),
        "width": Decimal("5"),
        "height": Decimal("2"),
        "weight": Decimal("0.150"),
        "price": Decimal("1299"),
    },
    {
        "sku": "ELE006",
        "name": "Bluetooth Speaker",
        "category": "Audio Devices",
        "length": Decimal("22"),
        "width": Decimal("10"),
        "height": Decimal("10"),
        "weight": Decimal("1.500"),
        "price": Decimal("3499"),
    },
    {
        "sku": "ELE007",
        "name": "Noise Cancelling Headphones",
        "category": "Audio Devices",
        "length": Decimal("22"),
        "width": Decimal("20"),
        "height": Decimal("10"),
        "weight": Decimal("0.350"),
        "price": Decimal("8999"),
    },
    {
        "sku": "ELE008",
        "name": "Wi-Fi Router",
        "category": "Networking Devices",
        "length": Decimal("25"),
        "width": Decimal("18"),
        "height": Decimal("6"),
        "weight": Decimal("0.600"),
        "price": Decimal("2799"),
    },
    {
        "sku": "ELE009",
        "name": "Full HD Webcam",
        "category": "Computer Accessories",
        "length": Decimal("12"),
        "width": Decimal("8"),
        "height": Decimal("7"),
        "weight": Decimal("0.250"),
        "price": Decimal("2199"),
    },
    {
        "sku": "ELE010",
        "name": "Power Bank (20000mAh)",
        "category": "Mobile Accessories",
        "length": Decimal("16"),
        "width": Decimal("8"),
        "height": Decimal("3"),
        "weight": Decimal("0.450"),
        "price": Decimal("1999"),
    },
    {
        "sku": "ELE011",
        "name": "Mini Projector",
        "category": "Display Devices",
        "length": Decimal("25"),
        "width": Decimal("20"),
        "height": Decimal("10"),
        "weight": Decimal("2.000"),
        "price": Decimal("14999"),
    },
    {
        "sku": "ELE012",
        "name": "24-inch LED Monitor",
        "category": "Display Devices",
        "length": Decimal("60"),
        "width": Decimal("38"),
        "height": Decimal("12"),
        "weight": Decimal("4.500"),
        "price": Decimal("12999"),
    },
    {
        "sku": "ELE013",
        "name": "Camera Tripod",
        "category": "Camera Accessories",
        "length": Decimal("70"),
        "width": Decimal("12"),
        "height": Decimal("12"),
        "weight": Decimal("2.500"),
        "price": Decimal("3999"),
    },
    {
        "sku": "ELE014",
        "name": "Portable Printer",
        "category": "Office Accessories",
        "length": Decimal("36"),
        "width": Decimal("18"),
        "height": Decimal("10"),
        "weight": Decimal("2.800"),
        "price": Decimal("9999"),
    },
    {
        "sku": "ELE015",
        "name": "Gaming Controller",
        "category": "Gaming Accessories",
        "length": Decimal("18"),
        "width": Decimal("17"),
        "height": Decimal("8"),
        "weight": Decimal("0.300"),
        "price": Decimal("3299"),
    },
]

BOXES = [
    {
        "box_code": "BX-S01",
        "name": "Small Box",
        "length": Decimal("20"),
        "width": Decimal("15"),
        "height": Decimal("10"),
        "max_weight_capacity": Decimal("1"),
        "cost": Decimal("30"),
    },
    {
        "box_code": "BX-M01",
        "name": "Medium Box",
        "length": Decimal("35"),
        "width": Decimal("25"),
        "height": Decimal("15"),
        "max_weight_capacity": Decimal("3"),
        "cost": Decimal("50"),
    },
    {
        "box_code": "BX-L01",
        "name": "Large Box",
        "length": Decimal("50"),
        "width": Decimal("35"),
        "height": Decimal("20"),
        "max_weight_capacity": Decimal("7"),
        "cost": Decimal("80"),
    },
    {
        "box_code": "BX-XL01",
        "name": "Extra Large Box",
        "length": Decimal("70"),
        "width": Decimal("45"),
        "height": Decimal("25"),
        "max_weight_capacity": Decimal("12"),
        "cost": Decimal("120"),
    },
    {
        "box_code": "BX-XXL01",
        "name": "Double XL Box",
        "length": Decimal("90"),
        "width": Decimal("60"),
        "height": Decimal("35"),
        "max_weight_capacity": Decimal("20"),
        "cost": Decimal("180"),
    },
    {
        "box_code": "BX-HD01",
        "name": "Heavy Duty Box",
        "length": Decimal("120"),
        "width": Decimal("80"),
        "height": Decimal("60"),
        "max_weight_capacity": Decimal("35"),
        "cost": Decimal("300"),
    },
]

ORDERS = [
    {
        "order_number": "ORD001",
        "customer_name": "Rahul Sharma",
        "items": [("ELE001", 1)],
    },
    {
        "order_number": "ORD002",
        "customer_name": "Priya Patel",
        "items": [("ELE001", 2), ("ELE004", 1)],
    },
    {
        "order_number": "ORD003",
        "customer_name": "Amit Kumar",
        "items": [("ELE002", 1)],
    },
    {
        "order_number": "ORD004",
        "customer_name": "Sneha Reddy",
        "items": [("ELE002", 1), ("ELE001", 1)],
    },
    {
        "order_number": "ORD005",
        "customer_name": "Vikram Singh",
        "items": [("ELE006", 1)],
    },
    {
        "order_number": "ORD006",
        "customer_name": "Ananya Iyer",
        "items": [("ELE007", 1), ("ELE009", 1)],
    },
    {
        "order_number": "ORD007",
        "customer_name": "Karan Mehta",
        "items": [("ELE003", 1), ("ELE010", 1)],
    },
    {
        "order_number": "ORD008",
        "customer_name": "Divya Nair",
        "items": [("ELE012", 1)],
    },
    {
        "order_number": "ORD009",
        "customer_name": "Arjun Desai",
        "items": [("ELE013", 1)],
    },
    {
        "order_number": "ORD010",
        "customer_name": "Meera Joshi",
        "items": [("ELE012", 1), ("ELE002", 1)],
    },
]


class Command(BaseCommand):
    help = "Load TechNest Electronics product catalog, shipping boxes, and sample orders."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush-orders",
            action="store_true",
            help="Delete orders that are not part of the demo catalog.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        catalog_skus = {product["sku"] for product in PRODUCTS}
        catalog_box_codes = {box["box_code"] for box in BOXES}
        catalog_order_numbers = {order["order_number"] for order in ORDERS}

        for data in PRODUCTS:
            Product.objects.update_or_create(sku=data["sku"], defaults=data)

        Product.objects.exclude(sku__in=catalog_skus).update(is_active=False)

        for data in BOXES:
            ShippingBox.objects.update_or_create(box_code=data["box_code"], defaults=data)

        ShippingBox.objects.exclude(box_code__in=catalog_box_codes).update(is_active=False)

        product_map = Product.objects.in_bulk(field_name="sku")

        for order_data in ORDERS:
            order, _ = Order.objects.update_or_create(
                order_number=order_data["order_number"],
                defaults={
                    "customer_name": order_data["customer_name"],
                    "order_date": date.today(),
                },
            )
            OrderItem.objects.filter(order=order).delete()
            for sku, quantity in order_data["items"]:
                OrderItem.objects.create(
                    order=order,
                    product=product_map[sku],
                    quantity=quantity,
                )

        if options["flush_orders"]:
            Order.objects.exclude(order_number__in=catalog_order_numbers).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {len(PRODUCTS)} products, {len(BOXES)} boxes, "
                f"and {len(ORDERS)} sample orders."
            )
        )
