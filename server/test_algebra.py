import algebra
import secrets
import nufhe

def test_secrets_random_init_call():
    secret = algebra.Secrets()
    assert isinstance(secret.a, int)
    assert isinstance(secret.b, int)

    assert secret.ciphertext_a
    assert secret.ciphertext_b

def test_secrets_encrypt_decrypt():
    test_data = secrets.randbelow(1000)
    secret = algebra.Secrets()
    assert secret.decrypt(secret.encrypt(test_data)) == test_data

def test_addition():
    secret = algebra.Secrets()
    nufhe.clear_computation_cache(secret.ctx.thread)
    # This would run on a server
    print(type(secret.ciphertext_a), type(secret.ciphertext_b))
    server = algebra.Algebra(secret.ciphertext_a, secret.ciphertext_b, secret.cloud_key)
    encrypted_result = server.add()

    assert secret.decrypt(encrypted_result) == secret.a + secret.b
