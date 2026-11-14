import os
import django
from decimal import Decimal
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from expenses.models import Category, Transaction


def run():

    # Obtener o crear un usuario de prueba
    user, created = User.objects.get_or_create(
        username='usuario_demo',
        defaults={'email': 'demo@example.com'}
    )
    if created:
        user.set_password('demo1234')
        user.save()
        print(f"Usuario creado: {user.username}")
    else:
        print(f"Usuario existente: {user.username}")

    # Categorías de ejemplo
    categorias_data = [
        ('Sueldo', 'INCOME'),
        ('Freelance', 'INCOME'),
        ('Inversiones', 'INCOME'),
        ('Alimentación', 'EXPENSE'),
        ('Transporte', 'EXPENSE'),
        ('Servicios', 'EXPENSE'),
        ('Entretenimiento', 'EXPENSE'),
        ('Salud', 'EXPENSE'),
        ('Ropa', 'EXPENSE'),
        ('Educación', 'EXPENSE'),
    ]

    categorias_creadas = []
    for nombre, tipo in categorias_data:
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

    # Movimientos de ejemplo (últimos 60 días)
    movimientos_data = [
        ('Sueldo mensual', Decimal('2500000.00'), 'Sueldo', date.today() - timedelta(days=5)),
        ('Pago proyecto web', Decimal('800000.00'), 'Freelance', date.today() - timedelta(days=12)),
        ('Dividendos acciones', Decimal('150000.00'), 'Inversiones', date.today() - timedelta(days=20)),
        ('Supermercado', Decimal('-180000.00'), 'Alimentación', date.today() - timedelta(days=2)),
        ('Transporte público', Decimal('-45000.00'), 'Transporte', date.today() - timedelta(days=3)),
        ('Electricidad', Decimal('-120000.00'), 'Servicios', date.today() - timedelta(days=8)),
        ('Internet', Decimal('-90000.00'), 'Servicios', date.today() - timedelta(days=8)),
        ('Cine y palomitas', Decimal('-65000.00'), 'Entretenimiento', date.today() - timedelta(days=10)),
        ('Consulta médica', Decimal('-110000.00'), 'Salud', date.today() - timedelta(days=15)),
        ('Ropa de oficina', Decimal('-150000.00'), 'Ropa', date.today() - timedelta(days=18)),
        ('Curso de Django', Decimal('-300000.00'), 'Educación', date.today() - timedelta(days=25)),
        ('Cena con amigos', Decimal('-95000.00'), 'Alimentación', date.today() - timedelta(days=1)),
        ('Gasolina', Decimal('-130000.00'), 'Transporte', date.today() - timedelta(days=6)),
        ('Agua', Decimal('-50000.00'), 'Servicios', date.today() - timedelta(days=10)),
        ('Suscripción streaming', Decimal('-40000.00'), 'Entretenimiento', date.today() - timedelta(days=14)),
        ('Medicamentos', Decimal('-75000.00'), 'Salud', date.today() - timedelta(days=22)),
        ('Zapatos', Decimal('-210000.00'), 'Ropa', date.today() - timedelta(days=30)),
        ('Libros', Decimal('-120000.00'), 'Educación', date.today() - timedelta(days=35)),
        ('Pago factura celular', Decimal('-85000.00'), 'Servicios', date.today() - timedelta(days=40)),
        ('Comida rápida', Decimal('-55000.00'), 'Alimentación', date.today() - timedelta(days=45)),
    ]

    for desc, monto, cat_name, fecha in movimientos_data:
        categoria = Category.objects.get(user=user, name=cat_name)
        # El monto se almacena positivo, el tipo lo da la categoría
        monto_abs = abs(monto)
        mov, created = Transaction.objects.get_or_create(
            user=user,
            description=desc,
            amount=monto_abs,
            date=fecha,
            category=categoria,
        )
        if created:
            print(f"Movimiento creado: {desc} - ${monto_abs} ({fecha})")
        else:
            print(f"Movimiento existente: {desc}")

    print("\n¡Seed completado exitosamente!")


if __name__ == '__main__':
    run()
