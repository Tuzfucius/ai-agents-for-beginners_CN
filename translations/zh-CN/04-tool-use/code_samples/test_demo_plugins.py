from demo_tool_agent import TimePlugin, CalculatorPlugin

def test_calculator_add():
    calc = CalculatorPlugin()
    result = calc.add(5, 7)
    assert result == 12
    print("test_calculator_add 通过")

def test_calculator_subtract():
    calc = CalculatorPlugin()
    result = calc.subtract(10, 4)
    assert result == 6
    print("test_calculator_subtract 通过")

def test_time_plugin():
    # 我们不容易测试精确时间，但可以检查格式
    time_plugin = TimePlugin()
    time_str = time_plugin.get_current_time()
    # 期望格式 YYYY-MM-DD HH:MM:SS
    assert len(time_str) == 19
    assert "-" in time_str
    assert ":" in time_str
    print("test_time_plugin 通过")

if __name__ == "__main__":
    try:
        test_calculator_add()
        test_calculator_subtract()
        test_time_plugin()
        print("所有测试通过！")
    except AssertionError as e:
        print(f"测试失败：{e}")
    except Exception as e:
        print(f"发生错误：{e}")
