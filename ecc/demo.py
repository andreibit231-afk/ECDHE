from curves import SECP256R1

curve = SECP256R1

alice_secret, alice_public = curve.generate_keypair()
print(f"Alice's Secret Key: 0x{alice_secret:x}")
print(f"Alice's Public Key:   {alice_public}")

bob_secret, bob_public = curve.generate_keypair()
print(f"Bob's Secret Key:    0x{bob_secret:x}")
print(f"Bob's Public Key:    {bob_public}")
print('-' * 60)

shared_secret_alice = alice_public * bob_secret
shared_secret_bob = bob_public * alice_secret

assert shared_secret_alice == shared_secret_bob, "Error: shared secrets do not match!"
assert curve.is_on_curve(shared_secret_alice), "Error: shared point is not on the curve"

print("Shared Secret:")
print(f"  X: 0x{shared_secret_alice.x:x}")
print(f"  Y: 0x{shared_secret_alice.y:x}")
print('-' * 60)
print("Success: ECDHE protocol completed.")