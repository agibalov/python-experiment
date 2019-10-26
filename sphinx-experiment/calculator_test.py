from calculator import add_numbers, sub_numbers, mul_numbers, div_numbers


# fun-start
def test_fun():
    assert mul_numbers(
        add_numbers(
            div_numbers(9801, 99),
            sub_numbers(2, 1)
        ), 10
    ) == 1000
# fun-end

# add-numbers1-start
def test_add_numbers_adds_numbers():
    assert add_numbers(2, 3) == 5
# add-numbers1-end


# add-numbers2-start
def test_add_numbers_adds_other_numbers():
    assert add_numbers(1, 1) == 2
# add-numbers2-end


# sub-numbers-start
def test_sub_numbers_subs_numbers():
    assert sub_numbers(2, 3) == -1
# sub-numbers-end


# mul-numbers-start
def test_mul_numbers_muls_numbers():
    assert mul_numbers(2, 3) == 6
# mul-numbers-end


# div-numbers-start
def test_div_numbers_divs_numbers():
    assert div_numbers(9801, 99) == 99
# div-numbers-end
