import algebra

def test_secrets_random_init_call():
    secret = algebra.Secrets()
    assert isinstance(secret._a, list)
    assert isinstance(secret._b, list)

    # double check if this asserts existence
    assert secret.encrypted_a
    assert secret.encrypted_b
