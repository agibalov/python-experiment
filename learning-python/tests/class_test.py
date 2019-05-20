def test_class_and_instance_field_behavior():
    class X:
        a = 1
    x1 = X()
    x2 = X()

    assert x1.a == 1 and x2.a == 1 and X.a == 1

    x1.a = 222
    assert x1.a == 222 and x2.a == 1 and X.a == 1

    x2.a = 333
    assert x1.a == 222 and x2.a == 333 and X.a == 1

    X.a = 444
    assert x1.a == 222 and x2.a == 333 and X.a == 444
