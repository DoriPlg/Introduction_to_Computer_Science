from ex7 import *


def test_mult():
    assert mult(5,3)==5*3
    assert round(mult(2.1,15)) == round(15*2.1)
    assert mult(-50,10) == -50*10

def test_even():
    assert is_even(2*75) == True
    assert is_even(323) == False
    assert is_even(1) == False
    assert is_even(0) == True

def test_mult_log():
    assert log_mult(5,3) == 5*3
    assert round(log_mult(2.1,15)) == round(15*2.1)
    assert log_mult(-50,10) == -50*10

def test_is_power():
    for i in range(1,50):
        for j in range(1,50):
            assert is_power(i,i**j) is True
def test_is_not_power():
    for i in range(1,50):
        for j in range(1,50):
            assert is_power(i,(i+1)**j) is False

def test_number_of_ones():
    assert number_of_ones(1) == 1
    assert number_of_ones(13) == 6
    assert number_of_ones(126) == sum([digs_in_number(x,1) for x in range(1,127)])

def test_reverse():
    assert "hellp" == reverse("plleh")
    assert reverse("") == ""
    assert reverse("Hey") == "yeH"

def test_lists():
    assert not compare_1d_lists([1,2,3,4,5],[2,4,12,5])
    assert compare_1d_lists([8,3,1,4,5,1,4],[8,3,1,4,5,1,4])
    assert compare_2d_lists([[1,2,3,4,5],[8,3,1,4,5,1,4],[42,3,1]],
                            [[1,2,3,4,5],[8,3,1,4,5,1,4],[42,3,1]])
    assert not compare_2d_lists([[1,2,3,4,5],[8,3,1,4,5,1,4],[42,3,1]],
                                [[1,2,3,4,5],[8,3,2,4,5,1,4],[42,3,1]])
    assert not compare_2d_lists([[1,2,3,4,5],[8,3,1,4,5,1,4],[42,3,1]],
                                [[1,2,3,4,5],[8,3,1,4,5,1,4],[2,4,12,5]])
    assert compare_2d_lists([[1,2,3,4,5],[2,4,12,5],[42,3,1]],
                            [[1,2,3,4,5],[2,4,12,5],[42,3,1]])
    assert compare_1d_lists([],[])
    assert compare_2d_lists([],[])
    assert compare_2d_lists([[]],[[]])
    assert compare_2d_lists([[],[]],[[],[]])
    assert compare_2d_lists([[],[1]],[[],[1]])
    assert not compare_2d_lists([[],[1]],[[],[2]])
    assert not compare_2d_lists([[],[]],[[]])
    assert not compare_2d_lists([],[[]])
    assert compare_2d_lists([[], [1], [2, 3], [4, 5, 6], [7, 8], [9], []],[[], [1], [2, 3], [4, 5, 6], [7, 8], [9], []])

def test_magic():
    magic_0 = magic_list(0)
    lst = []
    assert magic_0 == []
    assert magic_list(1) == [[]]
    assert magic_list(2) == [[],[[]]]
    assert magic_list(3) == [[],[[]],[[],[[]]]]
    for i in range(1,10):
        lst = [l for l in lst]+[lst]
        assert magic_list(i) == lst
