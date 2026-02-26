# ECDHE на эллиптических кривых (secp256k1 / secp256r1)

Простая и понятная реализация протокола **ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)** на Python с использованием кривых **secp256k1** (биткоин) и **secp256r1** (NIST P-256).

## 📌 Возможности

- Поддержка двух популярных кривых: secp256k1 и secp256r1
- Генерация ключевых пар (секретный + публичный ключ)
- Вычисление общего секрета через умножение точек
- Проверка принадлежности точки кривой
- Модульная архитектура для лёгкого добавления новых кривых

## 📁 Структура проекта

- `ecdhe.py` — основной модуль с классами `EllipticCurve` и `Point`
- `curves.py` — конретные объекты эллиптических кривых
- `demo.py` — пример использования протокола ECDHE

## 🚀 Быстрый старт

```python
from curves import SECP256R1

# Выбираем кривую
curve = SECP256R1

# Генерируем ключи для Алисы
alice_secret, alice_public = curve.generate_keypair()

# Генерируем ключи для Боба
bob_secret, bob_public = curve.generate_keypair()

# Вычисляем общий секрет
shared_secret_alice = alice_public * bob_secret
shared_secret_bob = bob_public * alice_secret

# Проверяем
assert shared_secret_alice == shared_secret_bob
print(f"Общий секрет: {shared_secret_alice}")
```

---

# ECDHE on Elliptic Curves (secp256k1 / secp256r1)

A simple and clear implementation of the **ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)** protocol in Python using **secp256k1** (Bitcoin) and **secp256r1** (NIST P-256) curves.

## 📌 Features

- Support for two popular curves: secp256k1 and secp256r1
- Key pair generation (private + public key)
- Shared secret computation via point multiplication
- Point validation on the curve
- Modular architecture for easy addition of new curves

## 📁 Project Structure

- `ecdhe.py` — main module with `EllipticCurve` and `Point` classes
- `curves.py` — specific elliptic curve objects
- `demo.py` — example of ECDHE protocol usage

## 🚀 Quick Start

```python
from curves import SECP256R1

# Select the curve
curve = SECP256R1

# Generate keys for Alice
alice_secret, alice_public = curve.generate_keypair()

# Generate keys for Bob
bob_secret, bob_public = curve.generate_keypair()

# Compute shared secret
shared_secret_alice = alice_public * bob_secret
shared_secret_bob = bob_public * alice_secret

# Verify
assert shared_secret_alice == shared_secret_bob
print(f"Shared secret: {shared_secret_alice}")
```
