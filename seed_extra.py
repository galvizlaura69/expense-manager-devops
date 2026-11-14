import os
import django
from decimal import Decimal
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from expenses.models import Category, Transaction


def run():

    # Obtener el usuario demo (debe existir ya)
    user = User.objects.filter(username='usuario_demo').first()
    if not user:
        print("Usuario 'usuario_demo' no encontrado. Ejecuta primero seed_data.py")
        return

    # 5 categorías nuevas
    categorias_nuevas = [
        ('Bonificación', 'INCOME'),
        ('Alquiler', 'EXPENSE'),
        ('Gimnasio', 'EXPENSE'),
        ('Tecnología', 'EXPENSE'),
        ('Viajes', 'EXPENSE'),
    ]

    categorias_creadas = []
    for nombre, tipo in categorias_nuevas:
        cat, created = Category.objects.get_or_create(
            user=user,
            name=nombre,
            type=tipo,
        )
        categorias_creadas.append(cat)
        if created:
            print(f"Categoría creada: {cat.name} ({cat.get_type_display()})")
        else:
            print(f"Categoría existente: {cat.name}")

    # 10 movimientos nuevos con fechas variadas y categorías diferentes
    movimientos_nuevos = [
        ('Bono anual', Decimal('500000.00'), 'Bonificación', date(2026, 10, 1)),
        ('Pago alquiler oficina', Decimal('400000.00'), 'Alquiler', date(2026, 10, 5)),
        ('Membresía gimnasio', Decimal('80000.00'), 'Gimnasio', date(2026, 10, 10)),
        ('Laptop nueva', Decimal('1200000.00'), 'Tecnología', date(2026, 10, 15)),
        ('Viaje a Medellín', Decimal('600000.00'), 'Viajes', date(2026, 10, 20)),
        ('Comisión ventas', Decimal('300000.00'), 'Bonificación', date(2026, 11, 1)),
        ('Alquiler casa', Decimal('900000.00'), 'Alquiler', date(2026, 11, 5)),
        ('Clases gimnasio', Decimal('120000.00'), 'Gimnasio', date(2026, 11, 10)),
        ('Celular nuevo', Decimal('800000.00'), 'Tecnología', date(2026, 11, 12)),
        ('Pasaje Bogotá', Decimal('350000.00'), 'Viajes', date(2026, 11, 14)),
    ]

    for desc, monto, cat_name, fecha in movimientos_nuevos:
        categoria = Category.objects.get(user=user, name=cat_name)
        mov, created = Transaction.objects.get_or_create(
            user=user,
            description=desc,
            amount=monto,
            date=fecha,
            category=categoria,
        )
        if created:
            print(f"Movimiento creado: {desc} - ${monto} ({fecha}) - {cat_name}")
        else:
            print(f"Movimiento existente: {desc}")

    print("\n¡Seed extra completado exitosamente!")


if __name__ == '__main__':
    run()
